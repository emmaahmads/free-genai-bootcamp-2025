import json
import re
import os
import datetime
from typing import Dict, List, Any, Optional
from openai import OpenAI
import instructor
from tools.get_transcript import get_transcript
from tools.get_content import get_content
from tools.search_videos import search_videos
from pydantic import BaseModel, Field

class AgentAction(BaseModel):
    """Model for the agent's next action"""
    thought: str = Field(description="The agent's reasoning process")
    action: Optional[str] = Field(None, description="The tool to execute")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters for the tool")
    final_answer: Optional[str] = Field(None, description="The final answer if the task is complete")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "thought": "I need to get the transcript of this video",
                    "action": "get_transcript",
                    "parameters": {"video_url": "https://www.youtube.com/watch?v=example"},
                    "final_answer": None
                }
            ]
        }
    }

class YouTubeTranscriptAgent:
    """
    An agent that follows the ReACT framework to retrieve transcripts from YouTube videos.
    It verifies videos are in Malay and appropriate for language learning settings.
    """
    
    def __init__(self):
        self.model = "mistral"
        self.tools = {
            "get_transcript": get_transcript,
            "get_content": get_content,
            "search_videos": search_videos
        }
        
        self.client = instructor.from_openai(
            OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",  # required, but unused
            ),
            mode=instructor.Mode.JSON,
        )

        # Create logs directory if it doesn't exist
        self.logs_dir = "logs"
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Load the agent prompt
        with open("agent-prompt-test.md", "r") as f:
            self.prompt_template = f.read()
        
    async def run(self, youtube_url: str) -> Dict[str, Any]:
        """
        Run the agent to process a YouTube URL and retrieve a transcript.
        
        Args:
            youtube_url: The URL of the YouTube video
            
        Returns:
            A dictionary containing either the transcript or alternative video suggestions
        """
        print(f"Running agent for YouTube URL: {youtube_url}")
        
        # Initialize the conversation
        conversation = [
            {"role": "system", "content": self.prompt_template},
            {"role": "user", "content": f"Get the transcript for this YouTube video: {youtube_url}"}
        ]
        
        # Maximum number of iterations to prevent infinite loops
        max_iterations = 10
        iterations = 0
        
        # Final response structure
        response = {
            "transcript": None,
            "alternatives": []
        }
        
        # Store the full conversation for logging
        conversation_log = []
        final_answer = None
        
        while iterations < max_iterations:
            iterations += 1
            print(f"Iteration {iterations}")
            
            # Get the next action from the model
            result = await self._get_next_action(conversation)
            
            # Check if the agent has completed the task
            print(f"Result: {result}")
            if result and result.get("final_answer"):
                # Parse the final answer to extract transcript or alternatives
                response = self._parse_final_answer(result.get("final_answer"))
                final_answer = result.get("final_answer")
                break
                
            # Execute the tool and get the observation
            if result and result.get("action") and result.get("parameters") is not None:
                tool_name = result.get("action")
                parameters = result.get("parameters", {})
                
                # Add to conversation log
                conversation_log.append({
                    "role": "assistant",
                    "thought": result.get("thought", ""),
                    "action": tool_name,
                    "parameters": parameters
                })
                
                # Execute the tool
                observation = await self._execute_tool(tool_name, parameters)
                
                # Add the observation to conversation log
                conversation_log.append({
                    "role": "environment",
                    "observation": observation
                })
                
                # Add the action and observation to the conversation
                conversation.append({
                    "role": "assistant", 
                    "content": f"Thought: {result.get('thought', '')}\n\nAction: {tool_name}\nParameters: {json.dumps(parameters, indent=2)}"
                })
                
                conversation.append({
                    "role": "user", 
                    "content": f"Observation: {observation}"
                })
            else:
                # If no action is specified, break the loop
                break
        
        # Log the conversation to a file
        self._log_conversation(youtube_url, conversation_log, final_answer)
        print("Logging conversation to file")
                
        return response
    
    async def _get_next_action(self, conversation: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Get the next action from the model.
        
        Args:
            conversation: The conversation history
            
        Returns:
            A dictionary containing the next action and parameters
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation,
                response_model=AgentAction,
                max_retries=2
            )
            
            # Convert to dict for consistency with the rest of the code
            return {
                "thought": response.thought,
                "action": response.action,
                "parameters": response.parameters,
                "final_answer": response.final_answer
            }
        except Exception as e:
            print(f"Error in _get_next_action: {str(e)}")
            # Return a default response with required fields
            return {
                "thought": "Error occurred while processing. Continuing with default reasoning.",
                "action": None,
                "parameters": None,
                "final_answer": "I encountered an error while processing your request. Please try again."
            }
    
    async def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """
        Execute a tool and return the observation.
        
        Args:
            tool_name: The name of the tool to execute
            parameters: The parameters to pass to the tool
            
        Returns:
            The observation from the tool execution
        """
        print(f"Attempting to execute tool: {tool_name} with parameters: {parameters}")
        if tool_name not in self.tools:
            error_message = f"Error: Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
            print(error_message)
            return error_message
        
        try:
            result = await self.tools[tool_name](**parameters)
            print(f"Tool '{tool_name}' executed successfully. Result: {result}")
            return str(result)
        except Exception as e:
            error_message = f"Error executing tool '{tool_name}': {str(e)}"
            print(error_message)
            return error_message
    
    def _parse_final_answer(self, final_answer: str) -> Dict[str, Any]:
        """
        Parse the final answer to extract transcript or alternatives.
        
        Args:
            final_answer: The final answer from the model
            
        Returns:
            A dictionary containing the transcript or alternative video suggestions
        """
        print("Parsing final answer...")
        
        # Ensure final_answer is a string
        if final_answer is None:
            final_answer = ""
            
        # Try to extract a JSON structure if present
        json_pattern = r'```json\s*([\s\S]*?)\s*```'
        json_match = re.search(json_pattern, final_answer)
        
        if json_match:
            try:
                json_str = json_match.group(1)
                print(f"JSON string extracted: {json_str}")
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
        
        # If no JSON found or parsing failed, create a default response
        response = {
            "transcript": None,
            "alternatives": []
        }
        print("No valid JSON found, defaulting response.")

        # Look for alternatives in the text
        alt_pattern = r'https://www\.youtube\.com/watch\?v=([a-zA-Z0-9_-]+)\s*-\s*"([^"]+)"'
        alternatives = re.findall(alt_pattern, final_answer)
        print(f"Found {len(alternatives)} alternative(s).")

        for video_id, title in alternatives:
            print(f"Alternative found - URL: https://www.youtube.com/watch?v={video_id}, Title: {title}")
            response["alternatives"].append({
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": title
            })
        
        return response
    
    def _log_conversation(self, youtube_url: str, conversation_log: List[Dict[str, Any]], final_answer: Optional[str]) -> None:
        """
        Log the conversation to a file.
        
        Args:
            youtube_url: The YouTube URL that was processed
            conversation_log: The conversation history
            final_answer: The final answer from the model
        """
        # Create a timestamp for the log file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = os.path.join(self.logs_dir, f"conversation_{timestamp}.log")
        
        with open(log_file_path, "w") as f:
            # Write date/time
            f.write(f"Date/time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write message request
            f.write(f"Message request: {youtube_url}\n\n")
            
            # Write conversation
            f.write("Conversation:\n")
            for entry in conversation_log:
                if entry.get("role") == "assistant":
                    f.write(f"Thought: {entry.get('thought', '')}\n")
                    f.write(f"Action: {entry.get('action', '')}\n")
                    f.write(f"Parameters: {json.dumps(entry.get('parameters', {}), indent=2)}\n\n")
                elif entry.get("role") == "environment":
                    f.write(f"Observation: {entry.get('observation', '')}\n\n")
            
            # Write final answer
            f.write("Final answer:\n")
            if final_answer is not None:
                f.write(f"{final_answer}\n")
            else:
                f.write("No final answer provided.\n")
