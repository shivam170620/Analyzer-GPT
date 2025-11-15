import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from agents.agents import get_code_executor_agent, get_data_analysis_agent

async def get_data_analyzer_team(model_client, docker_executor):

    code_executor_agent = await get_code_executor_agent(docker_executor)
    data_analysis_agent = await get_data_analysis_agent(model_client)
    text_termination = TextMentionTermination("STOP")
    team = RoundRobinGroupChat(
    participants=[data_analysis_agent,code_executor_agent],
    max_turns=50,
    termination_condition=text_termination
)

    return team
