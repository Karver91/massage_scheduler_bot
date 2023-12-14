from datetime import timedelta

from environs import Env


def parse_time_to_timedelta(time: str) -> timedelta:
    """Парсит строку со временем в timedelta"""
    hours, minutes = map(int, time.split(':'))
    return timedelta(hours=hours, minutes=minutes)


# Экземпляр класса Env для обращения к переменным окружения
env: Env = Env()
env.read_env()

# BOT
BOT_TOKEN = env.str('BOT_TOKEN')
ADMIN_IDS = set(map(int, env.list('ADMIN_IDS')))

# DATABASE
DATABASE = env.str('DATABASE')
DB_HOST = env.str('DB_HOST')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')

MONTH_LIMIT = env.int('MONTH_LIMIT')
WEEKEND = tuple(map(int, env.list('WEEKEND')))
WORKING_TIME = tuple(env.list('WORKING_TIME', subcast=parse_time_to_timedelta))

# CONTACT DETAILS
SALON_ADDRESS = env.str('SALON_ADDRESS')
SALON_PHONE = env.str('SALON_PHONE')

# SMTP
SMTP_USERNAME = env.str('SMTP_USERNAME')
SMTP_PASSWORD = env.str('SMTP_PASSWORD')
SMTP_RECEIVER = env.str('SMTP_RECEIVER')
