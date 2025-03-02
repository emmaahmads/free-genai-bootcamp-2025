# Creating a megaservice and the microservices (Homework)

## OPEA Comps
OPEA comps are the components that make up the OPEA ecosystem. These components are containerized microservices and can be orchestrated by a megaservice. A megaservice provides external endpoints.

## Microservices
[Source code](https://github.com/opea-project/GenAIComps/tree/main/comps/cores/mega)
1. A microservice instance provides an API Gateway to it's underlying services. The microservice instances are orchestrated following Directed Acyclic Graph (DAG) to construct a pipeline.
2. A microservice instance has an FastAPI HTTP server running. 

### High level setup of a microservice
Definitions for setting up the service [constants.py](https://github.com/opea-project/GenAIComps/blob/main/comps/cores/mega/constants.py)
1. If building the image, register the services using comps library.
2. Images can also be obtained from the Docker Hub. Define OPEA service(s) and the parameters in a Docker compose file. Define a volume to persist data if needed.

## Megaservices
[Source code](https://github.com/opea-project/GenAIComps/tree/main/comps/cores/mega)

### High level setup of a megaservice
In the same `Microservice` class, define the `service_role` as `ServiceRoleType.MEGASERVICE`
```python
self.endpoint = "/v1/example-service"
...
self.service = MicroService(
    self.__class__.__name__,
    service_role=ServiceRoleType.MEGASERVICE,
    host=self.host,
    port=self.port,
    endpoint=self.endpoint,
    input_datatype=ChatCompletionRequest,
    output_datatype=ChatCompletionResponse,
)
self.service.add_route(self.endpoint, self.handle_request, methods=["POST"])
self.service.start()
```

Define the Megaservice workflow using [ServiceOrchestrator](https://github.com/opea-project/GenAIComps/blob/main/comps/cores/mega/orchestrator.py)

## Lang Portal Frontend

So the frontend is built with Vue.js 3, which is pretty cool because it uses the Composition API for better code organization. The UI is super clean with a dashboard that shows study stats like streaks and success rates, plus a list of study activities you can jump into. They're using Vue Router for navigation between different views, and Axios for making API calls to the backend. The components are nicely organized with separate files for Dashboard, StudyActivities, QuickStats, and other UI elements. There's a slick grid layout for the dashboard with stat cards that show your progress at a glance. The study activities page has a neat card-based interface with pagination controls so you can browse through all your learning options. Everything's styled with scoped CSS so the styles don't leak between components. Overall, it's a modern, responsive frontend that makes language learning feel more like a fun app than a boring study tool.

## Vocab Importer Tool

The Vocab Importer is a Streamlit-based utility designed to rapidly generate Malay vocabulary content for the language learning platform. It leverages LLM capabilities through Ollama to create structured vocabulary data that can be imported into the main application. The implementation consists of several key components:

1. **Streamlit Interface**: A clean, user-friendly web interface where users can input vocabulary categories (like Food, Family, Colors) and select from different LLM models.

2. **Ollama Integration**: The tool connects to a locally-hosted Ollama service (containerized via Docker) to access various LLM models including llama3.1, llama3.2:1b, llama3:8b, and mistral.

3. **Prompt Engineering**: Carefully crafted prompts instruct the LLM to generate vocabulary words with proper Malay text, Jawi script transcription, and English translations in a structured JSON format.

4. **Robust JSON Parsing**: The implementation includes sophisticated error handling and JSON cleaning functions to deal with malformed LLM outputs, particularly focusing on issues with unescaped parentheses in translation values.

5. **Data Visualization**: Generated vocabulary is displayed in both tabular format for easy reading and raw JSON format for technical use.

6. **Export Functionality**: A one-click copy-to-clipboard feature allows users to easily export the generated JSON data for import into the main language portal.

7. **Containerization**: The Ollama service is containerized using Docker Compose, making deployment consistent across environments.

The tool addresses a critical technical challenge regarding the accuracy of Jawi script generation, noting that only the llama3-8b model produces reliable Jawi transcriptions, despite being slower on local hardware. This implementation serves as a temporary solution until a dedicated Jawi transcriptor service can be developed.