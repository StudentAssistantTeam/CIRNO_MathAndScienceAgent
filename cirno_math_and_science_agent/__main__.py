# Project dependencies
from cirno_math_and_science_agent.config import settings
import cirno_math_and_science_agent.logger_config as logger_config
from cirno_math_and_science_agent.prompts import academics_searcher_skill
from cirno_math_and_science_agent.agent import SUPPORTED_CONTENT_TYPES
# a2a
from a2a.server.apps import A2AStarletteApplication
from a2a.types import (
    AgentSkill,
    AgentCard,
    AgentCapabilities
)
from a2a.server.tasks import (
    InMemoryPushNotificationConfigStore,
    DatabasePushNotificationConfigStore,
    BasePushNotificationSender
)
# Other dependencies
import logging
import httpx

logger = logging.getLogger("Server")


def main():
    # Defining skills of agent
    skill_info_searching = AgentSkill(
        id="info_searching",
        name="STEM Info Searching Tool",
        description="Searching information or data about science, math, engineering, history or geology, and carry out calculations. ",
        tags=["information", "data"],
        examples=["Give me some information about jupiter.",
                  "Find me some information about France.",
                  "Solve $$2^x=114514$$"]
    )
    skill_academics_searching = AgentSkill(
        id="academics_searching",
        name="Research Paper Searching Tool",
        description=academics_searcher_skill,
        tags=["information", "theory", "academics"],
        examples=["Show me the researches about machine learning for drug discovery",
                  "Show me about the definition of Quantum Physics. "]
    )
    # Agent Capabilities
    capabilities = AgentCapabilities(
        streaming=True
    )
    # Defining Agent Card
    agent_card = AgentCard(
        name="STEM Agent",
        description="Expert in science, math, engineering, economics, history or geology",
        url=f"http://{settings.a2a_host}:{settings.a2a_port}/",
        version="0.1.0",
        default_input_modes=SUPPORTED_CONTENT_TYPES,
        default_output_modes=SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill_info_searching, skill_academics_searching]
    )
    # Server
    httpx_client = httpx.AsyncClient()
    # Configuring the push notification system
    if settings.use_db_push_notifications:
        push_config_store = DatabasePushNotificationConfigStore(
            settings.db_url
        )
    else:
        push_config_store = InMemoryPushNotificationConfigStore()
    push_sender = BasePushNotificationSender(
        httpx_client=httpx_client,
        config_store=push_config_store
    )


# Entry point
def run():
    logger_config.setup_logging()
    logger.info("Entering main process ...")
    main()
