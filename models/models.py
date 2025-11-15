from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    model_info={
                "vision": False,
                "function_calling": False,
                "json_output": False,
                "family": "gpt-4o",
                "structured_output": True,
            },
)

