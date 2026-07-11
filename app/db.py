from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
import os


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def create_db_and_tables(engine_db = engine):
    SQLModel.metadata.create_all(engine_db)


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    create_db_and_tables()
