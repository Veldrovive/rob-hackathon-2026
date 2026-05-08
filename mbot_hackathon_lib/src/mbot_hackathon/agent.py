"""
Interface for the LLM.
We have a remote vLLM running at VLLM_URL.
The agent prompt is stored in AGENT_PROMPT.
We use structured output to ensure the LLM returns a list of actions.
This file contains a class that connects to the vllm server, validates the connection,
and exposes a function to take in a user prompt and return the list of actions.
"""

"""
Sturctured output example
from typing import List, Union, Literal
from pydantic import BaseModel, Field
from openai import OpenAI

# 1. Define the specific action constraints
class SpeakAction(BaseModel):
    action: Literal["speak"]
    content: str

class NavigateAction(BaseModel):
    action: Literal["navigate"]
    waypoint: str

# 2. Combine them into a Union
# This forces the LLM to pick exactly one of the defined action objects
AgentCommand = Union[SpeakAction, NavigateAction]

# 3. Wrap it in a root object
# Note: While you can technically return a naked JSON array, wrapping it 
# inside a root object (like {"commands": [...]}) is the standard, 
# most reliable way to enforce schemas in OpenAI-compatible APIs.
class AgentOutput(BaseModel):
    commands: List[AgentCommand]
"""

"""
Usage example
# Initialize the client pointing to your local vLLM instance
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="empty", 
)

model = client.models.list().data[0].id

# Request the structured output
completion = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system", 
            "content": "You are a helpful robot guide. Choose to speak, navigate, or both."
        },
        {
            "role": "user", 
            "content": "I need to use the bathroom"
        }
    ],
    # Enforce the strict JSON schema
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "agent_commands",
            "schema": AgentOutput.model_json_schema()
        },
    },
)

print(completion.choices[0].message.content)
"""

from typing import List, Union, Literal
from pydantic import BaseModel
from openai import OpenAI

from mbot_hackathon.definitions import ROOT

VLLM_URL = "http://localhost:8001"
# VLLM_URL = "http://host.docker.internal:8000"
AGENT_PROMPT_PATH = ROOT / "agent_prompt.txt"
AGENT_PROMPT = AGENT_PROMPT_PATH.read_text()

# We support english, spanish, french, german, chinese, japanese, arabic, portuguese, russian
SUPPORTED_LANGUAGES = Literal["en", "es", "fr", "de", "zh", "ja", "ar", "pt", "ru"]

class SpeakAction(BaseModel):
    action: Literal["speak"]
    language: SUPPORTED_LANGUAGES
    content: str

class NavigateAction(BaseModel):
    action: Literal["navigate"]
    waypoint: str

AgentCommand = Union[SpeakAction, NavigateAction]

class AgentOutput(BaseModel):
    commands: List[AgentCommand]

class Agent:
    def __init__(self, base_url: str = f"{VLLM_URL}/v1"):
        self.client = OpenAI(
            base_url=base_url,
            api_key="empty", 
        )
        
        try:
            models = self.client.models.list().data
            if not models:
                raise ValueError("No models available from vLLM server.")
            self.model = models[0].id
        except Exception as e:
            raise ConnectionError(f"Failed to connect to vLLM server at {base_url}: {e}")

    def get_actions(self, user_prompt: str) -> List[AgentCommand]:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system", 
                    "content": AGENT_PROMPT
                },
                {
                    "role": "user", 
                    "content": user_prompt
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "agent_commands",
                    "schema": AgentOutput.model_json_schema()
                },
            },
        )
        
        response_content = completion.choices[0].message.content
        if not response_content:
            return []
            
        return AgentOutput.model_validate_json(response_content).commands

if __name__ == "__main__":
    print("Testing connection and agent initialization...")
    print(AgentOutput.model_json_schema())
    try:
        agent = Agent()
        print("Agent initialized successfully!")
        print(f"Using model: {agent.model}")
        # Try a test prompt
        actions = agent.get_actions("I'm hungry. Is there a place to get food?")
        print(f"Got {len(actions)} actions: {actions}")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")