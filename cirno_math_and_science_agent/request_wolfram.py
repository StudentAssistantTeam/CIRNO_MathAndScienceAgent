import httpx
from typing import Dict
from cirno_math_and_science_agent.config import settings

# 获取需要的数据
async def get_answer(query: str) -> Dict[str,str]:
    # 设置参数
    params = {
        'appid': settings.wolfram_app_id,
        'input': query
    }
    # 异步请求
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url="https://www.wolframalpha.com/api/v1/llm-api",params=params,timeout=30)
            result = response.text
        return {
            "topic":query,
            "result":result
        }
    except Exception as e:
        return {
            "topic":query,
            "result": f"An error {e} occured when fetching this information"
        }

if __name__ == "__main__":
    print(settings.wolfram_app_id)
    print(get_answer("Satellites of jupiter"))