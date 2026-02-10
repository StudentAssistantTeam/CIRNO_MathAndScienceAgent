from langchain_openai import ChatOpenAI
from cirno_math_and_science_agent.config import settings
from langchain.agents import create_agent
from cirno_math_and_science_agent.data_models import StreamingMessage
from cirno_math_and_science_agent.prompts import system_prompt
from cirno_math_and_science_agent.tool import *
from cirno_math_and_science_agent import logger_config
from langchain_core.messages import SystemMessage, HumanMessage
import asyncio
from collections.abc import AsyncGenerator
import logging

logger = logging.getLogger("agent")
#Agent setting
class agent():
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI(
            model_name=settings.llm_model_name,
            openai_api_base=settings.llm_base_url,
            openai_api_key=settings.llm_api_key
        )
        # tools preparation
        tools = [search_math_and_science_info]
        # agent
        self.agent = create_agent(self.llm, tools)
    def test_invoke(self, prompt):
        logger.info("Start requesting...")
        messages = [SystemMessage(content=system_prompt)]
        messages.append(HumanMessage(prompt))
        message = {"messages": messages}
        result = asyncio.run(self.agent.ainvoke(message))
        return result
    async def streaming(self, query:str) -> AsyncGenerator[StreamingMessage, None]:
        try:
            # Setting messages
            messages = [SystemMessage(content=system_prompt)]
            messages.append(HumanMessage(content=query))
            message = {"messages": messages}
            messages_recorded = []
            # Streaming Response
            async for chunk in self.agent.astream(message):
                for step, data in chunk.items():
                    if(step=="model"):
                        messages_recorded.append(data['messages'][0].content)
                    yield StreamingMessage(
                        step = step,
                        content = data['messages'][0].content,
                        done=False
                    )
            yield StreamingMessage(
                step = "finish",
                content = messages_recorded[len(messages_recorded)-1],
                done = True
            )
        except Exception as e:
            logger.error(f"An error occurred due to {e}")
            yield StreamingMessage(
                step="error",
                content=f"Sorry, I have encountered an error {e}",
                done=True
            )

if __name__=="__main__":
    logger_config.setup_logging()
    Agent = agent()
    iterer = Agent.streaming(query="Find me the information about mars")
    async def itering():
        async for i in iterer:
            if(i.step=="model" or i.step=="finish"):
                print(i.content)
    asyncio.run(itering())