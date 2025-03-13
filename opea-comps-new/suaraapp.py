import os

from comps import MegaServiceEndpoint, MicroService, ServiceOrchestrator, ServiceRoleType, ServiceType
from comps.cores.proto.api_protocol import AudioChatCompletionRequest, ChatCompletionResponse
from comps.cores.proto.docarray import LLMParams
from fastapi import Request

MEGA_SERVICE_PORT = int(os.getenv("MEGA_SERVICE_PORT", 8888))

# Service configurations based on docker-compose.yml
WHISPER_SERVER_HOST_IP = os.getenv("WHISPER_SERVER_HOST_IP", "0.0.0.0")
WHISPER_SERVER_PORT = int(os.getenv("WHISPER_SERVER_PORT", 7066))
SPEECHT5_SERVER_HOST_IP = os.getenv("SPEECHT5_SERVER_HOST_IP", "0.0.0.0")
SPEECHT5_SERVER_PORT = int(os.getenv("SPEECHT5_SERVER_PORT", 7055))
OLLAMA_SERVER_HOST_IP = os.getenv("OLLAMA_SERVER_HOST_IP", "0.0.0.0")
OLLAMA_SERVER_PORT = int(os.getenv("OLLAMA_SERVER_PORT", 11434))
OLLAMA_MODEL_ID = os.getenv("OLLAMA_MODEL_ID", "mistral")

# Nginx proxy configuration
USE_NGINX_PROXY = os.getenv("USE_NGINX_PROXY", "true").lower() == "true"
NGINX_HOST = os.getenv("NGINX_HOST", "0.0.0.0")
NGINX_PORT = int(os.getenv("NGINX_PORT", 80))    

def align_inputs(self, inputs, cur_node, runtime_graph, llm_parameters_dict, **kwargs):
    # if self.services[cur_node].service_type == ServiceType.LLM:
    #     # Handle Ollama format
    #     next_inputs = {}
    #     next_inputs["model"] = OLLAMA_MODEL_ID
    #     next_inputs["prompt"] = f"{inputs["asr_result"]}. Sila bagi jawapan dalam 50 perkataan sahaja."
    #     next_inputs["stream"] = False
    #     next_inputs["options"] = {
    #         "temperature": inputs["temperature"],
    #         "top_p": llm_parameters_dict["top_p"],
    #         "frequency_penalty": inputs["frequency_penalty"],
    #     }
    #     inputs = next_inputs
    # elif self.services[cur_node].service_type == ServiceType.TTS:
    #     next_inputs = {}
    #     # Extract text from Ollama response format
    #     if "response" in inputs:
    #         next_inputs["text"] = inputs["response"]
    #     else:
    #         # Fallback for other LLM formats
    #         next_inputs["text"] = inputs.get("choices", [{}])[0].get("message", {}).get("content", "")
    #     next_inputs["voice"] = kwargs["voice"]
    #     inputs = next_inputs
    return inputs


class SuaraService:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        ServiceOrchestrator.align_inputs = align_inputs
        self.megaservice = ServiceOrchestrator()

        self.endpoint = "/v1/suara"

    def add_remote_service(self):
        # Configure ASR service (Whisper)
        if USE_NGINX_PROXY:
            asr = MicroService(
                name="asr",
                host=NGINX_HOST,
                port=NGINX_PORT,
                endpoint="/asr",
                use_remote_service=True,
                service_type=ServiceType.ASR,
            )
        else:
            asr = MicroService(
                name="asr",
                host=WHISPER_SERVER_HOST_IP,
                port=WHISPER_SERVER_PORT,
                endpoint="/v1/asr",
                use_remote_service=True,
                service_type=ServiceType.ASR,
            )

        # Configure LLM service (Ollama)
        if USE_NGINX_PROXY:
            llm = MicroService(
                name="llm",
                host=NGINX_HOST,
                port=NGINX_PORT,
                endpoint="/ollama",
                use_remote_service=True,
                service_type=ServiceType.LLM,
            )
        else:
            llm = MicroService(
                name="llm",
                host=OLLAMA_SERVER_HOST_IP,
                port=OLLAMA_SERVER_PORT,
                endpoint="/api/generate",
                use_remote_service=True,
                service_type=ServiceType.LLM,
            )

        # Configure TTS service (SpeechT5)
        if USE_NGINX_PROXY:
            tts = MicroService(
                name="tts",
                host=NGINX_HOST,
                port=NGINX_PORT,
                endpoint="/tts",
                use_remote_service=True,
                service_type=ServiceType.TTS,
            )
        else:
            tts = MicroService(
                name="tts",
                host=SPEECHT5_SERVER_HOST_IP,
                port=SPEECHT5_SERVER_PORT,
                endpoint="/v1/tts",
                use_remote_service=True,
                service_type=ServiceType.TTS,
            )

        # self.megaservice.add(asr).add(llm).add(tts)
        # self.megaservice.flow_to(asr, llm)
        # self.megaservice.flow_to(llm, tts)
        self.megaservice.add(asr)

    async def handle_request(self, request: Request):
        data = await request.json()

        chat_request = AudioChatCompletionRequest.parse_obj(data)
        parameters = LLMParams(
            # relatively lower max_tokens for audio conversation
            max_tokens=chat_request.max_tokens if chat_request.max_tokens else 128,
            top_k=chat_request.top_k if chat_request.top_k else 10,
            top_p=chat_request.top_p if chat_request.top_p else 0.95,
            temperature=chat_request.temperature if chat_request.temperature else 0.01,
            frequency_penalty=chat_request.frequency_penalty if chat_request.frequency_penalty else 0.0,
            presence_penalty=chat_request.presence_penalty if chat_request.presence_penalty else 0.0,
            repetition_penalty=chat_request.repetition_penalty if chat_request.repetition_penalty else 1.03,
            stream=False,  # TODO add stream LLM output as input to TTS
        )
        result_dict, runtime_graph = await self.megaservice.schedule(
            initial_inputs={"audio": chat_request.audio},
            llm_parameters=parameters,
            voice=chat_request.voice if hasattr(chat_request, "voice") else "default",
        )

        last_node = runtime_graph.all_leaves()[-1]
        response = result_dict[last_node]["tts_result"]

        return response

    def start(self):
        self.service = MicroService(
            self.__class__.__name__,
            service_role=ServiceRoleType.MEGASERVICE,
            host=self.host,
            port=self.port,
            endpoint=self.endpoint,
            input_datatype=AudioChatCompletionRequest,
            output_datatype=ChatCompletionResponse,
        )
        self.service.add_route(self.endpoint, self.handle_request, methods=["POST"])
        self.service.start()


if __name__ == "__main__":
    print(f"[LOG] USE_NGINX_PROXY={USE_NGINX_PROXY}")
    suara = SuaraService(port=MEGA_SERVICE_PORT)
    suara.add_remote_service()
    suara.start()