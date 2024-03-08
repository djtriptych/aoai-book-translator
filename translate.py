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

import asyncio
import os
import textwrap
import itertools
import sys
from collections import defaultdict

import semantic_kernel as sk
from semantic_kernel import (
    ChatPromptTemplate,
    SemanticFunctionConfig,
    PromptTemplateConfig,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

kernel = sk.Kernel()
deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()

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


kernel.add_chat_service("chat_completion", 
  AzureChatCompletion(
    deployment_name=deployment, 
    endpoint=endpoint, 
    api_key=api_key)
)

# This is the "system prompt" used to instruct the LLM.
# To change to a difference source or target language, amend the prompt
# below.
TRANSLATE_PARAGRAPH_PROMPT = """
You are an AI assistant to help editors translate books from English to Swedish.

- Take the markdown input you receive and output ONLY the Swedish translation.
- Match content and tone as closely as possible.
- Match markdown formatting as closely as possible.
"""

def make_translation_sys_prompt(source_language, target_language):
  source = source_language.title()
  target = target_language.title()
  return f"""
  You are an AI assistant to help editors translate books from {source} to
  {target}.

  RULES:
  - Take the markdown input you receive and output ONLY the {target} language translation.
  - Match content and tone as closely as possible.
  - Match markdown formatting as closely as possible.
  """

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

def make_translate_bot(source, target):

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
    "system_prompt": make_translation_sys_prompt(source, target)
  }

  async def translator(text):

    print (source, target)
    bot = kernel.create_semantic_function(
        function_config=create_semantic_function_chat_config(
            "{{$input}}", chat_config_dict, kernel
        ),
    )

    return await kernel.run_async(bot, input_str=text)

  return translator

async def main(source, target):
  bot = make_translate_bot(source, target)
  answer = await bot('goodbye')
  print(answer)
  answer = await bot('hi there!')
  print(answer)

if __name__ == '__main__':
  help(kernel)
  asyncio.run(main('english','spanish'))
