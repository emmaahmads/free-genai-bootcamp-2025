import os
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo
)
from comps.cores.mega.constants import ServiceType, ServiceRoleType
from comps import MicroService, ServiceOrchestrator
from comps.cores.proto.docarray import LLMParams
from fastapi import FastAPI, Request, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from starlette.responses import JSONResponse, PlainTextResponse, StreamingResponse

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7

# Environment variables with defaults
# Lang Portal service
LP_SERVICE_HOST_IP = os.getenv("LP_SERVICE_HOST_IP", "0.0.0.0")
LP_SERVICE_PORT = int(os.getenv("LP_SERVICE_PORT", 9997))

# Embedding services
EMBEDDING_SERVICE_HOST_IP = os.getenv("EMBEDDING_SERVICE_HOST_IP", "0.0.0.0")
EMBEDDING_SERVICE_PORT = int(os.getenv("EMBEDDING_SERVICE_PORT", 6000))
MULTIMODAL_CLIP_EMBEDDER_PORT = int(os.getenv("MULTIMODAL_CLIP_EMBEDDER_PORT", 6990))
EMBEDDER_PORT = int(os.getenv("EMBEDDER_PORT", 10203))

# LLM services
LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "0.0.0.0")
LLM_SERVICE_PORT = int(os.getenv("LLM_SERVICE_PORT", 11434))
LLM_ENDPOINT_PORT = int(os.getenv("LLM_ENDPOINT_PORT", 8008))

# Guardrails and retrieval services
BIAS_DETECTION_PORT = int(os.getenv("BIAS_DETECTION_PORT", 9092))
RETRIEVER_PORT = int(os.getenv("RETRIEVER_PORT", 7000))
PGVECTOR_PORT = int(os.getenv("PGVECTOR_PORT", 5432))

# Jaeger tracing ports
JAEGER_PORT_4317 = int(os.getenv("JAEGER_PORT_4317", 4317))
JAEGER_PORT_4318 = int(os.getenv("JAEGER_PORT_4318", 4318))
JAEGER_PORT_9411 = int(os.getenv("JAEGER_PORT_9411", 9411))
JAEGER_PORT_16686 = int(os.getenv("JAEGER_PORT_16686", 16686))

