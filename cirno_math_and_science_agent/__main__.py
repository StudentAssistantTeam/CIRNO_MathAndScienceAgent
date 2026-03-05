# Project dependencies
from cirno_math_and_science_agent.config import settings
import cirno_math_and_science_agent.logger_config as logger_config
from cirno_math_and_science_agent.prompts import academics_searcher_skill
# a2a
from a2a.server.apps import A2AStarletteApplication
from a2a.types import (
    AgentSkill
)
import logging

logger = logging.getLogger("Server")
def main():
    # Defining skills of agent
    skill_info_searching = AgentSkill(
        id="info_searching",
        name="STEM Info Searching Tool",
        description="Searching information or data about science, math, engineering, history or geology. And carry out calculation. ",
        tags=["information", "data"],
        examples=["Give me some information about jupiter.", "Find me some information about France.", ]
    )
    skill_academics_searching = AgentSkill(
        id="academics_searching",
        name="Research Paper Searching Tool",
        description=academics_searcher_skill,
        tags=["information", "theory", "academics"],
        examples=["Show me the researches about machine learning for drug discovery", "Show me about the definition of Quantum Physics. "]
    )
#Entry point
def run():
    logger_config.setup_logging()
    logger.info("Entering main process ...")
    main()