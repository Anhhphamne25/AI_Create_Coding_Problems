from typing import  List

from pydantic import BaseModel, Field


class CreateProblemRequest(BaseModel):
    topic: str = Field(default_factory=list, examples=["array"])
    difficulty: str = Field(default="easy", examples=["easy"])
    language: str = Field(default="Python", examples=["Python"])


class Example(BaseModel):
    input: str = Field(..., examples=["5\n1 2 3 4 5"])
    output: str = Field(..., examples=["15"])


class ProgrammingProblem(BaseModel):
    title: str = Field(..., examples=["Tinh tong mang"])
    description: str = Field(
        ...,
        examples=["Cho mot mang gom n so nguyen. Hay tinh tong cac phan tu trong mang."],
    )
    examples: List[Example] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    note: str = Field(default="")


class CriticResponse(BaseModel):
    approved: str = Field(default="NOT_APPROVED")
    feedback: str = Field(default="")