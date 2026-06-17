from fastapi import APIRouter, HTTPException

from app.modules.schemas.schema import CreateProblemRequest, ProgrammingProblem
from app.modules.workflow import ProblemGenerationService

service = ProblemGenerationService()

router = APIRouter(tags=["problems"])


@router.post("/create_problem", response_model=ProgrammingProblem)
def create_problem(payload: CreateProblemRequest):
    try:
        return service.generate_problem(payload.topic, payload.difficulty, payload.language)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc