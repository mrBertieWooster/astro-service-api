from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.planet_calculation import calculate_planetary_positions, calculate_houses, calculate_aspects
from app.schemas.natal_chart import NatalChartRequest, NatalChartResponse

router = APIRouter()

@router.post("/natal_chart", response_model=NatalChartResponse)
async def generate_natal_chart(request: NatalChartRequest):
    try:
        # Шаг 1: Расчет планет, аспектов и домов
        planetary_positions = calculate_planetary_positions(request.date_of_birth, request.time_of_birth, request.place_of_birth)
        aspects = calculate_aspects(planetary_positions)
        houses = calculate_houses(request.date_of_birth, request.time_of_birth, request.place_of_birth)

        # Шаг 2: Генерация текстового описания через OpenAI
        description = await generate_natal_chart_text(planetary_positions, aspects, houses)

        # Шаг 3: Формирование ответа
        return NatalChartResponse(
            description=description,
            planets=planetary_positions,
            aspects=aspects,
            houses=houses
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации натальной карты: {str(e)}")