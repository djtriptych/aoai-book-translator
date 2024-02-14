

# Instructions

1. Create a file named `.env` with the following keys.
AZURE_OPENAI_DEPLOYMENT_NAME=<deployment name>
AZURE_OPENAI_ENDPOINT=//<endpoint>.openai.azure.com/
AZURE_OPENAI_API_KEY=


1. First, activate your python environment.

  `source venv/bin/activate`

   And install any dependencies you might need from `requirements.txt`

1. Given a new book as a PDF, convert to markdown:

  `pandoc book.pdf -o book.md`

  This uses pandoc to create a markdown version of your book at `./book.md`.
  Pandoc also works with many other formats e.g. `.docx`.

2. This python / semantic kernel script splits markdown books first by chapters, 
   then by markdown chunks (approximately equivalent to pages). It will output a
   JSON representation of this book's content tree on STDOUT.

   `python prepare <book.md>`

   to store it as a known filename, redirect STDOUT to a file:

   `python prepare book.md > book.json`

  ```json
    {
      "Prologue": [
        'english chunk one [..]',
        'english chunk two [..]',
      ],
      "Chapter 1": [
        'english chunk one [..]',
        'english chunk two [..]',
      ]
    }
  ```

3. You're ready to run your translation at this point! The chunks in the JSON
   file represent the amount of source text we're sending to GPT-4 in a single
   API call. The size of the chunk is configurable, and I would experiment a
   bit. You are limited by the token limits of the particular model and version
   of GPT you're using.

   To run the translation we use the JSON representation of book and pass it to
   our restartable "runner":

   `python runner.py book.json`




## Installation of Python Environment.

Create environment
```
   python3 -m venv venv
```

Activate env
```
   source venv/bin/activate
```

Install packages
```
   pip install -r requirements.txt
```

