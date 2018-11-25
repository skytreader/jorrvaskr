from app import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Player(Base):

    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )
    last_modified = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )
