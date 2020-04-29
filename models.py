import datetime
from sqlalchemy import Column, String, Integer, Text, Date, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    registered_on = Column(Date, default=datetime.date.today())

    def __str__(self):
        return '\n'.join([self.id, self.username, self.password, self.email, self.registered_on])


# Base.metadata.create_all()


def add_user(username, email, password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    password = generate_password_hash(password)
    user = User(username=username, email=email, password=password)
    session.add(user)
    session.commit()
    session.close()


def check_user(email, password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    name = session.query(User).filter_by(email=email).first()
    if name and check_password_hash(name.password, password):
        session.close()
        return name
    session.close()
    return None
