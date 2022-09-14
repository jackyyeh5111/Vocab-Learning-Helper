import os
import argparse
import json
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

VOCAB_LIST_DIR = "./vocab_lists"
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


def Heading(heading):
    print("\n-----------------------------------")
    print("\n        {}".format(heading))
    print("\n-----------------------------------")
    print("\nPress Enter to continue or Q to quit at any time")


def checkChoiceValidDigit(choice, start, end):
    if not choice.isdigit():
        print("Input has to be a digit ranging from {} to {}".format(start, end))
        return False
    if int(choice) < start or int(choice) > end:
        print("Input has to be a digit ranging from {} to {}".format(start, end))
        return False
    return True


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


def displayVocabInfo(vocab):
    try:
        print('synonym: {}'.format(global_synonym_info[vocab]))
    except:
        pass
    try:
        print('antonym: {}'.format(global_antonym_info[vocab]))
    except:
        pass

    try:
        for entry in global_dict[vocab]:
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
    except:
        print('Cannot find "{}" is the dictionary.'.format(vocab))

    inp = input('Press any key to continue')
    print('='*40)


def getVocabList():
    vocab_files = []
    while True:
        print('\n\nAvailable vocabulary lists ==>')
        idx = 1
        for file in os.listdir(VOCAB_LIST_DIR):
            if file.endswith('txt'):
                print("{}. {}".format(idx, file))
                idx += 1
                vocab_files.append(file)

        choice = input(
            '\n\nPlease choose a vocabulary list you want to learn: ')

        if checkChoiceValidDigit(choice, 1, idx-1):
            break

    vocab_path = os.path.join(VOCAB_LIST_DIR,  vocab_files[int(choice)-1])
    with open(vocab_path, 'r') as f:
        vocab_list = [vocab.strip().lower() for vocab in f.read().splitlines()]

    return vocab_list


def interactiveLearn():
    '''
    1. Randomly choose words from the mentioned list
    2. Choose words in a serial order from the mentioned list
    '''
    ClearOutput()
    vocab_list = getVocabList()

    input('\nEnjoy learning vocabularies! (Press any key to continue)')
    ClearOutput()
    for i, vocab in enumerate(vocab_list):
        print ('\n\n')
        print ('-'*50)
        print('\n{}. {}\n'.format(i+1, vocab))
        print ('-'*50)
        displayVocabInfo(vocab)


def searchInVocabulary(vocab=None):
    ClearOutput()
    Heading("Search In Vocabulary")
    while True:
        if vocab is None:
            word_to_search = str(
                input("\nEnter the word to search: ")).lower()
        else:
            word_to_search = vocab.lower()
        if word_to_search == 'q':
            break
        displayVocabInfo(word_to_search)

    ClearOutput()
    return


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
            if choice == 2:
                searchInVocabulary()


if __name__ == '__main__':
    main()
