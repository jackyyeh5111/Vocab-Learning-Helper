from curses.ascii import isdigit
import os
import argparse
import json
from typing import List
import requests
import random
import json
import sys
import os
import platform
import datetime
from pathlib import Path
from pytz import timezone
import calendar
import time
import csv
import plotext as plt
from tabulate import tabulate
from bs4 import BeautifulSoup

SYN_ANT_PATH = "./syn_ant.json"
DICTIONARY_PATH = "./dict.json"


def processSynonymAndAntonym():
    with open(SYN_ANT_PATH, 'r') as f:
        syn_ant_info = json.load(f)

    for synonyms in syn_ant_info["synonyms"]:
        for word in synonyms:
            global_synonym_info[word] = synonyms
    for antonyms in syn_ant_info["antonyms"]:
        for word in antonyms:
            global_antonym_info[word] = antonyms


try:
    with open(DICTIONARY_PATH, 'r') as f:
        global_dict = json.load(f)
except:
    print("\n[ERROR] Unable to find {} file. Please check the path again".format(
        DICTIONARY_PATH))
    exit(1)

global_synonym_info = {}
global_antonym_info = {}
processSynonymAndAntonym()


def ClearOutput():
    MyOS = platform.system()
    if MyOS == "Windows":
        os.system("cls")
    elif MyOS == "Darwin":
        os.system("clear")
    elif MyOS == "Linux":
        os.system("clear")
    else:
        print("\nUnknown OS ☠️ Please check ClearOutput() function in Main.py")


def PrintMenu():
    print("------------------------------------")
    print("Please enter a number: ")
    print("1. Start to learn")
    print("2. Search for a word")
    print("10. Exit")
    print("------------------------------------")


def interactiveLearn():
    '''
    1. Randomly choose words from the mentioned list
    2. Choose words in a serial order from the mentioned list
    '''
    ClearOutput()

    for i, (vocab, info) in enumerate(global_dict.items()):
        print('\n\n{}. {}'.format(i+1, vocab))
        try:
            print('synonym: {}'.format(global_synonym_info[vocab]))
        except:
            pass
        try:
            print('antonym: {}'.format(global_antonym_info[vocab]))
        except:
            pass

        for entry in info:
            print('\n##### {} {} ##### '.format(entry['pos'], entry['pron']))
            print('({} definitions for this pos)'.format(
                len(entry["blocks"])))

            for j, block in enumerate(entry["blocks"]):
                print('\n[definition {}]'.format(j+1))

                print(block['def'])
                print(block['trans'])

                if len(block['examples']):
                    print('\n# examples')
                    for example in block['examples']:
                        print('• {}'.format(example))
                else:
                    print('\n# No examples')

        inp = input('Press any key to continue')
        print('='*40)


def main():
    ClearOutput()
    print("\nWelcome to the GRE World!")
    while(True):
        print("\nTell us what would you like to do")
        print()
        PrintMenu()
        choice = input("\nEnter your choice: ")
        if choice.isnumeric():
            choice = int(choice)
            if choice == 1:
                interactiveLearn()

if __name__=='__main__':
    main()
