"""
Load a file named book.json at the current path
"""

import hashlib
import json
import os

from translate import translate_chunk, dutch_bot

BOOK_PATH = 'book.json'
CACHE_PATH = 'cache'

def load_book(path=BOOK_PATH):
  with open(BOOK_PATH) as f:
    book = json.load(f)
    return book

def store(chunk, result):
  obj = {
      "source": chunk,
      "result": result.result,
  }

  path = chunk_path(chunk)
  with open(path, 'w') as fp:
    print ('wrote', path)
    print (json.dumps(obj, indent=2))
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

def tx(chunk):
  cache_result = fetch(chunk)
  if cache_result:
    print (cache_result)
    return
  result = dutch_bot(chunk)
  store(chunk, result)

def main():
  book = load_book()
  render_data = []
  for title in book:
    chapter = book[title]
    tx = fetch(title)
    if tx is not None:
      render_data.append(tx)
    else:
      render-data.append({
        'source': chunk,
        'result': None
      })
    for chunk in chapter:
      tx = fetch(chunk) 
      if tx is not None:
        render_data.append(tx)
      else:
        render-data.append({
          'source': chunk,
          'result': None
        })
  return render_data

data = main()
print(json.dumps(data, indent=2))
