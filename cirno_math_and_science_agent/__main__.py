from a2a.server.apps import A2AStarletteApplication
from cirno_math_and_science_agent.config import settings
import cirno_math_and_science_agent.logger_config as logger_config
from a2a.types import (
    AgentSkill
)
import logging

logger = logging.getLogger("Server")
def main():
    # Defining skills of agent
    skill_info_searching = AgentSkill(
        id="info_searching",
        name="Search Information Relative to STEM and Other Subjects",
        description="Searching information or data about science, math, engineering, history or geology. And carry out calculation. ",
        tags=["information", "data"],
        examples=["Give me some information about jupiter.", "Find me some information about France.", ]
    )
#Entry point
def run():
    logger_config.setup_logging()
    logger.info("Entering main process ...")
    main