from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = 'your_secret_key'

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
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
        
        # 检查两次输入的密码是否一致
        if password != confirm_password:
            flash('Passwords do not match! Please try again.')
            return redirect(url_for('register'))

        existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
        
        if existing_user:
            flash('Username or email already exists!')
        else:
            new_user = User(username=username, password=password, email=email)
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
        user = session.query(User).filter_by(username=username, password=password).first()
        
        if user:
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

