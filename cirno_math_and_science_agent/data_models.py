from pydantic import BaseModel, Field
from typing import List
from cirno_math_and_science_agent.prompts import queries_input_description

# Standard for the input of the wolfram tool
class WolframInputs(BaseModel):
    queries:List[str] = Field(
        description=queries_input_description
    )