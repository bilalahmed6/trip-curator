from fastapi import APIRouter
router = APIRouter()
from app.models.schemas import DayPlan, PlanRequest, PlanResponse
from app.services.llm_handler import generate_plan


@router.post("", response_model=PlanResponse)
async def plan_endpoint(req: PlanRequest):
    result = generate_plan(req.query, req.days, req.preferences)
    return {'title': result['title'], 'days': result['days']}
