import requests
from bs4 import BeautifulSoup
import json
import time
import os
import argparse
import pathlib

parser = argparse.ArgumentParser(
    description='Given an input vocab list, this script would crawl corresponding information from an online dictionary and then output a json file.')
parser.add_argument('-i', '--input_path', type=str, required=True)
parser.add_argument('-o', '--output_path', type=str, default="./db/vocabcom_dict.json")
args = parser.parse_args()

assert args.input_path.endswith('txt')
assert os.path.exists(args.input_path)

cur_path = pathlib.Path(__file__).parent.absolute()
args.output_path = os.path.join(cur_path, args.output_path)

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36'}
url = 'https://www.vocabulary.com/dictionary/{}'

with open(args.input_path, 'r') as f:
    vocabs = [vocab.strip().lower() for vocab in f.read().splitlines()]

existed_vocab_info = {}
if os.path.exists(args.output_path):
    with open(args.output_path, 'r') as f:
        existed_vocab_info = json.load(f)
vocab_info = existed_vocab_info

def is_vocab_existed(vocab, existed_vocab_info):
    try:
        if existed_vocab_info[vocab]:
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
        short = soup.select_one('.short').text
        long = soup.select_one('.long').text

        vocab_info[vocab] = {
            "short": short,
            "long": long
        }    
        print('[Finish] crawling "{}"'.format(vocab))
        time.sleep(0.1)
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