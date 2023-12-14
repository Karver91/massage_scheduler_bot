import csv
import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import aiofiles
import aiosmtplib

from config.config import SMTP_USERNAME, SMTP_RECEIVER, SMTP_PASSWORD
from database.db_init import database

# НЕ ЗАБЫТЬ ПЕРЕДАТЬ ПРАВА ДОСТУПА, можно попробовать задать 644 и 600. Поумолчанию 755
# Права на файл принадлежат mysql, mysql должно хватить прав - 7. Для создания файла нужно 7.
# Скорее всего придется использовать создание файла от имени пользователя


async def __get_csv_file_path() -> str:
    await database.execute(query=f'SHOW VARIABLES LIKE "secure_file_priv"')
    result = await database.cursor.fetchone()
    csv_file_path = result['Value'] + 'file.csv'
    await database.close()
    return csv_file_path


async def __get_data() -> list[dict]:
    await database.execute(query=f"SELECT date as 'Дата', time as 'Время', last_name as 'Фамилия', "
                                 f"first_name as 'Имя', phone_number as 'Телефон', service_name as 'Название процедуры' "
                                 f"FROM {database.db_name}.schedule "
                                 f"JOIN {database.db_name}.service "
                                 f"ON {database.db_name}.schedule.service_id = {database.db_name}.service.id "
                                 f"JOIN {database.db_name}.client "
                                 f"ON {database.db_name}.schedule.client_id = {database.db_name}.client.id "
                                 f"ORDER BY date, time")
    result = await database.cursor.fetchall()
    await database.close()
    return result


async def __write_to_csv(file_path: str, data: list[dict]) -> None:
    field_names = [x for x in data[0].keys()]

    async with aiofiles.open(file=file_path, mode='w', encoding='cp1251') as file:
        writer = csv.writer(file)
        await writer.writerow(field_names)
        for row in data:
            await writer.writerow(row.values())


# ПОЧТА
async def __send_email(file_path: str) -> None:
    # Создаем объект многочастных сообщений
    # (сообщения, с включением различных типов содержимого: текст, изображения вложения)
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = SMTP_RECEIVER
    msg['Subject'] = f'Расписание клиентов на {datetime.date.today()}'

    # Добавляем CSV файл
    async with aiofiles.open(file=file_path, mode='rb') as attachment:
        part = MIMEApplication(await attachment.read(), Name='Расписание.csv')
        part['Content-Disposition'] = f'attachment; filename="Расписание.csv"'
        msg.attach(part)

    # Подключение к почтовому серверу и отправка сообщения
    async with aiosmtplib.SMTP(hostname='smtp.gmail.com', port=587) as server:
        await server.login(SMTP_USERNAME, SMTP_PASSWORD)
        await server.sendmail(SMTP_USERNAME, SMTP_RECEIVER, msg.as_string())


async def csv_email_sender() -> None:
    csv_file_path: str = await __get_csv_file_path()
    data: list[dict] = await __get_data()
    if data:
        await __write_to_csv(file_path=csv_file_path, data=data)
        await __send_email(file_path=csv_file_path)
