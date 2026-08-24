'''
schema/request.py

요청 모델 정의
'''
from pydantic import BaseModel, Field
from typing import Optional

class IngredientCreate(BaseModel):
    name: str = Field(..., min_length=1, description="식재료 이름")
    category: str = Field(default="미분류", description="카테고리")
    quantity: str = Field(default="1", description="수량")
    expiration_date: Optional[str] = Field(default=None, description="유통기한 (YYYY-MM-DD)")