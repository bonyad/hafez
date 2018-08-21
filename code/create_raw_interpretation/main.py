#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from unidecode import unidecode
import os


def main():
    with open("raw.txt", "r", encoding="UTF-8") as input_text:
        rawdata = input_text.readlines()
    i = 1
    for line in rawdata:
        print(i)
        print(line)
        output_file_path_and_name = "{0:03d}.txt".format(i)
        i += 1
        with open(output_file_path_and_name, "w", encoding="utf-8") as text_file:
            text_file.write(re.findall(r'"(.*?)"', line)[0])


if __name__ == "__main__":
    main()
