from langchain.tools import tool
import asyncio
from cirno_math_and_science_agent.essay_manager import (
    get_essay_info,
    essay_downloader
)
from cirno_math_and_science_agent.request_wolfram import get_answer
from cirno_math_and_science_agent.data_models import *
from cirno_math_and_science_agent.prompts import (
    math_and_science_searcher_description,
    academics_searcher_description
)
import logging

logger = logging.getLogger("Tools")
# The tool for getting the info from wolfram
@tool("math_and_science_searcher", args_schema=WolframInputs, description=math_and_science_searcher_description)
async def search_math_and_science_info(queries:List[str]) -> str:
    logger.info("Start math and science searching...")
    # store the results for the answer.
    results = []
    try:
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
    except Exception as e:
        return f"Search failed due to {e}"
# The tool for getting info from academics searcher
@tool("academics_searcher", args_schema=AcademicsSearcherInput, description=academics_searcher_description)
async def academics_searcher(query:str) -> str:
    logger.info("Start searching in research essay database...")
    # Essay info list
    essay_info = await get_essay_info(query=query, number=5)
    # Process essay info
    succeed_list = []
    # Process essay list
    if (essay_info["success"]):
        for i in essay_info["results"]:
            if "id" in i.keys() and "title" in i.keys():
                tmp = {}
                tmp["id"] = i["id"]
                tmp["title"] = i["title"]
                if "doi" in i.keys():
                    tmp["doi"] = i["doi"]
                else:
                    tmp["doi"] = "N/A"
                succeed_list.append(tmp)
    # Processed list
    processed_list = []