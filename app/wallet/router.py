from fastapi import APIRouter, Depends

from app.users.dependencies import get_current_user
from app.wallet.schemas import SWalletRead, SWalletSpend, SWalletTopUp
from app.wallet.service import WalletService

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"],
)


@router.get("/me", response_model=SWalletRead)
async def get_my_wallet(current_user=Depends(get_current_user)):
    return await WalletService.get_or_create_wallet(current_user.id)


@router.post("/topup", response_model=SWalletRead)
async def top_up_wallet(
    data: SWalletTopUp,
    current_user=Depends(get_current_user),
):
    return await WalletService.top_up(current_user.id, data.amount)


@router.post("/spend", response_model=SWalletRead)
async def spend_from_wallet(
    data: SWalletSpend,
    current_user=Depends(get_current_user),
):
    return await WalletService.spend(current_user.id, data.amount)


