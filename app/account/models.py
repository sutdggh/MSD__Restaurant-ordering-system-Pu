from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"

engine = create_engine('sqlite:///restaurant_system.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def register_user(username, password, email):
    existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        print("Username or email already exists!")
        return False
    
    new_user = User(username=username, password=password, email=email)
    session.add(new_user)
    session.commit()
    print(f"User {username} registered successfully!")
    return True

def login_user(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        print(f"Welcome back, {username}!")
        return True
    else:
        print("Invalid username or password.")
        return False

if __name__ == "__main__":
    register_user("alice", "alice123", "alice@example.com")
    register_user("bob", "bob123", "bob@example.com")
    
    login_user("alice", "alice123")
    login_user("bob", "wrongpassword")
