
"""
Load a file named book.json at the current path
"""


import argparse
import hashlib
import json
import os

from translate import translate_chunk, dutch_bot

CACHE_PATH = 'cache'

def load_book(path):
  with open(path) as f:
    book = json.load(f)
    return book

def main(path):
  book = load_book(path)
  chunks = 0
  try:
    print('Chapters')
    for title in book:
      chapter = book[title]
      print('  - ', title)
      for chunk in chapter:
        chunks += 1
  except KeyboardInterrupt:
    return
  print (chunks, ' chunks')

# Set up argument parsing
parser = argparse.ArgumentParser(
    prog='runner.py',
    description='Split book into chapters'
    )

parser.add_argument('path')
args = parser.parse_args()

main(args.path)
