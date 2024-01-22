import json
import os
import textwrap
import time
import itertools
import sys
import argparse
from collections import defaultdict

from semantic_kernel import text

def get_chapters(path):

  chapters = defaultdict(list)
  chapter_titles = []
  current_chapter = None

  with open(path) as f:
    for index, line in enumerate(f):

      if line.startswith('Chapter '):
        current_chapter = line.strip()
      elif line.startswith('Prologue'):
        current_chapter = 'Prologue'

      # Line of content
      elif current_chapter:
        chapters[current_chapter].append(line)

      # Lines reached before the first chapter heading
      else:
        continue

  return chapters

# Set up argument parsing
parser = argparse.ArgumentParser(
    prog='prepare.py',
    description='Split markdown book into chapters'
    )

parser.add_argument('path')
args = parser.parse_args()

# Load Book Chapters
chapters = get_chapters(args.path)

# Split into pages of configurable size
chunked = {}
for title in chapters:
  lines = chapters[title]
  content = ''.join(lines)
  newlines = text.split_markdown_lines(content, 1000)

  # 500 tokens = roughly 1 page
  paras = text.split_markdown_paragraph(newlines, 500) 
  chunked[title] = paras

print(json.dumps(chunked, indent=2))
