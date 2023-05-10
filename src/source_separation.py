import io
import select
from shutil import rmtree
import subprocess as sp
import sys
from typing import Dict, Tuple, Optional, IO


class DemucsLib:

    def __init__(self) -> None:
        self.model = "htdemucs"
        self.mp3 = True
        self.mp3_rate = 320
        self.float32 = False
        self.int24 = False
        self.two_stems = None


    def copy_process_streams(self, process: sp.Popen):
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


    def separate(self, inp, outp):
        cmd = ["demucs", "-o", str(outp)]
        if self.mp3:
            cmd += ["--mp3", f"--mp3-bitrate={self.mp3_rate}"]
        if self.float32:
            cmd += ["--float32"]
        if self.int24:
            cmd += ["--int24"]
        if self.two_stems is not None:
            cmd += [f"--two-stems={self.two_stems}"]

        print("Going to separate file:")
        print(inp)
        print("With command: ", " ".join(cmd))
        p = sp.Popen(cmd + [inp], stdout=sp.PIPE, stderr=sp.PIPE)

        self.copy_process_streams(p)
        p.wait()
        if p.returncode != 0:
            print("Command failed, something went wrong.")

        out_path = outp + 'htdemucs/' + inp.split('/')[-1].split('.mp3')[0] + '/other.mp3'
        return out_path