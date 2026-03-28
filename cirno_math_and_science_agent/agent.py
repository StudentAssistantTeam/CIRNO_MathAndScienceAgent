# langchain
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
# Project dependencies
from cirno_math_and_science_agent.config import settings
from cirno_math_and_science_agent.data_models import StreamingMessage
from cirno_math_and_science_agent.prompts import system_prompt
from cirno_math_and_science_agent.tool import (
    search_math_and_science_info,
    academics_searcher,
    final_answer
)
from cirno_math_and_science_agent import logger_config
import asyncio
from collections.abc import AsyncGenerator
import logging

logger = logging.getLogger("agent")
# Supported content types to get inputted or outputted by the model
SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']


# Agent setting
class agent():
    def __init__(self):
        # LLM
        self.llm = ChatOpenAI(
            model_name=settings.llm_model_name,
            openai_api_base=settings.llm_base_url,
            openai_api_key=settings.llm_api_key
        )
        # tools preparation
        tools = [search_math_and_science_info,
                 academics_searcher,
                 final_answer]
        # agent
        self.agent = create_agent(
            self.llm,
            tools,
            checkpointer=MemorySaver(),
            system_prompt=system_prompt
        )

    def test_invoke(self, prompt):
        logger.info("Start requesting...")
        messages = []
        messages.append(HumanMessage(prompt))
        message = {"messages": messages}
        result = asyncio.run(self.agent.ainvoke(message))
        return result

    async def streaming(self, query: str, context_id: str) -> AsyncGenerator[StreamingMessage, None]:
        logger.info("Start streaming...")
        try:
            # Configuration
            config = {'configurable': {'thread_id': context_id}}
            # Setting messages
            messages = []
            messages.append(HumanMessage(content=query))
            message = {"messages": messages}
            final_content = ""
            # Streaming Response
            async for chunk in self.agent.astream(message, config=config):
                for step, data in chunk.items():
                    if (step == "model"):
                        final_content = data['messages'][-1].content
                    yield StreamingMessage(
                        step=step,
                        content=data['messages'][-1].content,
                        done=False
                    )
            yield StreamingMessage(
                step="finish",
                content=final_content,
                done=True
            )
        except Exception as e:
            logger.error(f"An error occurred due to {e}")
            yield StreamingMessage(
                step="error",
                content=f"Sorry, I have encountered an error {e}",
                done=True
            )


if __name__ == "__main__":
    logger_config.setup_logging()
    Agent = agent()
    iterer = Agent.streaming(query="Give me the info about quantum physics", context_id="114514")


    async def itering():
        async for i in iterer:
            if (i.step == "model" or i.step == "finish"):
                print(i.done)
                print(i.content)


    asyncio.run(itering())
