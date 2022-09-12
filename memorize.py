from curses.ascii import isdigit
import os
import argparse
import json

parser = argparse.ArgumentParser(
    description='Given an input vocab info json, this script would display English cards.')
parser.add_argument('-i', '--input_path', type=str, required=True)
args = parser.parse_args()

assert args.input_path.endswith('json')
assert os.path.exists(args.input_path)

with open(args.input_path, 'r') as f:
    vocab_info = json.load(f)

# sorting (TODO)

jump_idx = -1
for i, (vocab, info) in enumerate(vocab_info.items()):
    if i+1 < jump_idx:
        continue
    jump_idx = -1

    print('{}. {}'.format(i+1, vocab))

    for entry in info:
        print('\n##### {} {} ##### '.format(entry['pos'], entry['pron']))
        print('({} definitions for this pos)'.format(
            len(entry["blocks"])))

        for j, block in enumerate(entry["blocks"]):
            print('\n[definition {}]'.format(j+1))

            print(block['def'])
            print(block['trans'])

            print('\n# examples')
            for example in block['examples']:
                print('• {}'.format(example))

        print('-'*10)

    print('='*10)
    inp = input('Next move: (n/Number)')
    if inp.isdigit():
        jump_idx = int(inp)


# TODO
# sorting
# classify vocabs into [difficult, ,medium, easy]
