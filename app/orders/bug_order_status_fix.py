from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)  # 增加了密码长度用于存储加密后的密码
    email = Column(String(100), unique=True, nullable=False)

engine = create_engine('sqlite:///restaurant_system.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        if password != confirm_password:
            flash('Passwords do not match! Please try again.')
            return redirect(url_for('register'))

        existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
        
        if existing_user:
            flash('Username or email already exists!')
        else:
            hashed_password = generate_password_hash(password)  # 密码加密
            new_user = User(username=username, password=hashed_password, email=email)
            session.add(new_user)
            session.commit()
            flash(f'Registration successful for {username}!')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):  # 验证加密密码
            flash(f'Welcome back, {username}!')
            return redirect(url_for('order'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/order')
def order():
    menu = {
        "1": {"name": "Fried Rice", "price": 8.50},
        "2": {"name": "Noodles", "price": 7.00},
        "3": {"name": "Dumplings", "price": 6.00},
        "4": {"name": "Soup", "price": 4.50}
    }
    return render_template('order.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)

