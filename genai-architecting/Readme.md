## Functional Requirements

The company wants to use self-hosted Generative AI models for their TokiPona learning platform as they are concerned about privacy and the costs of managed services.
Most LLMs have challenges in teaching TokiPona due to the limitations of the language and the lack of trainings in the language. 

The company wishes to standardize TokiPona lessons and contents with enforcement on it's simplicity in practice.

The company has about 50 students all from the South East Asia region.

## Assumptions

Hosting an LLM on the cloud server

## Data Strategy


## Considerations

We're considering using agent and RAG, to restrict the sentence format to TokiPona standards with context, and to transcribe the sentence into TokiPona. We're also going to keep a local dictionary of the vocabularies. We're most likely won't be needing the model (RAG) to connect to the internet.