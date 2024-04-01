from sqlalchemy import Column, String, Integer
from models import Base
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import validates

bcrypt = Bcrypt()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(84), nullable=False, unique=True)
    email = Column(String(84), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User : {self.username} >"
    
    @validates('username')
    def validate_username(self, key, username):
        assert len(username) >= 3, "Username must be at least 3 characters long."
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Email must contain @ symbol."
        return email
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) >= 6, "Password must be at least 6 characters long."
        return password