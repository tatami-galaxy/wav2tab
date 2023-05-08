from argparse import ArgumentParser
import io
from pathlib import Path
import select
from shutil import rmtree
import subprocess as sp
import sys
from typing import Dict, Tuple, Optional, IO
from os.path import dirname, abspath
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import numpy as np
import librosa

# get root directory
#root = abspath(__file__)
#while root.split('/')[-1] != 'wav2tab':
    #root = dirname(root)

# hyps #

model = "htdemucs"
extensions = ["mp3", "wav", "ogg", "flac"]  # we will look for all those file types.
two_stems = None   # only separate one stems from the rest, for instance
# two_stems = "vocals"

# Options for the output audio.
mp3 = True
mp3_rate = 320
float32 = False  # output as float 32 wavs, unsused if 'mp3' is True.
int24 = False    # output as int24 wavs, unused if 'mp3' is True.
# You cannot set both `float32 = True` and `int24 = True` !!

def find_files(in_path):
    out = []
    for file in Path(in_path).iterdir():
        if file.suffix.lower().lstrip(".") in extensions:
            out.append(file)
    return out


def copy_process_streams(process: sp.Popen):
    def raw(stream: Optional[IO[bytes]]) -> IO[bytes]:
        assert stream is not None
        if isinstance(stream, io.BufferedIOBase):
            stream = stream.raw
        return stream

    p_stdout, p_stderr = raw(process.stdout), raw(process.stderr)
    stream_by_fd: Dict[int, Tuple[IO[bytes], io.StringIO, IO[str]]] = {
        p_stdout.fileno(): (p_stdout, sys.stdout),
        p_stderr.fileno(): (p_stderr, sys.stderr),
    }
    fds = list(stream_by_fd.keys())

    while fds:
        # `select` syscall will wait until one of the file descriptors has content.
        ready, _, _ = select.select(fds, [], [])
        for fd in ready:
            p_stream, std = stream_by_fd[fd]
            raw_buf = p_stream.read(2 ** 16)
            if not raw_buf:
                fds.remove(fd)
                continue
            buf = raw_buf.decode()
            std.write(buf)
            std.flush()

# separate all song in directory passed in
def separate_dir(inp=None, outp=None):
    inp = inp 
    outp = outp 
    cmd = ["python3", "-m", "demucs.separate", "-o", str(outp), "-n", model]
    if mp3:
        cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]
    if float32:
        cmd += ["--float32"]
    if int24:
        cmd += ["--int24"]
    if two_stems is not None:
        cmd += [f"--two-stems={two_stems}"]
    files = [str(f) for f in find_files(inp)]
    if not files:
        print(f"No valid audio files in {inp}")
        return
    print("Going to separate the files:")
    print('\n'.join(files))
    print("With command: ", " ".join(cmd))
    p = sp.Popen(cmd + files, stdout=sp.PIPE, stderr=sp.PIPE)
    copy_process_streams(p)
    p.wait()
    if p.returncode != 0:
        print("Command failed, something went wrong.")


def separate(inp=None, outp=None):
    inp = inp 
    outp = outp 
    cmd = ["demucs", "-o", str(outp)]
    if mp3:
        cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]
    if float32:
        cmd += ["--float32"]
    if int24:
        cmd += ["--int24"]
    if two_stems is not None:
        cmd += [f"--two-stems={two_stems}"]

    print("Going to separate file:")
    print(inp)
    print("With command: ", " ".join(cmd))
    p = sp.Popen(cmd + [inp], stdout=sp.PIPE, stderr=sp.PIPE)

    copy_process_streams(p)
    p.wait()
    if p.returncode != 0:
        print("Command failed, something went wrong.")


def pitch_to_note(note_events):
    ret_list = []
    for event in note_events:
        l = list(event)
        note = librosa.midi_to_note(event[2], unicode=False)  # event[2] is pitch
        l[2] = note
        ret_list.append(l)
    return ret_list


if __name__ == '__main__':

    argp = ArgumentParser()

    # song input -> mp3 file (for now)
    # make sure file has no space in name (for now)
    argp.add_argument('--in_path', type=str, default=None)
    # stems output
    argp.add_argument('--out_path', type=str, default='./')

    # parse and check cli arguments #
    args = argp.parse_args() 

    # separate into stems -> other.mp3 has guitar for now
    separate(args.in_path, args.out_path)

    # midi : pretty_midi.PrettyMIDI object
    # note_events: A list of note event tuples (start_time_s, end_time_s, pitch_midi, amplitude, bends)
    outfile_path = args.out_path + 'htdemucs/' + args.in_path.split('/')[-1].split('.mp3')[0] + '/other.mp3'

    model_output, midi_data, note_events = predict(outfile_path)

    # sort note events according to start time 
    sorted_events = sorted(note_events, key=lambda x: x[0])  # x[0] is start time

    # midi pitch to note
    # each event is now a list [start_time_s, end_time_s, pitch_midi, amplitude, bends]
    music_note_events = pitch_to_note(sorted_events)

    print(music_note_events[0])

    ## fix guitar constants ##
    


