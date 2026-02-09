from pydantic import BaseModel, Field
from typing import List
from cirno_math_and_science_agent.prompts import queries_input_description

# Standard for the input of the wolfram tool
class WolframInputs(BaseModel):
    queries:List[str] = Field(
        description=queries_input_description
    )

# Messages returned through chunking
class StreamingMessage():
    def __init__(self, step:str, done:bool, content:str):
        self.step = step
        self.done = done
        self.content = content