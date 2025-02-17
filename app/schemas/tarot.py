from pydantic import BaseModel, Field
from typing import List, Optional

class TarotSpreadRequest(BaseModel):
    spread_type: str = Field(..., description="Тип расклада (past-present-future, card-of-the-day и т.д.)")
    question: Optional[str] = Field(None, description="Вопрос, на который ищем ответ.")

class TarotCardResponse(BaseModel):
    name: str
    position: str
    meaning: str

class TarotSpreadResponse(BaseModel):
    cards: List[TarotCardResponse]
    interpretation: str
