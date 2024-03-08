from dotenv import load_dotenv
from openai import AzureOpenAI
import os

MAX_TOKENS = 4000

load_dotenv()

deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
api_key = os.getenv('AZURE_OPENAI_API_KEY')
api_version = os.getenv('AZURE_OPENAI_VERSION')

def make_client():
  return AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
  )

client=make_client()

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

def simple_response(oai_response):
  return oai_response.choices[0].message.content

def translate(source_language, target_language, text):
  sys_prompt = make_translation_sys_prompt(source_language, target_language)
  
  response = client.chat.completions.create(
    model=deployment_name, 
    messages=[
      {'role': 'system', 'content': sys_prompt},
      {'role': 'user', 'content': text}
    ],
    max_tokens=MAX_TOKENS
  )

  return simple_response(response)
