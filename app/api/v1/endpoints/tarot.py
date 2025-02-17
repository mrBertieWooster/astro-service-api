from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.tarot_generator import draw_tarot_cards
from app.services.ai_clients.openai_client.taro_generation import generate_tarot_interpretation
from app.schemas.tarot import TarotSpreadRequest, TarotSpreadResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/spread", response_model=TarotSpreadResponse)
async def get_tarot_spread(request: TarotSpreadRequest, db: Session = Depends(get_db)):
    """
    Генерирует расклад Таро и его интерпретацию.
    """
    spread_types = {
        "card-of-the-day": 1,
        "past-present-future": 3,
        "celtic-cross": 10
    }

    if request.spread_type not in spread_types:
        raise HTTPException(status_code=400, detail="Неизвестный тип расклада.")

    try:
        cards = draw_tarot_cards(db, spread_types[request.spread_type])
        interpretation = await generate_tarot_interpretation(cards, request.spread_type, request.question)

        return TarotSpreadResponse(cards=cards, interpretation=interpretation)
    except Exception as e:
        logger.error(f'Error while calculating tarot draw {str(e)}')
        raise
