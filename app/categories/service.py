from app.categories.model import Category
from app.services.base import BaseService


class CategoryService(BaseService):
    model = Category
