# ABHISHEKBARNWAL1301
# CyBZdjzf4G-kxCQ0u7QH5A


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

DATABASE_URL="cockroachdb://abhishekbarnwal1301:CyBZdjzf4G-kxCQ0u7QH5A@cockroach-cluster-4691.j77.aws-ap-south-1.cockroachlabs.cloud:26257/bookmarkdb?sslmode=verify-full"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()