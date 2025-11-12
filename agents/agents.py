from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from pathlib import Path
from autogen_core import CancellationToken
from autogen_core.code_executor import CodeBlock
import asyncio
from dotenv import load_dotenv
from prompts import data_analyst_system_prompt

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
)

root_dir = Path(__file__).resolve().parent.parent
work_dir = root_dir / "docker_executor_workdir"
work_dir.mkdir(exist_ok=True, parents=True)

async def code_executor_agent(code_block):
    async with DockerCommandLineCodeExecutor(
        image="python:3.10",
        work_dir=work_dir,
        timeout=60,
    ) as executor:
        result = await executor.execute_code_blocks(
            code_blocks=[
                CodeBlock(language="python", code=code_block),
            ],
            cancellation_token=CancellationToken(),
        )
        print("Execution Result:")
        print(result)

asyncio.run(code_executor_agent())

async def data_analysis_agent():
    assistant_agent = AssistantAgent(
        name="DataAnalysisAgent",
        model_client=model_client,
        ui=Console(),
        system_message=data_analyst_system_prompt,
    )

    user_query = "Please analyze the file and provide insights on sales trends of last 3 years."

    initial_message = StructuredMessage.from_text(user_query)

    response = await assistant_agent.run(initial_message)

    print("Assistant Response:")
    print(response.content)
