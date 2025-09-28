from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, MenuItem, Order, OrderItem, Payment  # 从models文件中导入数据模型
from datetime import datetime

# 创建Flask应用
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 设置数据库连接
engine = create_engine('sqlite:///restaurant_system.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 菜单页面和订单处理
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    menu_items = session.query(MenuItem).all()
    if request.method == 'POST':
        user_id = 1  # 假设用户ID为1，实际场景中使用当前登录的用户ID
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

# 支付页面
@app.route('/pay/<int:order_id>', methods=['GET', 'POST'])
def pay(order_id):
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        flash('Order not found!')
        return redirect(url_for('index'))

    if request.method == 'POST':
        payment_method = request.form['payment_method']
        payment_status = 'Completed'  # 假设支付成功
        paid_amount = order.total_price

        payment = Payment(order_id=order.id, payment_method=payment_method, payment_status=payment_status, paid_amount=paid_amount)
        session.add(payment)

        order.status = 'Paid'
        session.commit()

        flash('Payment successful!')
        return redirect(url_for('order_details', order_id=order.id))

    return render_template('pay.html', order=order)

# 订单详情页面
@app.route('/order/<int:order_id>')
def order_details(order_id):
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        flash('Order not found!')
        return redirect(url_for('index'))

    return render_template('order_details.html', order=order)

# 订单历史页面
@app.route('/orders')
def order_history():
    user_id = 1  # 假设用户ID为1
    orders = session.query(Order).filter_by(user_id=user_id).all()
    return render_template('order_history.html', orders=orders)

# 启动Flask服务器
if __name__ == '__main__':
    app.run(debug=True)

