"""
Load a file named book.json at the current path
"""


import argparse
import hashlib
import json
import os
import time

from translate import dutch_bot

CACHE_PATH = 'cache'

# Time to pause between requests to AOAI to avoid rate limiting.
PAUSE_SECONDS = 5

def load_book(path):
  with open(path) as f:
    book = json.load(f)
    return book

def store(chunk, result):
  obj = {
      "source": chunk,
      "result": result.result,
  }

  path = chunk_path(chunk)
  with open(path, 'w') as fp:
    print ('cache: ', path)
    json.dump(obj, fp)

def chunk_path(chunk):
  hash = hashlib.md5(chunk.encode('utf8')).hexdigest()
  path = os.path.join(CACHE_PATH, f'{hash}.json')
  return path

def fetch(chunk):
  path = chunk_path(chunk)
  if not os.path.exists(path):
    return None
  with open(path) as fp:
    return json.load(fp)

def fprint(chunk, length=50):
  print ("  source:", ' '.join(chunk['source'][:length].split()))
  print ("  result:", ' '.join(chunk['result'][:length].split()))

def tx(chunk):
  cache_result = fetch(chunk)
  if cache_result:
    fprint (cache_result)
    return
  result = dutch_bot(chunk)
  time.sleep(PAUSE_SECONDS)
  store(chunk, result)

def main(path):
  book = load_book(path)
  try:
    for title in book:
      chapter = book[title]
      print(title)
      tx(title)
      for chunk in chapter:
        tx(chunk)

  except KeyboardInterrupt:
    print('Caught interrupt')
    return

# Set up argument parsing
parser = argparse.ArgumentParser(
    prog='runner.py',
    description='Split book into chapters'
    )

parser.add_argument('path')
args = parser.parse_args()

main(args.path)
