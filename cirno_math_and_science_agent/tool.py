from langchain.tools import tool
from typing import List
import asyncio
from cirno_math_and_science_agent.request_wolfram import get_answer
from cirno_math_and_science_agent.data_models import *
import logging

logger = logging.getLogger("Tool-Math&Science")
# The tool for getting the info from wolfram
@tool("math_and_science_searcher", args_schema=WolframInputs, description="The tool that allows you to search for information in science, math, engineering, history or geology. Real-time data can be provided.")
async def search_math_and_science_info(queries:List[str]) -> str:
    # store the results for the answer.
    results = []
    # The function that can store the answer at the same time.
    async def get_ans(query:str):
        results.append(await get_answer(query))
    tasks = [get_ans(i) for i in queries]
    await asyncio.gather(*tasks)
    result =  "# Results of Searching:\n\n"+"".join([
            f"## Search Result No.{i}\n\n### Topic:\n\n{res["topic"]}\n\n### Result:\n\n{res["result"]}\n\n"
            for i,res in enumerate(results)
        ])
    logger.info(result)
    return result