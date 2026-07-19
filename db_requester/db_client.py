from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import MoviesDbCreds

USERNAME = MoviesDbCreds.DB_MOVIES_USERNAME
PASSWORD = MoviesDbCreds.DB_MOVIES_PASSWORD
HOST = MoviesDbCreds.DB_MOVIES_HOST
PORT = MoviesDbCreds.DB_MOVIES_PORT
DATABASE_NAME = MoviesDbCreds.DB_MOVIES_NAME

#  движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False  # Установить True для отладки SQL запросов
)

#  создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()