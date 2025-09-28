from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

Base = declarative_base()

# 数据模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    phone = Column(String(15))

    orders = relationship('Order', back_populates='user')


class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200))
    price = Column(Float, nullable=False)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(50), default='Pending')
    order_time = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship('Order', back_populates='order_items')
    menu_item = relationship('MenuItem')

# 数据库初始化
engine = create_engine('sqlite:///restaurant_system.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# 主页
@app.route('/')
def index():
    return render_template('index.html')

# 菜单展示和点餐功能
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    menu_items = session.query(MenuItem).all()
    if request.method == 'POST':
        user_id = 1  # 假设用户ID为1，实际情况下应使用登录用户的ID
        total_price = 0.0
        order = Order(user_id=user_id, total_price=0.0, status='Pending')
        session.add(order)
        session.commit()

        for item in menu_items:
            quantity = int(request.form.get(f'quantity_{item.id}', 0))
            if quantity > 0:
                total_price += item.price * quantity
                order_item = OrderItem(order_id=order.id, menu_item_id=item.id, quantity=quantity, price=item.price)
                session.add(order_item)

        order.total_price = total_price
        session.commit()
        flash('Order placed successfully!')
        return redirect(url_for('order_details', order_id=order.id))

    return render_template('menu.html', menu_items=menu_items)

# 订单详情页
@app.route('/order/<int:order_id>')
def order_details(order_id):
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        flash('Order not found!')
        return redirect(url_for('index'))

    return render_template('order_details.html', order=order)

# 订单历史页
@app.route('/orders')
def order_history():
    user_id = 1  # 假设用户ID为1，实际情况下应使用登录用户的ID
    orders = session.query(Order).filter_by(user_id=user_id).all()
    return render_template('order_history.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)

