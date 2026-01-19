import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@db:5432/biblioteca",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT_URL", "http://localstack:4566")
TOPIC_ARN = os.getenv("TOPIC_ARN", "arn:aws:sns:us-east-1:000000000000:email-notifications-topic")

AWS_PARAMS = {
    "endpoint_url": AWS_ENDPOINT,
    "region_name": "us-east-1",
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test"
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)