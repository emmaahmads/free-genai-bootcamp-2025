# Vocab Importer

## Overview
We need to quickly populate the application with word and word groups so students can begin testing the system. We will use an LLM to generate words based on a prompt and then save the words to JSON. The JSON can then be imported into the application.

## Requirements
- The word must be categorized as a `noun`, `verb`, `adjective`, `adverb` or `preposition`
- The word must have the Jawi transcription
- The word must have the English translation
- The word must have a word group (food, color, etc)
- We will use the [Jawi API](https://jawi.dev/) to generate the Jawi transcription 
- For fast prototyping, we will use Streamlit

## Features


