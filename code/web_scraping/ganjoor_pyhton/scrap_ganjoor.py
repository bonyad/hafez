#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import os
from concurrent.futures import ThreadPoolExecutor

ganjoor_page = "https://ganjoor.net/hafez/ghazal/"


def getPoemsUrl(url):
    try:
        html = urlopen(url, timeout=60)
        # print(html.read())
    except HTTPError as e:
        print(e)
        return None

    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        links = []
        for link in bsObj.find_all(
            "a", attrs={"href": re.compile("^" + ganjoor_page + "sh")}
        ):
            # print(link.get('href'))
            links.append(link.get("href"))
        # print('\n'.join(links))
    except AttributeError as e:
        print(e)
        return None

    return links


def getPoem(url):
    try:
        html = urlopen(url, timeout=60)
        # print(html.read())
    except HTTPError as e:
        print(e)
        return None

    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        poem = []
        for raw_mesra in bsObj.findAll("div", {"class": "b"}):
            # print((raw_mesra))
            raw_mesra = str(raw_mesra)
            for nlChar in ["\n", "\r\n", "\r"]:
                if nlChar in raw_mesra:
                    raw_mesra = raw_mesra.replace(nlChar, "")
            re_mesra = re.compile(
                r'<div class="b"><div class="m1"><p>(.*)</p></div><div class="m2"><p>(.*)</p></div></div>'
            )
            mesra = re_mesra.findall(raw_mesra)
            # print(mesra)
            poem.append(mesra[0][0] + "\n")
            poem.append(mesra[0][1] + "\n\n")
            # print("--------------------------")

    except AttributeError as e:
        print(e)
        return None

    return "".join(poem)


def savePoem(url):
    # print(url)
    poem = getPoem(url).rstrip()
    # print(poem)
    poem_number = int(re.findall(r"sh(\d+)", url)[0])
    # print("poem number= {}".format(poem_number))
    output_file_path_and_name = output_file_path + "/{0:03d}.txt".format(poem_number)
    # print("Save to " + output_file_path_and_name)
    with open(output_file_path_and_name, "w", encoding="utf-8") as text_file:
        text_file.write(poem)
    print("poem number= {0:03d} saved!".format(poem_number))


def main():
    print("Get Poems URL ...")
    poems_url = getPoemsUrl(ganjoor_page)
    print("\n".join(poems_url))

    print("\nGet and save Poems ...")
    t = ThreadPoolExecutor(max_workers=50)
    t.map(savePoem, poems_url)
    t.shutdown()

    print("Done!")


if __name__ == "__main__":
    output_file_path = os.path.dirname(os.path.realpath(__file__)) + "/data"
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)

    main()
