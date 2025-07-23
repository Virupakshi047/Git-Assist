from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./db.sqlite3"  # Local SQLite DB file

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    from app.models import IssueAnalysis
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
