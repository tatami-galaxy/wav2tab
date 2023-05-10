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
from source_separation import DemucsLib
from pitch_detection import BasicPitchLib
from tab_generation import GuitarCMD

if __name__ == '__main__':

    argp = ArgumentParser()

    # song input -> mp3 file (for now)
    # make sure file has no space in name (for now)
    argp.add_argument('--in_path', type=str, default=None)
    # stems output
    argp.add_argument('--out_path', type=str, default='./')

    # parse and check cli arguments #
    args = argp.parse_args() 

    # source separator
    separator = DemucsLib()

    # pitch detector
    pitch_detector = BasicPitchLib()

    # tab generator
    tab_generator = GuitarCMD()

    # separate into stems -> other.mp3 has guitar for now
    outfile_path = separator.separate(args.in_path, args.out_path)

    # get midi
    # note_events: A list of note event tuples (start_time_s, end_time_s, pitch_midi, amplitude, bends)
    note_events = pitch_detector.get_midi_events(outfile_path)

    # generate tabs
    tab_generator.generate(note_events)

    


