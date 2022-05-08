from app import db, session, Base


class Message(Base):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    success = db.Column(db.Integer, primary_key=True)

