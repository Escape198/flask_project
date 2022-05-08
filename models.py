from app import db, session, Base


class Message(Base):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(250), nullable=False, default='review')
    success = db.Column(db.String(250), nullable=False, default='False')
