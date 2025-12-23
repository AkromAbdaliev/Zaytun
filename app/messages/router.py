from fastapi import APIRouter, Depends, status

from app.messages.schemas import SMessageCreate, SMessageRead
from app.messages.service import MessageService
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post("", response_model=SMessageRead, status_code=status.HTTP_201_CREATED)
async def send_message(
    data: SMessageCreate,
    current_user=Depends(get_current_user),
):
    return await MessageService.send_message(
        sender_id=current_user.id,
        data=data.model_dump(),
    )


@router.get("/inbox", response_model=list[SMessageRead])
async def get_inbox(current_user=Depends(get_current_user)):
    return await MessageService.get_inbox(current_user.id)


@router.get(
    "/thread/{listing_id}/{other_user_id}",
    response_model=list[SMessageRead],
)
async def get_thread(
    listing_id: int,
    other_user_id: int,
    current_user=Depends(get_current_user),
):
    return await MessageService.get_thread(
        current_user.id,
        other_user_id,
        listing_id,
    )


@router.patch("/{message_id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_message_as_read(
    message_id: int,
    current_user=Depends(get_current_user),
):
    await MessageService.mark_as_read(message_id, current_user.id)
