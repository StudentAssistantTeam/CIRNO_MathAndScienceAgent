import httpx
from typing import Dict
from cirno_math_and_science_agent.config import settings
import asyncio
import logging

logger = logging.getLogger("Wolfram Requests")


# Get information needed
async def get_answer(query: str) -> Dict[str, str]:
    # params setting
    params = {
        'appid': settings.wolfram_app_id,
        'input': query
    }
    # Async request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url="https://www.wolframalpha.com/api/v1/llm-api", params=params, timeout=30)
            result = response.text
        logger.info("Requesting successed")
        return {
            "topic": query,
            "result": result
        }
    except Exception as e:
        # Error processing
        logger.error(f"Request failed due to {e}")
        return {
            "topic": query,
            "result": f"An error {e} occured when fetching this information"
        }


if __name__ == "__main__":
    print(settings.wolfram_app_id)
    print(asyncio.run(get_answer("Satellites of jupiter")))
