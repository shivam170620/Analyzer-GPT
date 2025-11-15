import asyncio
from agents.team import get_data_analyzer_team
from autogen_core import CancellationToken
from utils.docker_utils import (
    getDockerCommandLineExecutor,
    start_docker_container,
    stop_docker_container,
)
from models.models import model_client
import os
import shutil
from autogen_agentchat.base import TaskResult


async def run_team():
    docker_executor = getDockerCommandLineExecutor()
    team = await get_data_analyzer_team(model_client, docker_executor)

    try:
        print(" Starting Docker...")
        await start_docker_container(docker_executor)

        print(" Preparing data...")
        os.makedirs("temp", exist_ok=True)
        shutil.copy("data/sales_data_sample.csv", "temp/sales_data_sample.csv")

        print(" Running Data Analyzer Team...")
        initial_task = (
            "Analyze the sales data from temp/sales_data_sample.csv and "
            "provide insights on sales trends for years 2002–2003."
        )

        async for message in team.run_stream(task=initial_task):
            if isinstance(message, TaskResult):
                print(f"Task completed, {message}")
            else:
                print(f"{message.source}: {message.content}")

    except Exception as e:
        print(f" Error occurred: {e}")

    finally:
        print("Stopping Docker...")
        await stop_docker_container(docker_executor)


def main():
    asyncio.run(run_team())


if __name__ == "__main__":
    main()
