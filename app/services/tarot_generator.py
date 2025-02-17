from app.api.v1.models.tarot import TarotCard
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import random
import logging

logger = logging.getLogger(__name__)

async def draw_tarot_cards(db: Session, num_cards: int):
    """
    Выбирает случайные карты Таро и определяет их положение (прямое или перевернутое).
    """
    try:
        result = await db.execute(select(TarotCard).order_by(TarotCard.id))
        cards = result.scalars().all()
        selected_cards = random.sample(cards, num_cards)

        spread = []
        for card in selected_cards:
            is_reversed = random.choice([True, False])
            spread.append({
                "name": card.name,
                "position": "reversed" if is_reversed else "upright",
                "meaning": card.reversed_meaning if is_reversed else card.upright_meaning
            })

        return spread
    except SQLAlchemyError as se:
        logger.error(f'Error cannot generate tarot draw: {str(se)}')
        db.rollback()
        raise
    except Exception as e:
        logger.error(f'Error cannot generate tarot draw: {str(e)}')
        raise
