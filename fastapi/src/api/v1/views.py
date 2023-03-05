from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from exceptions import PromoNotFoundException, PromoIsNotStartedException, PromoIsExpiredException, \
    NoAvailableActivationsException
from models import Promo, ActivationResult
from promo_service import PromoService, get_promo_service
from tools.text_constants import PROMO_IS_NOT_FOUND_MESSAGE

router = APIRouter()


@router.get(
    "/promo/code/{code}",
    response_model=Promo,
    description="Получить информацию о промокоде по уникальному коду"
)
async def get_by_code(
    code: str,
    promo_service: PromoService = Depends(get_promo_service),
) -> Promo | None:
    promo = await promo_service.get_by_code(code)
    if not promo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PROMO_IS_NOT_FOUND_MESSAGE)
    return promo


@router.get(
    "/promo/user/{user_id}",
    response_model=list[Promo],
    description="Получить информацию о промокодах для пользователя"
)
async def get_by_user_id(
    user_id: UUID,
    promo_service: PromoService = Depends(get_promo_service),
) -> list[Promo]:
    return await promo_service.get_by_user_id(user_id)


@router.post("/promo/code/{code}/activate", response_model=ActivationResult, description="Активировать промокод")
async def activate(
    code: str,
    promo_service: PromoService = Depends(get_promo_service),
) -> ActivationResult:
    try:
        await promo_service.activate(code)
        return ActivationResult(result=True)
    except (
        PromoNotFoundException, PromoIsNotStartedException, PromoIsExpiredException, NoAvailableActivationsException
    ) as e:
        return ActivationResult(result=False, message=e.message)


@router.post("/promo/code/{code}/deactivate", description="Деактивировать промокод")
async def deactivate(
    code: str,
    promo_service: PromoService = Depends(get_promo_service),
) -> None:
    await promo_service.deactivate(code)
