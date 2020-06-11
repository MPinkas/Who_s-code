import sys
from os import listdir
from os.path import isfile, join
import os
import random
from itertools import islice
from enum import Enum, unique

input_path = "github_data/"
output_path = "github_data_slices/"

MIN_LINES_PER_SLICE = 1
MAX_LINES_PER_SLICE = 5


@unique
class MsgTypes(Enum):
    ERROR = "ERROR"
    INFO = "INFO"


def print_msg(msg_type, msg):
    print("[" + msg_type.value + "] " + str(msg))


def main():
    if not os.path.exists(input_path):
        print_msg(MsgTypes.ERROR, "Cannot find the path specified: " + input_path)
        exit(1)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    original = sys.stdout

    input_files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    print_msg(MsgTypes.INFO, "Input :" + str(input_files))

    for file in input_files:
        print_msg(MsgTypes.INFO, ">> " + file)
        with open(input_path + file, mode="r", encoding="utf-8") as input_file:
            output_file = "_" + file.replace("all_data", "all_data_", 1)
            i = 0
            with open(output_path + output_file, mode="w", encoding="utf-8") as file_handle:
                while True:
                    sys.stdout = file_handle
                    random_num_lines = random.randint(MIN_LINES_PER_SLICE, MAX_LINES_PER_SLICE)
                    lines = list(islice(input_file, random_num_lines))
                    if not lines:
                        sys.stdout = original
                        break
                    print(lines)
                    sys.stdout = original


main()