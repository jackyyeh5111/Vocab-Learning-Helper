import requests
from bs4 import BeautifulSoup
import json
import time

OUTPUT_PATH = "vocab_info.json"
INPUT_PATH = 'vocabs.txt'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36'}
url = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{}'

with open(INPUT_PATH, 'r') as f:
    vocabs = [vocab.strip() for vocab in f.read().splitlines()]

vocab_info = {}
fail_vocabs = []
for vocab in vocabs:
    try:
        res = requests.get(url.format(vocab), headers=headers)
        text = res.text
        soup = BeautifulSoup(text, 'lxml')
            
        # begin crawling
        entries = []
        for entry in soup.select('.entry-body__el'):
            entry_info = {}
            if len(entry.select('.pos')) == 0:
                continue
            if len(entry.select('.gram')) == 0:
                pos = entry.select('.pos')[0].text
            else:
                pos = '{} {}'.format(entry.select('.pos')[0].text, entry.select('.gram')[0].text)
            entry_info['pos'] = pos
            
            entry_info['pron'] = entry.select('.us')[0].select('.pron')[0].text
            for block in entry.select('.def-block'):
                entry_info['def'] = entry.select('.def')[0].text
                entry_info['trans'] = entry.select('.trans')[0].text
                for example in block.select('.examp'):
                    entry_info['examp'] = example.text
            entries.append(entry_info)
            
        if len(entries) == 0:
            raise Exception('Entry of "{}" is empty.'.format(vocab))
            
        vocab_info[vocab] = entries
        print ('Finish crawling "{}"'.format(vocab))
        time.sleep(0.5)
    except Exception as e:
        print ('Fail crawling "{}"'.format(vocab))
        print ('==> ERROR Reason: {}'.format(e))
        fail_vocabs.append(vocab)
    
# check failure vocabs
print ('\n----- fail crawling vocabs -----') 
print ('# of failure: {}'.format(len(fail_vocabs))) 
for vocab in fail_vocabs:
    print (vocab)   
print ('Pls add the info of failure vocabs manually.') 

# output json with Chinese charanter
print ('\n----- Output -----')
print ('Output vocab info to {}'.format(OUTPUT_PATH)) 
with open(OUTPUT_PATH, "w", encoding="utf-8") as outfile:
    json.dump(vocab_info, outfile, indent=2, ensure_ascii=False)
