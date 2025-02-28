```sh
CONTAINER ID   IMAGE                                   COMMAND                  CREATED         STATUS                   PORTS                                                                                                                                                                                 NAMES
f50f567b4e33   jaegertracing/all-in-one:latest         "/go/bin/all-in-one-…"   2 minutes ago   Up 2 minutes             0.0.0.0:4317-4318->4317-4318/tcp, [::]:4317-4318->4317-4318/tcp, 14250/tcp, 0.0.0.0:9411->9411/tcp, [::]:9411->9411/tcp, 0.0.0.0:16686->16686/tcp, [::]:16686->16686/tcp, 14268/tcp   jaeger
e203d646018a   opea/retriever:latest                   "python opea_retriev…"   9 minutes ago   Up 1 second              0.0.0.0:7000->7000/tcp, [::]:7000->7000/tcp                                                                                                                                           retriever-pgvector
692abd88b6cf   opea/embedding:latest                   "sh -c 'python $( [ …"   9 minutes ago   Up 8 minutes             0.0.0.0:10203->6000/tcp, [::]:10203->6000/tcp                                                                                                                                         clip-embedding-server
5691ed97dfb4   opea/embedding-multimodal-clip:latest   "python clip_server.…"   9 minutes ago   Up 9 minutes (healthy)   0.0.0.0:6990->6990/tcp, [::]:6990->6990/tcp                                                                                                                                           multimodal-clip-embedding-server
94587ce55800   opea/guardrails-bias-detection:latest   "python opea_bias_de…"   9 minutes ago   Up 9 minutes             0.0.0.0:9092->9092/tcp, [::]:9092->9092/tcp                                                                                                                                           guardrails-bias-detection-server
3e96c10b1c06   pgvector/pgvector:0.7.0-pg16            "docker-entrypoint.s…"   9 minutes ago   Up 9 minutes (healthy)   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp                                                                                                                                           pgvector-db
13490fec00a7   ollama/ollama                           "/bin/ollama serve"      9 minutes ago   Up 9 minutes             0.0.0.0:8008->11434/tcp, [::]:8008->11434/tcp                                                                                                                                         ollama-server
```



## OPEA Comps
OPEA comps are the components that make up the OPEA ecosystem. These components are containerized microservices and can be assembled as a megaservice.

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

## Microservices interaction