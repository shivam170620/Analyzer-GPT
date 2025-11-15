from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage
import os
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from pathlib import Path
from autogen_core import CancellationToken
from autogen_core.code_executor import CodeBlock
import asyncio
from dotenv import load_dotenv
import asyncio
from autogen_agentchat.agents import CodeExecutorAgent, ApprovalRequest, ApprovalResponse
from autogen_agentchat.messages import TextMessage
from agents.prompts import data_analyst_system_prompt

root_dir = Path(__file__).resolve().parent.parent
work_dir = root_dir / "docker_executor_workdir"
work_dir.mkdir(exist_ok=True, parents=True)

async def get_code_executor_agent(docker) -> None:
    # docker = DockerCommandLineCodeExecutor(work_dir=work_dir)

    code_executor_agent = CodeExecutorAgent(
        name = "code_executor_agent",
        code_executor=docker,
    )
    return code_executor_agent

async def get_data_analysis_agent(model_client):
    data_analyst_agent = AssistantAgent(
        name="data_analyst_agent",
        model_client=model_client,
         description = 'An Agent that solves Data Analysis problem and gives the code as well',
        system_message=data_analyst_system_prompt,
    )

    return data_analyst_agent
