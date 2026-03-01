from cirno_math_and_science_agent.config import settings
from cirno_math_and_science_agent.prompts import summarize_prompt
import logging
import fitz
import re
import httpx
import litellm

logger = logging.getLogger("essay_manager")
# Load PDF
def load_pdf(path: str):
    # load pdf through fitz
    logger.info(f"Loading PDF: {path}")
    loader = fitz.open(path)
    pages = []
    for page in loader:
        pages.append(page.get_text())
    loader.close()
    return pages
# Get work id
def get_work_id(url: str):
    match = re.search(r"https://openalex\.org/(W\d+)", url)
    if match:
        work_id = match.group(1)
        return work_id
# Essay info searching
async def get_essay_info(query: str, number: int):
    # Request params
    params = {
        "api_key": settings.openalex_api,
        "search": query,
        "page":1,
        "per-page":number,
        "filter":"has_content.pdf:true"
    }
    url = "https://api.openalex.org/works"
    try:
        # Result storage
        results = []
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, params=params, timeout=60)
            if response.status_code==200:
                logger.info("Request successful")
                response_json = response.json()
                result = response_json["results"]
                # Data processing
                for i in result:
                    processed_result = {}
                    # Find id and other info for the result
                    if "id" in i.keys():
                        processed_result["id"] = get_work_id(i["id"])
                    if "doi" in i.keys():
                        processed_result["doi"] = i["doi"]
                    if "title" in i.keys():
                        processed_result["title"] = i["title"]
                    # Add to the results
                    results.append(processed_result)
                return {
                    "success": True,
                    "results": results
                }
            else:
                logger.info(f"request failed due to {response.status_code}")
                # Process the failed requests due to http problems
                return {
                    "success": False,
                    "error": f"search failed due to {response.content}"
                }
    except Exception as e:
        # Error handling
        logger.error(f"Search failed due to {e}")
        return {
            "success": False,
            "error": f"search failed due to {e}"
        }
# Request LLM for essay summary
async def request_llm4summary(pages, title: str):
    try:
        # Get response from the llm
        response = await litellm.acompletion(
            model=settings.llm_model_name,
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            messages=[{
                "role": "user",
                "content":summarize_prompt+f"\n## {title}\n"+"".join([
                    f"\n\n**=====Page{i+1}=====**\n\n{content}" for i,content in enumerate(pages)
                ])
            }]
        )
    except Exception as e:
        logger.error(f"Request failed due to {e}")
        response = f"Cannot get this response due to {e}, try again later!"
    return response