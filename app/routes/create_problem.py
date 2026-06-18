from fastapi import APIRouter, HTTPException, Header, Depends

from app.core.config import settings
from app.modules.schemas.schema import CreateProblemRequest, ProgrammingProblem
from app.modules.workflow import ProblemGenerationService


service = ProblemGenerationService()

router = APIRouter(tags=["problems"])


def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != settings.app_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


@router.post(
    "/create_problem",
    response_model=ProgrammingProblem,
    dependencies=[Depends(verify_api_key)],
)
def create_problem(payload: CreateProblemRequest):
    try:
        return service.generate_problem(
            payload.topic,
            payload.difficulty,
            payload.language,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc