from curses.ascii import isdigit
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
import pathlib
from pytz import timezone
import calendar
import time
import csv
import plotext as plt
from tabulate import tabulate
from bs4 import BeautifulSoup

cur_path = pathlib.Path(__file__).parent.absolute()

VOCAB_LIST_DIR = os.path.join(cur_path, "./vocab_lists")
SYN_ANT_PATH = os.path.join(cur_path, "./db/syn_ant.json")
CAMBRIDGE_DICTIONARY_PATH = os.path.join(cur_path, "./db/cambridge_dict.json")
VOCABCOM_DICTIONARY_PATH = os.path.join(cur_path, "./db/vocabcom_dict.json")


try:
    with open(CAMBRIDGE_DICTIONARY_PATH, 'r') as f:
        global_cambridge_dict = json.load(f)
except Exception as e:
    print("\n[ERROR] Fail to load {}. Reason: {}".format(CAMBRIDGE_DICTIONARY_PATH, e))
    exit(1)
try:
    with open(VOCABCOM_DICTIONARY_PATH, 'r') as f:
        global_vocabcom_dict = json.load(f)
except Exception as e:
    print("\n[ERROR] Fail to load {}. Reason: {}".format(VOCABCOM_DICTIONARY_PATH, e))
    exit(1)
    

def processSynonymAndAntonym():
    with open(SYN_ANT_PATH, 'r') as f:
        syn_ant_info = json.load(f)

    for synonyms in syn_ant_info["synonyms"]:
        for word in synonyms:
            global_synonym_info[word] = synonyms
    for antonyms in syn_ant_info["antonyms"]:
        for word in antonyms:
            global_antonym_info[word] = antonyms

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
    print("3. Edit a word")
    print("10. Exit")
    print("------------------------------------")


def displayVocabInfo(vocab):
    try:
        print('short explanation: \n\n{}'.format(global_vocabcom_dict[vocab]["short"]))
        print('\nlong explanation: \n\n{}'.format(global_vocabcom_dict[vocab]["long"]))
    except:
        pass
    try:
        print('\nsynonym: {}'.format(global_synonym_info[vocab]))
    except:
        pass
    try:
        print('antonym: {}'.format(global_antonym_info[vocab]))
    except:
        pass
    
    inp = input('\nPress any key to continue')
    
    try:
        for entry in global_cambridge_dict[vocab]:
            print('\n##### {} {} ##### '.format(entry['pos'], entry['pron']))
            if 'note' in entry.keys():
                print ('Note: {}\n'.format(entry['note']))
                
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
        print('Cannot find "{}" in the dictionary.'.format(vocab))

    inp = input('\nPress any key to continue')
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
    while True:
        start_id = input(
            '\nInput a vocabulary id you want to start with (input 1 to start from the beginning):')
        if not start_id.isdigit():
            print("\nInvalid choice! Enter a number less than or equal to {}".format(
                (len(vocab_list))))
            continue
        start_id = int(start_id)
        break

    input('\nEnjoy learning vocabularies! (Press any key to continue)')
    ClearOutput()
    for i, vocab in enumerate(vocab_list):
        if i+1 < start_id:
            continue
        print('\n\n')
        print('-'*50)
        print('\n{}. {}\n'.format(i+1, vocab))
        print('-'*50)
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


def editVocabulary():
    pass


def addVocabulary(word):
    pos = input("Pos: ")
    pron = input("Pronunciation: ")
    definition = input("Definition: ")
    trans = input("Transition: ")
    example = input("Example: ")

    block_info = {
        "def": definition,
        "trans": trans,
        "examples": [example]
    }
    info = {
        "pos": pos,
        "pron": pron,
        "blocks": [block_info]
    }
    global_cambridge_dict[word] = [info]

    with open(DICTIONARY_PATH, "w", encoding="utf-8") as outfile:
        json.dump(global_cambridge_dict, outfile, indent=2, ensure_ascii=False)


def updateDictionary():
    ClearOutput()
    Heading("Add/Edit a vocabulary")
    while True:
        word = str(
            input("\nEnter the word to add/edit: ")).lower()
        if word == 'q':
            break
        try:
            global_cambridge_dict[word]
            editVocabulary()
        except:
            addVocabulary(word)


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
            if choice == 3:
                updateDictionary()


if __name__ == '__main__':
    main()
