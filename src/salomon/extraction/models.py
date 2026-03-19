from typing import Literal

from pydantic import BaseModel

LanguageName = Literal["c", "cpp", "python"]


class SourceFile(BaseModel):
    path: str
    language: str


class FunctionInfo(BaseModel):
    name: str
    file_path: str
    language: LanguageName
    start_line: int
    end_line: int
    signature: str
    code: str
