from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from exceptions import PromoNotFoundException, PromoIsNotStartedException, PromoIsExpiredException, \
    NoAvailableActivationsException, PromoIsNotActiveException, PromoIsNotConnectedWithService, \
    PromoIsNotConnectedWithUser
from models import Promo, ActivationResult, DeactivationResult
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


@router.post("/promo/activate", response_model=ActivationResult, description="Активировать промокод")
async def activate(
    code: str,
    user_id: UUID,
    service_id: UUID,
    promo_service: PromoService = Depends(get_promo_service),
) -> ActivationResult:
    try:
        promo_info = await promo_service.activate(code, user_id, service_id)
        return ActivationResult(
            result=True, discount_type=promo_info.discount_type, discount_amount=promo_info.discount_amount
        )
    except (
        PromoNotFoundException,
        PromoIsNotStartedException,
        PromoIsExpiredException,
        NoAvailableActivationsException,
        PromoIsNotActiveException,
        PromoIsNotConnectedWithService,
        PromoIsNotConnectedWithUser,
    ) as e:
        return ActivationResult(result=False, error_message=e.message)


@router.post("/promo/deactivate", response_model=DeactivationResult, description="Деактивировать промокод")
async def deactivate(
    code: str,
    user_id: UUID,
    promo_service: PromoService = Depends(get_promo_service),
) -> DeactivationResult:
    try:
        await promo_service.deactivate(code, user_id)
        return DeactivationResult(result=True)
    except PromoIsNotConnectedWithUser as e:
        return DeactivationResult(result=False, error_message=e.message)
