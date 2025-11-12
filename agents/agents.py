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

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
)

# define both agent here datanalyst_agent and code exceutor agent and we have to first ready the code executor agent
# 

root_dir = Path(__file__).resolve().parent.parent
work_dir = root_dir / "docker_executor_workdir"
work_dir.mkdir(exist_ok=True, parents=True)

async def code_executor_agent():
    async with DockerCommandLineCodeExecutor(
        image="python:3.10",
        work_dir=work_dir,
        timeout=60,
    ) as executor:
        result = await executor.execute_code_blocks(
            code_blocks=[
                CodeBlock(language="python", code="print('Hello, World!')"),
            ],
            cancellation_token=CancellationToken(),
        )
        print("Execution Result:")
        print(result)

asyncio.run(code_executor_agent())

# async def data_analyst_agent():
#     console = Console()
#     data_analyst_agent = AssistantAgent(
#         name="Data Analyst Agent",
#         model_client=model_client,
#         system_message=StructuredMessage(
#             content=DATA_ANALYST_AGENT_SYSTEM_PROMPT
#         ),
#         ui=console,
#     )

#     await data_analyst_agent.start_interaction_loop(
#         cancellation_token=CancellationToken(),
#     )
