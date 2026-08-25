'''
schema/request.py

요청 모델 정의
'''
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class IngredientCreate(BaseModel):
    name: str = Field(..., min_length=1, description="식재료 이름")
    category: str = Field(default="미분류", description="카테고리")
    quantity: str = Field(default="1", description="수량")
    purchase_date: date = Field(..., description='구매일 (YYYY-MM-DD)')
    expiration_date: date = Field(default=None, description="유통기한 (YYYY-MM-DD)")
    storage_method: str = Field(default='냉장', description='보관 방법 (냉장/냉동/실온)')

class IngredientUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, description="식재료 이름")
    category: Optional[str] = Field(default=None, description="카테고리")
    quantity: Optional[str] = Field(default=None, description="수량")
    purchase_date: Optional[date] = Field(default=None, description='구매일 (YYYY-MM-DD)')
    expiration_date: Optional[date] = Field(default=None, description="유통기한 (YYYY-MM-DD)")
    storage_method: Optional[str] = Field(default=None, description='보관 방법 (냉장/냉동/실온)')