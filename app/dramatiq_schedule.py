from dramatiq_crontab import cron
from app.services.horo_generator import (
    generate_daily_horoscopes,
    generate_weekly_horoscopes,
    generate_monthly_horoscopes
)

cron.schedule(generate_daily_horoscopes, cron="0 0 * * *")    # Каждый день в 00:00
cron.schedule(generate_weekly_horoscopes, cron="0 0 * * 1")   # Каждый понедельник в 00:00
cron.schedule(generate_monthly_horoscopes, cron="0 0 1 * *")  # 1-го числа каждого месяца в 00:00
