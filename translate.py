"""

  Temperature notes
  on semantic kernel
  rate limiting
  pricing / estimation
  content exception important
  producing structured parallel translations
  Next:
    - translation with context window
    - translate with summaries
    - with author notes
"""

import os
import textwrap
import time
import itertools
import sys
from collections import defaultdict

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from semantic_kernel import (
    ChatPromptTemplate,
    SemanticFunctionConfig,
    PromptTemplateConfig,
)

def create_semantic_function_chat_config(prompt_template, prompt_config_dict, kernel):
    chat_system_message = (
        prompt_config_dict.pop("system_prompt")
        if "system_prompt" in prompt_config_dict
        else None
    )

    prompt_template_config = PromptTemplateConfig.from_dict(prompt_config_dict)
    prompt_template_config.completion.token_selection_biases = (
        {}
    )  # required for https://github.com/microsoft/semantic-kernel/issues/2564

    prompt_template = ChatPromptTemplate(
        template=prompt_template,
        prompt_config=prompt_template_config,
        template_engine=kernel.prompt_template_engine,
    )

    if chat_system_message is not None:
        prompt_template.add_system_message(chat_system_message)

    return SemanticFunctionConfig(prompt_template_config, prompt_template)



kernel = sk.Kernel()
deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
# print (deployment, api_key, endpoint)

kernel.add_chat_service("chat_completion", 
  AzureChatCompletion(
    deployment_name=deployment, 
    endpoint=endpoint, 
    api_key=api_key)
)

TRANSLATE_PARAGRAPH_PROMPT = """
You are an AI assistant to help editors translate books from English to Dutch.

- Take the markdown input you receive and output ONLY the Dutch translation.
- Match content and tone as closely as possible.
- Match markdown formatting as closely as possible.
- Where possible, use common Dutch idioms in place of English idioms, such as
  "buiten het net" or "van het net af" for the english "off the grid".
"""

dad_joke = kernel.create_semantic_function(
  "You are a bot that tells dad jokes ",
  max_tokens=4000, 
  temperature=0.1, 
  top_p=0.5
)

chat_config_dict = {
  "schema": 1,
  # The type of prompt
  "type": "completion",
  # A description of what the semantic function does
  "description": "A chatbot which translates from english to dutch",
  # Specifies which model service(s) to use
  "default_services": ["azure_gpt4_chat_completion"],
  # The parameters that will be passed to the connector and model service
  "completion": {
      "temperature": 0.0,
      "top_p": 1,
      "max_tokens": 4000,
      "number_of_responses": 1,
      "presence_penalty": 0,
      "frequency_penalty": 0,
  },
  # Defines the variables that are used inside of the prompt
  "input": {
      "parameters": [
          {
              "name": "input",
              "description": "The input given by the user",
              "defaultValue": "",
          },
      ]
  },

  # Non-schema variable
  "system_prompt": TRANSLATE_PARAGRAPH_PROMPT,
}


dutch_bot = kernel.register_semantic_function(
    skill_name="TranslationBot",
    function_name="translate_bot",
    function_config=create_semantic_function_chat_config(
        "{{$input}}", chat_config_dict, kernel
    ),
)



translate_chunk = kernel.create_semantic_function(
  TRANSLATE_PARAGRAPH_PROMPT,
  max_tokens=4000, 
  temperature=0.0, 
  top_p=0.5
)

def get_chapters(path):

  chapters = defaultdict(list)
  chapter_titles = []
  current_chapter = None

  with open(path) as f:
    for index, line in enumerate(f):

      if line.startswith('Chapter '):
        current_chapter = line.split(' ')[-1].strip()
      elif line.startswith('Prologue'):
        current_chapter = 'Prologue'

      # Line of content
      elif current_chapter:
        chapters[current_chapter].append(line)

      # Lines reached before the first chapter heading
      else:
        continue

  return chapters

def book_stats(chapters):
  for chapter_name in chapters:
    print(chapter_name)
    lines = chapters[chapter_name]
    text = '\n'.join(lines)
    print('\t', len(lines), 'lines.')
    print('\t', len(text), 'characters.')

def print_zipped(zipped):
  for source, translation in zipped:
      print (source, '  |  ', translation)

def translate_paragraphs(chapters, chapter_name):
  chapter = chapters[chapter_name]
  print ("Translating Chapter:", chapter_name)
  for paragraph in chapter:
    if not paragraph.strip(): 
      continue
    wrapped_paragraph = textwrap.fill(paragraph)
    translated = translate_chunk(wrapped_paragraph)

    wrapped_translated = textwrap.fill(str(translated))

    zipped = list(itertools.zip_longest(
        textwrap.wrap(str(paragraph).strip()),
        textwrap.wrap(str(translated).strip()),
        fillvalue=''
    ))

    for source, translation in zipped:
      print (source.ljust(70), '  |  ', translation.ljust(70))

    print ('-' * 145)
    time.sleep(2)

def translate_chapter(chapters, chapter_name):
  chapter = chapters[chapter_name]
  print ("Translating Chapter:", chapter_name)
  lines = chapters[chapter_name]
  text = ''.join(lines)

  translated = translate(text)

  print (translated)

  return

  wrapped_translated = textwrap.fill(str(translated))

  zipped = list(itertools.zip_longest(
      textwrap.wrap(str(text).strip()),
      textwrap.wrap(str(translated).strip()),
      fillvalue=''
  ))

  for source, translation in zipped:
    print (source.ljust(70), '  |  ', translation.ljust(70))

  print ('-' * 145)
  time.sleep(2)
