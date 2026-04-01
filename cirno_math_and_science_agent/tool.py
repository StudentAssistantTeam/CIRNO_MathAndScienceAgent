from langchain.tools import tool
import asyncio
from cirno_math_and_science_agent.essay_manager import (
    get_essay_info,
    essay_processor
)
from cirno_math_and_science_agent.request_wolfram import get_answer
from cirno_math_and_science_agent.data_models import (
    WolframInputs,
    AcademicsSearcherInput
)
from cirno_math_and_science_agent.prompts import (
    math_and_science_searcher_description,
    academics_searcher_description,
    final_answer_description
)
import logging
from typing import List

logger = logging.getLogger("Tools")


# The tool for getting the info from wolfram
@tool("math_and_science_searcher", args_schema=WolframInputs, description=math_and_science_searcher_description)
async def search_math_and_science_info(queries: List[str]) -> str:
    logger.info("Start math and science searching...")
    # store the results for the answer.
    results = []
    try:
        # The function that can store the answer at the same time.
        async def get_ans(query: str):
            results.append(await get_answer(query))

        tasks = [get_ans(i) for i in queries]
        await asyncio.gather(*tasks)
        result = "# Results of Searching:\n\n" + "".join([
            f"## Search Result No.{i}\n\n### Topic:\n\n{res["topic"]}\n\n### Result:\n\n{res["result"]}\n\n"
            for i, res in enumerate(results)
        ])
        logger.info(result)
        return result
    except Exception as e:
        return f"Search failed due to {e}"


# The tool for getting info from academics searcher
@tool("academics_searcher", args_schema=AcademicsSearcherInput, description=academics_searcher_description)
async def academics_searcher(query: str) -> str:
    try:
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

        async def get_essay_summary(info_dict):
            processor = essay_processor(doi=info_dict["doi"], id=info_dict["id"], essay_name=info_dict["title"])
            # Download the essay file
            await processor.download()
            summary = await processor.get_summary()
            if summary["success"]:
                tmp_dict = {}
                tmp_dict["doi"] = summary["doi"]
                tmp_dict["title"] = summary["essay_name"]
                tmp_dict["summary"] = summary["summary"]
                processed_list.append(tmp_dict)

        # Gather the tasks and execute
        tasks = [get_essay_summary(i) for i in succeed_list]
        await asyncio.gather(*tasks)
        # Return
        return "result of searching for essays: " + "".join(
            [
                f"\n\nResult No.{idx + 1}:\n\nTitle: {result['title']}\n\ndoi: {result["doi"]}\n\nShort Summary: \n\n{result["summary"]}"
                for idx, result in enumerate(processed_list)
            ]
        )
    except Exception as e:
        return f"Essay searching failed due to {e}"


# Testing
async def academics_searcher_test(query: str) -> str:
    try:
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

        async def get_essay_summary(info_dict):
            processor = essay_processor(doi=info_dict["doi"], id=info_dict["id"], essay_name=info_dict["title"])
            # Download the essay file
            await processor.download()
            summary = await processor.get_summary()
            if summary["success"]:
                tmp_dict = {}
                tmp_dict["doi"] = summary["doi"]
                tmp_dict["title"] = summary["essay_name"]
                tmp_dict["summary"] = summary["summary"]
                processed_list.append(tmp_dict)

        # Gather the tasks and execute
        tasks = [get_essay_summary(i) for i in succeed_list]
        await asyncio.gather(*tasks)
        # Return
        return "result of searching for essays: " + "".join(
            [
                f"\n\nResult No.{idx + 1}:\n\nTitle: {result['title']}\n\ndoi: {result["doi"]}\n\nShort Summary: \n\n{result["summary"]}"
                for idx, result in enumerate(processed_list)
            ]
        )
    except Exception as e:
        return f"Essay searching failed due to {e}"


# Get final answer.
@tool("final_answer", description=final_answer_description)
async def final_answer() -> None:
    return None


if __name__ == "__main__":
    print(asyncio.run(academics_searcher_test("Application of quantum physics")))
