from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.planet_calculation import calculate_planetary_positions_and_houses, calculate_aspects
from app.schemas.natal_chart import NatalChartRequest, NatalChartResponse
from app.services.ai_clients.openai_client.openai_natal_generator import generate_natal_chart_text

router = APIRouter()

@router.post("/", response_model=NatalChartResponse)
async def generate_natal_chart(request: NatalChartRequest):
    try:
        latitude = request.place_of_birth.latitude
        longitude = request.place_of_birth.longitude

        planetary_data = calculate_planetary_positions_and_houses(request.date_of_birth, request.time_of_birth, latitude, longitude)
          
        planets = planetary_data["planets"]
        houses = planetary_data["houses"]
        ascendant = planetary_data["ascendant"]
        midheaven = planetary_data["midheaven"]
        
        aspects = calculate_aspects(planets)

        description = await generate_natal_chart_text(planets, aspects, houses, ascendant, midheaven)

        return NatalChartResponse(
            description=description,
            planets=planets,
            aspects=aspects,
            ascendant=ascendant,
            midheaven=midheaven
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации натальной карты: {str(e)}")