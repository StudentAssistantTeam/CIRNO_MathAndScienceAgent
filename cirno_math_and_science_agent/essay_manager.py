from cirno_math_and_science_agent.config import settings
from cirno_math_and_science_agent.prompts import summarize_prompt
import logging
import fitz
import re
import httpx
import litellm
import tempfile
import os
import asyncio

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
        "page": 1,
        "per-page": number,
        "filter": "has_content.pdf:true"
    }
    url = "https://api.openalex.org/works"
    try:
        # Result storage
        results = []
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, params=params, timeout=60)
            if response.status_code == 200:
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
            model=f"{settings.llm_provider}/{settings.llm_model_name}",
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            messages=[{
                "role": "user",
                "content": summarize_prompt + f"\n## {title}\n" + "".join([
                    f"\n\n**=====Page{i + 1}=====**\n\n{content}" for i, content in enumerate(pages)
                ])
            }]
        )
    except Exception as e:
        logger.error(f"Request failed due to {e}")
        response = f"Cannot get this response due to {e}, try again later!"
    return response


# Essay downloader
class essay_downloader:
    # Initialize the downloader: Get file id
    def __init__(self, file_id: str):
        self.id = file_id
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

    # Get file name
    def get_name(self):
        return self.temp_file.name

    # Delete temp file
    def delete(self):
        try:
            logger.info(f"Start deleting file {self.temp_file.name}")
            os.unlink(self.temp_file.name)
        except Exception as e:
            logger.error(f"Delete file {self.temp_file.name} failed due to {e}")

    # Download
    async def download(self):
        params = {
            "api_key": settings.openalex_api
        }
        url = f"https://content.openalex.org/works/{self.id}.pdf"
        logger.info(f"Start downloading file {self.id}")
        async with httpx.AsyncClient() as client:
            try:
                # Streaming download
                async with client.stream("GET", url=url, params=params, follow_redirects=True, timeout=60) as responses:
                    if responses.status_code != 200:
                        return {
                            "success": False,
                            "reason": f"Download failed due to {responses.status_code}"
                        }
                    else:
                        async for chunk in responses.aiter_bytes():
                            self.temp_file.write(chunk)
                        self.temp_file.flush()
                        self.temp_file.close()
                        return {
                            "success": True,
                            "path": self.temp_file.name
                        }
            except Exception as e:
                logger.info(f"File download failed due to {e}")
                # Error handling
                return {
                    "success": False,
                    "reason": f"Download failed due to {e}"
                }


# Essay processor
class essay_processor:
    def __init__(self, doi: str, id: str, essay_name: str):
        self.essay_name = essay_name
        self.doi = doi
        self.downloader = essay_downloader(id)
        self.downloaded = False
        self.id = id

    # Download
    async def download(self):
        result = await self.downloader.download()
        if (result["success"]):
            self.downloaded = True
        return result

    # Get summary
    async def get_summary(self, remove_tmp_file: bool = True):
        # Check whether the file is downloaded
        if not self.downloaded:
            return {
                "success": False,
                "reason": "File not downloaded"
            }
        else:
            try:
                loop = asyncio.get_event_loop()

                # reader
                def pdf_reader():
                    return load_pdf(self.downloader.get_name())

                results = await loop.run_in_executor(None, pdf_reader)
                # Summarize
                summary = await request_llm4summary(pages=results, title=self.essay_name)
                # Remove temp files to save spaces.
                if (remove_tmp_file):
                    await loop.run_in_executor(None, self.downloader.delete)
                return {
                    "success": True,
                    "summary": summary.choices[0].message.content,
                    "doi": self.doi,
                    "open_alex_id": self.id,
                    "essay_name": self.essay_name
                }
            except Exception as e:
                logger.error(f"Summary generation failed due to {e}")
                # Remove file even if the summary generation failed
                if (remove_tmp_file):
                    await loop.run_in_executor(None, self.downloader.delete)
                return {
                    "success": False,
                    "reason": str(e)
                }
