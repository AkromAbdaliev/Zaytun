from fastapi import APIRouter, status

from app.categories.schemas import SCategoryCreate, SCategoryRead
from app.categories.service import CategoryService
from app.core.exceptions import (
    CategoryAlreadyExistsException,
    CategoryNotFoundException,
)

router = APIRouter(
    prefix="/category",
    tags=["Categories"],
)


@router.get("", response_model=list[SCategoryRead])
async def get_categories():
    return await CategoryService.find_all()


@router.get("/{category_id}", response_model=SCategoryRead)
async def get_category(category_id: int):
    category = await CategoryService.find_by_id(category_id)
    if not category:
        raise CategoryNotFoundException
    return category


@router.post("", response_model=SCategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: SCategoryCreate):
    existing_category = CategoryService.find_one_or_none(category_data.name)
    if existing_category:
        raise CategoryAlreadyExistsException
    return await CategoryService.add_one(category_data)


@router.put(
    "/{category_id}", response_model=SCategoryRead, status_code=status.HTTP_202_ACCEPTED
)
async def update_category(category_id: int, category_data: SCategoryCreate):
    existing_category = CategoryService.find_by_id(category_id)
    if not existing_category:
        raise CategoryNotFoundException
    return await CategoryService.update_one(existing_category, category_data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int):
    existing_category = await CategoryService.find_by_id(category_id)
    if not existing_category:
        raise CategoryNotFoundException
    return await CategoryService.delete_one(existing_category)
