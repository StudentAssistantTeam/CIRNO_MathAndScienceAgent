from langchain_openai import ChatOpenAI
from cirno_math_and_science_agent.config import settings
from langchain.agents import create_agent
from cirno_math_and_science_agent.tool import *
from cirno_math_and_science_agent import logger_config
import asyncio

#Agent setting
class agent():
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI(
            model_name=settings.llm_model_name,
            openai_api_base=settings.llm_base_url,
            openai_api_key=settings.llm_api_key
        )
        # tools
        tools = [search_math_and_science_info]
        # agent
        self.agent = create_agent(self.llm, tools)
    def test_invoke(self, prompt):
        logger.info("Start requesting...")
        message = {"messages": [{"role": "user", "content": prompt}]}
        result = asyncio.run(self.agent.ainvoke(message))
        return result

if __name__=="__main__":
    logger_config.setup_logging()
    Agent = agent()
    print(Agent.test_invoke(prompt="Find me the information about mars"))