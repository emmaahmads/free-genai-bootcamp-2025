## OPEA Comps
OPEA comps are the components that make up the OPEA ecosystem. These components are containerized microservices and can be orchestrated by a megaservice.

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
The MegaService MicroService is defining external endpoints to interact with the Megaservice

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

Example from Exampro:

```python
self.megaservice = ServiceOrchestrator()
self.megaservice.add(guardrail_in).add(embedding).add(retriever).add(rerank).add(llm)
self.megaservice.flow_to(guardrail_in, embedding)
self.megaservice.flow_to(embedding, retriever)
self.megaservice.flow_to(retriever, rerank)
self.megaservice.flow_to(rerank, llm)
```

## Helper utilies (WIP)
