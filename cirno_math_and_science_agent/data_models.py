from pydantic import BaseModel, Field
from typing import List
from cirno_math_and_science_agent.prompts import (
    math_and_science_searcher_queries_input_description,
    academics_searcher_query_description
)
import uuid


# Standard for the input of the wolfram tool
class WolframInputs(BaseModel):
    queries: List[str] = Field(
        description=math_and_science_searcher_queries_input_description
    )


# Standard for the input of the academics searcher tool
class AcademicsSearcherInput(BaseModel):
    query: str = Field(
        description=academics_searcher_query_description
    )


# Messages returned through chunking
class StreamingMessage():
    def __init__(self, step: str, done: bool, content: str):
        self.step: str = step
        self.done: bool = done
        self.content: str = content
