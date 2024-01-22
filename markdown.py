"""
Load a file named book.json at the current path
"""

import argparse
import hashlib
import json
import os
import markdown2

from translate import translate_chunk, dutch_bot

CACHE_PATH = 'cache'

def load_book(path):
  with open(path) as f:
    book = json.load(f)
    return book

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


def render_markdown(path):
  book = load_book(path)
  render_data = []
  for title in book:
    chapter = book[title]
    tx = fetch(title)
    if tx is not None:
      render_data.append('\n\n## ' + tx['result'] + "\n\n")
    else:
      render_data.append('\n...untranslated...\n')
    for chunk in chapter:
      tx = fetch(chunk) 
      # render_data.append(chunk_path(chunk))
      if tx is not None:
        render_data.append(tx['result'])
      else:
        render_data.append('\n...untranslated...\n')
        render_data.append('\n...'+ chunk[:70] + '\n')
  return '\n'.join(render_data)


# Set up argument parsing
parser = argparse.ArgumentParser(
    prog='prepare.py',
    description='Split book into chapters'
    )

parser.add_argument('path')
args = parser.parse_args()


DEFAULT_STYLE = '''

<style>

  body {
    font-family: Calibri, times new roman;
    font-size: 24pt;
  }

  h2 {
    text-align: center;
    margin: 10em 0 2em;
  }

  #frame {
    background-color: white;
    width: 30em;
    margin: 50px auto;
    padding: 1em;
  }

  table {
    font-size: 60%;
    table-layout: fixed;
    border-collapse: collapse;
    width: 100%;
    font-family: arial, sans-serif;
    margin-bottom: 15em;
  }

  th { 
    width: 30%; 
    text-align: left; 
    vertical-align: top;
    padding-top: 6px;
    color: black;
    font-weight: normal;
  }

  td { 
    padding: 6px;
    width: 70% 
  }
  tr {
       border-bottom: 1px solid #ccc;
  }

  ol {
    margin: 1em 0;
    padding: 0;
  }

  li {
    margin-bottom: 1em;
  }

  p {
    margin: 0;
    padding: 0;
    text-indent: 2em;
  }

</style>'''

running_stats = {
  'title': 'De Tijd Dringt',
  'author': '',
  'time_to_generate': '~ 20 minutes',
  'model': 'GPT-4 (128k) on Azure Open AI',
  'cost': '~ $2',
  'process': '',
}

cause_stats = {
  'title': 'Reden tot Ongerustheid',
  'author': 'Amanda Stevens',
  'time_to_generate': '~ 2 hours',
  'model': 'GPT-4 (128k) on Azure Open AI',
  'cost': '~ $3',
  'process': '',
}


def make_html(md, stats):

  html = (f'''

  {DEFAULT_STYLE}

  <div id="frame">
    <table id="stats">
      <tr>
        <th> Time to generate </th>
        <td> {stats['time_to_generate']} </td>
      </tr>
      <tr>
        <th> Model </th>
        <td> {stats['model']} </td>
      </tr>
      <tr>
        <th> Word Count (approx.)</th>
        <td> {len(md.split())} </td>
      </tr>
      <tr>
        <th> Cost </th>
        <td> {stats['cost']} </td>
      </tr>
      <tr>
        <th> Process </th>
        <td> 
        <ol>
          <li>Convert source PDF to <a href="https://en.wikipedia.org/wiki/Markdown">markdown</a>, using <a href="https://pandoc.org/"><code>pandoc</code></a>. Pandoc
          will make a best effort to retain styling information from PDF source in
          output markdown.</li>
          <li>Split markdown document by chapter (custom Python script).</li>
          <li>Chunk markdown chapters into ~1000 token chunks. (custom Python / <a href="https://github.com/microsoft/semantic-kernel">semantic
          kernel</a>).</li>
          <li>Provide each chunk to GPT-4, with a system prompt instructing GPT-4 to
          convert from English to Dutch, while retaining markdown styling information.</li>
          <li>Store translated chunks in on-disk cache, allowing restarts, interactive
          debugging, inspection of in-process translations, etc.</li>
          <li>Render stored/cached chunks back into Dutch markdown document representing
          the full book.</li>
          <li>Render markdown to HTML, with custom CSS to render output.</li>
          <li>Print HTML to PDF (via web browser).</li>
          </ol>
        </td>
      </tr>
    </table>

    <h1> {stats['title']} </h1>
    <h4> {stats['author']}</h4>
  ''' 
  + markdown2.markdown(md) + 
  '''
  </div>

  ''')

  return html


md = render_markdown(args.path)
doc = make_html(md, running_stats)
# doc = make_html(md, cause_stats)

print(doc)


