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
- We will use OPEA comps, LLM and TGI microservices

## Workflows

### Word generation
1. User inputs a prompt for word group
2. LLM generates 50 words based on the prompt in JSON format
3. JSON is saved to file
4. JSON is imported into the application

## OPEA Comps resources
- [llms/deployment/docker_compose/compose_text-generation.yaml](https://github.com/opea-project/GenAIComps/blob/main/comps/llms/deployment/docker_compose/compose_text-generation.yaml)
- [third_parties/tgi/deployment/docker_compose/compose.yaml](https://github.com/opea-project/GenAIComps/blob/main/comps/third_parties/tgi/deployment/docker_compose/compose.yaml)
https://github.com/huggingface/text-generation-inference
https://huggingface.co/docs/text-generation-inference/en/messages_api