class LearnMalayService():
    def __init__(self):
        self.host = LP_SERVICE_HOST_IP
        self.port = LP_SERVICE_PORT
        self.endpoint = "/v1/learn-malay"
        self.megaservice = ServiceOrchestrator()
        os.environ["LOGFLAG"] = "true"
        
    def start(self):
        self.service = MicroService(
            self.__class__.__name__,
            service_role=ServiceRoleType.MEGASERVICE,
            host=self.host,
            port=self.port,
            endpoint=self.endpoint,
            input_datatype=ChatCompletionRequest,
            output_datatype=ChatCompletionResponse,
        )
        
        self.service.app.add_route(
            self.endpoint,
            self.handle_request,
            methods=["POST"]
        )
        
        self.service.start()

    async def handle_request(self, request: Request):
        """
        Handle incoming requests to the service.
        """
        print("Received request to /v1/learn-malay")
        try:
            data = await request.json()
            print(f"Request data: {data}")
            model = data.get("model", "deepseek-r1:1.5b")
            messages = data.get("messages", [])
            max_tokens = data.get("max_tokens", 100)
            temperature = data.get("temperature", 0.7)
            
            # Extract the user's message content
            content = ""
            if messages and len(messages) > 0:
                content = messages[0].get("content", "")
            
            # Create a prompt for learning Malay with JSON formatting instruction
            prompt = f"You are a helpful assistant that translates English to Malay. Provide the translation and a brief explanation of key phrases or grammar points. Format your response as JSON with the following structure: {{\"translation\": \"Malay translation here\", \"explanation\": \"Brief explanation of key phrases or grammar\"}}. Translate this English text to Malay: {content}"
            
            # For now, just return a placeholder response until we fix the LLM integration
            return JSONResponse({
                "translation": "This would be the Malay translation",
                "explanation": "This would include an explanation of the translation",
                "original": content,
                "model": model,
                "note": "This is a placeholder. In a real implementation, we would use the LLM to generate a proper translation."
            })
            
            # The code below is commented out until we fix the LLM integration
            """
            # Call the LLM service
            result_dict, runtime_graph = await self.megaservice.schedule(
                initial_inputs={
                    "query": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "model": model
                }
            )
            
            print(f"Runtime graph leaves: {runtime_graph.all_leaves()}")
            print(f"Result dict keys: {result_dict.keys()}")
            
            last_node = runtime_graph.all_leaves()[-1]
            print(f"Last node: {last_node}")
            response_obj = result_dict[last_node]
            print(f"Response object type: {type(response_obj)}")
            
            # Handle the response
            if isinstance(response_obj, StreamingResponse):
                try:
                    # Try to extract the LLM response content
                    response_content = await self.extract_streaming_content(response_obj)
                    print(f"Extracted LLM response: {response_content}")
                    
                    # Parse the JSON from the LLM response
                    try:
                        # Try to extract JSON from the response
                        import re
                        import json
                        
                        # Look for JSON pattern in the response
                        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(0)
                            llm_data = json.loads(json_str)
                            
                            # Create the final response
                            return JSONResponse({
                                "translation": llm_data.get("translation", "Translation not provided"),
                                "explanation": llm_data.get("explanation", "Explanation not provided"),
                                "original": content,
                                "model": model
                            })
                    except Exception as json_error:
                        print(f"Error parsing JSON from LLM response: {json_error}")
                        # If JSON parsing fails, use the raw response
                        return JSONResponse({
                            "translation": response_content,
                            "explanation": "Unable to parse structured explanation",
                            "original": content,
                            "model": model,
                            "raw_response": response_content
                        })
                        
                except Exception as extract_error:
                    print(f"Error extracting content from streaming response: {extract_error}")
                    # Fallback to a basic response
                    return JSONResponse({
                        "translation": "Error extracting translation",
                        "explanation": f"Error: {extract_error}",
                        "original": content,
                        "model": model
                    })
            else:
                # For non-streaming responses, try to extract the text content
                response_text = response_obj.get("text", "") if isinstance(response_obj, dict) else str(response_obj)
                
                # Try to parse JSON from the response text
                try:
                    import re
                    import json
                    
                    # Look for JSON pattern in the response
                    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                        llm_data = json.loads(json_str)
                        
                        # Create the final response
                        return JSONResponse({
                            "translation": llm_data.get("translation", "Translation not provided"),
                            "explanation": llm_data.get("explanation", "Explanation not provided"),
                            "original": content,
                            "model": model
                        })
                except Exception:
                    # If JSON parsing fails, use the raw response
                    return JSONResponse({
                        "translation": response_text,
                        "explanation": "Unable to parse structured explanation",
                        "original": content,
                        "model": model
                    })
            """
        
        except Exception as e:
            import traceback
            print(f"Error processing request: {str(e)}")
            print(traceback.format_exc())
            return PlainTextResponse(f"Error: {e}", status_code=500)
            
    async def extract_streaming_content(self, streaming_response):
        """
        Extract content from a streaming response.
        """
        content = ""
        async for chunk in streaming_response.body_iterator:
            if chunk:
                # Decode the chunk and add it to the content
                chunk_str = chunk.decode('utf-8')
                # Remove the "data: " prefix if present
                if chunk_str.startswith("data: "):
                    chunk_str = chunk_str[6:]
                content += chunk_str
        return content

    def add_remote_service(self):
        # LLM service (Ollama)
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )     
   
        # # CLIP Embedding service
        # clip_embedding = MicroService(
        #     name="clip-embedding",
        #     host=EMBEDDING_SERVICE_HOST_IP,
        #     port=EMBEDDER_PORT,
        #     endpoint="/v1/embeddings",
        #     use_remote_service=True,
        #     service_type=ServiceType.EMBEDDING,
        # )
 
        # # Multimodal CLIP Embedding service
        # multimodal_clip = MicroService(
        #     name="multimodal-clip",
        #     host=EMBEDDING_SERVICE_HOST_IP,
        #     port=MULTIMODAL_CLIP_EMBEDDER_PORT,
        #     endpoint="/v1/embeddings/multimodal",
        #     use_remote_service=True,
        #     service_type=ServiceType.EMBEDDING,
        # )
        
        # # Guardrails Bias Detection service
        # bias_detection = MicroService(
        #     name="bias-detection",
        #     host=EMBEDDING_SERVICE_HOST_IP,
        #     port=BIAS_DETECTION_PORT,
        #     endpoint="/v1/detect_bias",
        #     use_remote_service=True,
        #     service_type=ServiceType.GUARDRAIL,
        # )
        
        # # Retriever service (PGVector)
        # retriever = MicroService(
        #     name="retriever",
        #     host=EMBEDDING_SERVICE_HOST_IP,
        #     port=RETRIEVER_PORT,
        #     endpoint="/v1/retrieve",
        #     use_remote_service=True,
        #     service_type=ServiceType.RETRIEVER,
        # )
        # self.megaservice.add(llm).add(clip_embedding).add(multimodal_clip).add(bias_detection).add(retriever)
        # self.megaservice.flow_to(bias_detection, llm)
        # self.megaservice.flow_to(retriever, llm)
        self.megaservice.add(llm)
        # Display all services
        print("Service Names:", [name.split('/')[0] for name in self.megaservice.services.keys()])

if __name__ == "__main__":
    service = LearnMalayService()
    service.add_remote_service()
    service.start()