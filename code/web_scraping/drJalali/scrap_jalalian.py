#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import os


def getGhazal(url):
    try:
        html = urlopen(url, timeout=60)
        # print(html.read()
    except HTTPError as e:
        print(e)
        return None, None

    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        # print(bsObj.h1)
        # r"غزل شماره .*[۰۱۲۳۴۵۶۷۸۹]"
        ghazal_number = unidecode(re.search(r"[۰۱۲۳۴۵۶۷۸۹]+", str(bsObj.h1)).group(0))
        raw_hemistichs = bsObj.find_all("table")
        for raw_hemistich in raw_hemistichs:
            # print(repr(raw_hemistich.get_text()))
            gazal = re.sub(r"[۰۱۲۳۴۵۶۷۸۹]+\-", "", raw_hemistich.get_text())
            gazal = re.sub(r"\n\n\n\n", "\n", gazal)
            gazal = gazal.strip()
            # print(gazal)

    except AttributeError as e:
        print(e)
        return None, None

    return ghazal_number, gazal


# url = "https://ganjoor.net/hafez/ghazal/sh1/"


def main():
    for i in range(18665, 19928):
        print("---------------------------------------------------")
        print(i)
        url = "http://dr-jalalian.ir/?p={}".format(i)
        ghazal_number, gazal = getGhazal(url)
        if ghazal_number and gazal:
            print(ghazal_number)
            print(repr(gazal))
            print(gazal)
            output_file_path_and_name = output_file_path + "/{0:03d}.txt".format(
                int(ghazal_number)
            )
            with open(output_file_path_and_name, "w", encoding="utf-8") as text_file:
                text_file.write(gazal)


if __name__ == "__main__":
    output_file_path = os.path.dirname(os.path.realpath(__file__)) + "/dr-jalalian"
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)

    main()
