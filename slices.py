import numpy as np
from os import listdir
from os.path import isfile, join
import os
import random
from enum import Enum, unique

STR_ARRAY_SIZE = 10000
INPUT_DIR = "github_data/"


@unique
class MsgTypes(Enum):
    ERROR = "ERROR"
    INFO = "INFO"


def print_msg(msg_type, msg):
    print("[" + msg_type.value + "] " + str(msg))


def check_dir(input_dir):
    if not os.path.exists(input_dir):
        print_msg(MsgTypes.ERROR, "Cannot find the path specified: " + input_dir)
        exit(0)


def create_snippets(total_samples, input_dir, min_lines_per_slice=1, max_lines_per_slice=5):
    input_str = []
    input_lbl = []

    input_files = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
    total_num_of_files = len(input_files)
    print_msg(MsgTypes.INFO, "Input Files:" + str(input_files))

    while total_samples:
        random_file_index = random.randint(0, total_num_of_files-1)
        print_msg(MsgTypes.INFO, ">> " + input_files[random_file_index])

        random_num_code_lines = random.randint(min_lines_per_slice, max_lines_per_slice)

        with open(input_dir + input_files[random_file_index], mode="r", encoding="utf-8") as input_file:
            all_file_lines = input_file.readlines()
            file_len = len(all_file_lines)
            random_starting_line = random.randint(1, file_len) - 1
            if random_starting_line + random_num_code_lines > file_len:
                lines = all_file_lines[random_starting_line:]
            else:
                lines = all_file_lines[random_starting_line:random_starting_line+random_num_code_lines]
            input_str.append("".join(lines))
            input_lbl.append(random_file_index)
        total_samples = total_samples - 1
    return np.array(input_str), np.array(input_lbl)


str_arr, lbl_arr = create_snippets(STR_ARRAY_SIZE, INPUT_DIR)
