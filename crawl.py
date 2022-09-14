from genericpath import isfile
import requests
from bs4 import BeautifulSoup
import json
import time
import os
import argparse

parser = argparse.ArgumentParser(
    description='Given an input vocab list, this script would crawl corresponding information from an online dictionary and then output a json file.')
parser.add_argument('-i', '--input_path', type=str, required=True)
parser.add_argument('-o', '--output_path', type=str, default="vocabs/vocabs.json")
args = parser.parse_args()

assert args.input_path.endswith('txt')
assert os.path.exists(args.input_path)

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36'}
url = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{}'

with open(args.input_path, 'r') as f:
    vocabs = [vocab.strip().lower() for vocab in f.read().splitlines()]

existed_vocab_info = {}
if os.path.exists(args.output_path):
    with open(args.output_path, 'r') as f:
        existed_vocab_info = json.load(f)
vocab_info = existed_vocab_info

def is_vocab_existed(vocab, existed_vocab_info):
    try:
        existed_vocab_info[vocab]
        print('[Skip] Vocab "{}" info already exists.'.format(vocab))
        return True
    except:
        pass
    return False

fail_vocabs = []
for vocab in vocabs:
    if is_vocab_existed(vocab, vocab_info):
        continue

    try:
        res = requests.get(url.format(vocab), headers=headers)
        text = res.text
        soup = BeautifulSoup(text, 'lxml')

        # begin crawling
        entries = []
        for entry in soup.select('.entry-body__el'):
            if len(entry.select('.pos')) == 0:
                continue
            if len(entry.select('.gram')) == 0:
                pos = entry.select('.pos')[0].text
            else:
                pos = '{} {}'.format(entry.select(
                    '.pos')[0].text, entry.select('.gram')[0].text)
            pron = entry.select('.us')[0].select('.pron')[0].text

            entry_info = {}
            entry_info['pos'] = pos
            entry_info['pron'] = pron
            entry_info['blocks'] = []

            for block in entry.select('.def-block'):
                block_info = {}
                block_info['def'] = block.select('.def')[0].text
                block_info['trans'] = block.select('.trans')[0].text
                block_info['examples'] = []
                for example in block.select('.examp'):
                    block_info['examples'].append(example.text)
                entry_info['blocks'].append(block_info)
            entries.append(entry_info)

        if len(entries) == 0:
            raise Exception('Entry of "{}" is empty.'.format(vocab))

        vocab_info[vocab] = entries
        print('[Finish] crawling "{}"'.format(vocab))
        time.sleep(0.2)
    except Exception as e:
        print('[Fail] crawling "{}"'.format(vocab))
        print('==> ERROR Reason: {}'.format(e))
        fail_vocabs.append(vocab)

# check failure vocabs
print('\n----- fail crawling vocabs -----')
print('# of failure: {}'.format(len(fail_vocabs)))
for vocab in fail_vocabs:
    print(vocab)
if len(fail_vocabs):
    print('Pls add the info of failure vocabs manually.')

# output json with Chinese character
print('\n----- Output -----')
print('Output vocab info to {}'.format(args.output_path))
with open(args.output_path, "w", encoding="utf-8") as outfile:
    json.dump(vocab_info, outfile, indent=2, ensure_ascii=False)

# if __name__ == '__main__':