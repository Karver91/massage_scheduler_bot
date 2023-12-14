import aiomysql
from asyncio import Lock
from config.config import DATABASE, DB_HOST, DB_USER, DB_PASSWORD


class Database:
    def __init__(self):
        self.user: str = DB_USER
        self.password: str = DB_PASSWORD
        self.host: str = DB_HOST
        self.db_name: str = DATABASE
        self.port: int = 3306
        self.connection: aiomysql.Connection | None = None
        self.cursor: aiomysql.Cursor | None = None
        self._lock: Lock = Lock()  # Будет блокировать потоки при вызове execute

    async def execute(self, query: str, values: tuple = None, commit: bool = False):
        """Выполняет работу с БД"""
        async with self._lock:
            await self.__connect()
            await self.cursor.execute(query, values)
            if commit:
                await self.connection.commit()

    async def __connect(self):
        """Устанавливает соединение"""
        if self.connection is None:
            self.connection: aiomysql.Connection = await aiomysql.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        self.cursor: aiomysql.Cursor = await self.connection.cursor(aiomysql.DictCursor)

    async def close(self) -> None:
        """Закрывает соединение"""
        if isinstance(self.connection, aiomysql.Connection):
            await self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    async def create_tables(self):
        """Создает Базу Данных"""
        await self.execute(query=f"CREATE DATABASE IF NOT EXISTS {self.db_name};\n"
                                 f"CREATE TABLE IF NOT EXISTS {self.db_name}.client("
                                 f"id INT PRIMARY KEY AUTO_INCREMENT, "
                                 f"telegram_id VARCHAR(20), "
                                 f"first_name VARCHAR(32), "
                                 f"last_name VARCHAR(32), "
                                 f"phone_number VARCHAR(16) UNIQUE"
                                 f");\n"
                                 f"CREATE TABLE IF NOT EXISTS {self.db_name}.service("
                                 f"id INT PRIMARY KEY AUTO_INCREMENT, "
                                 f"service_name VARCHAR(32) UNIQUE, "
                                 f"description VARCHAR(496), "
                                 f"duration TINYINT, "
                                 f"price SMALLINT, "
                                 f"is_deleted BOOLEAN NOT NULL DEFAULT FALSE"
                                 f");\n"
                                 f"CREATE TABLE IF NOT EXISTS {self.db_name}.schedule("
                                 f"id INT PRIMARY KEY AUTO_INCREMENT, "
                                 f"client_id INT, "
                                 f"service_id INT, "
                                 f"date DATE, "
                                 f"time TIME, "
                                 f"FOREIGN KEY(client_id) REFERENCES {self.db_name}.client(id), "
                                 f"FOREIGN KEY(service_id) REFERENCES {self.db_name}.service(id)"
                                 f");"
                           )
        await self.close()


database = Database()
