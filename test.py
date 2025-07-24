import pretty_midi
from music21 import *
import pickle
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import time
import os
import glob
from itertools import groupby
import mido
from mido import MidiFile, merge_tracks, tempo2bpm
import math

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import (
    Dense,
    LSTM,
    Bidirectional,
    Dropout,
    GlobalMaxPooling1D,
    Activation,
    GlobalMaxPooling2D,
)
from keras_self_attention import SeqSelfAttention
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
from keras.layers import Layer
from tensorflow.python.client import device_lib
import keras

# data_path = "./selected_data/"
data_path = "./data/"
# data_path = "./sample_data/"
# encoded_data_path = "./encoded_doug_mckenzie_midi_32/"
encoded_data_path = "./encoded_data/"


def extract_midi_info(path):
    # Parse the MIDI file
    mid = converter.parse(path)

    # Find the part with the most notes
    part_lengths = [len(part.flat.notes) for part in mid.parts]
    max_idx = np.argmax(part_lengths)

    # Assume the piano part is the part with the most notes
    piano_part = mid.parts[max_idx]

    # Find the BPM (tempo)
    bpm = None
    for i in piano_part.recurse().getElementsByClass(tempo.MetronomeMark):
        bpm = i.getQuarterBPM()
        break

    if bpm is None:
        bpm = 120  # Default to 120 BPM if no tempo is found

    # Find the key signature
    try:
        key_sig = piano_part.analyze("key")
    except Exception as e:
        print(f"Error while finding key signature: {e}")
        return None, None

    # Convert key signature to major
    key_in_major = key_sig.asKey(mode="major")

    # Calculate the offset by the tonic's pitch class
    offset_by = key_in_major.tonic.pitchClass

    return offset_by, bpm


def preprocess_midi(path, offset_by, bpm):
    mid = pretty_midi.PrettyMIDI(midi_file=path)
    print("Here")
    print(mid)
    filtered_inst_ls = [
        inst
        for inst in mid.instruments
        if ((len(inst.notes) > 0) and (inst.is_drum == False) and (inst.program < 8))
    ]
    print(filtered_inst_ls)
    piano = filtered_inst_ls[np.argmax([len(inst.notes) for inst in filtered_inst_ls])]
    start_time = piano.notes[0].start
    end_time = piano.get_end_time()

    quater_note_len = 60 / bpm
    #     Set 4 for 16th note, 8 for 32 note
    nth_note = 8
    #     Set fs to get 16th notes
    fs = 1 / (quater_note_len / nth_note)
    #     fs = 100
    print(piano)
    piano_roll = piano.get_piano_roll(
        fs=fs, times=np.arange(start_time, end_time, 1.0 / fs)
    )
    piano_roll = np.roll(piano_roll, -offset_by)
    out = np.where(piano_roll > 0, 1, 0)

    return out.T


def process_piano_roll(piano_roll, max_consecutive=64):
    #     This function is to remove consecutive notes that last for more than roughtly 2 secs
    prev = np.random.rand(128)
    count = 0
    remove_idxs = []
    remove_slice = []
    for idx, piano_slice in enumerate(piano_roll):
        #         print(prev.shape)
        #         print(piano_slice.shape)
        if np.array_equal(prev, piano_slice):
            count += 1
            if count > max_consecutive:
                remove_idxs.append(idx)
                if str(piano_slice) not in remove_slice:
                    remove_slice.append(str(piano_slice))
        else:
            count = 0
        prev = piano_slice
    print(piano_roll)
    out_piano_roll = np.delete(piano_roll, remove_idxs, axis=0)
    return out_piano_roll


failed_list = []
# keep track of list of midi we failed to parse and preprocess
for temp in glob.glob(data_path + "*.mid"):
    try:
        print(temp)
        offset_by, bpm = extract_midi_info(temp)
        print("First part complete!")
        print(offset_by, bpm)

        piano_roll = preprocess_midi(temp, offset_by, bpm)
        print("Second part complete!")
        piano_roll = process_piano_roll(piano_roll)
        print("Third part complete!")
        name = temp.split("/")[-1].split(".")[0]

        out_name = encoded_data_path + "AutumnLeaves.npy"

        np.save(out_name, piano_roll)
        print(f"saved {out_name}")

    except Exception as e:
        print(f"Failed to preprocess {temp}")
        print(e)
        failed_list.append(temp)
        continue
