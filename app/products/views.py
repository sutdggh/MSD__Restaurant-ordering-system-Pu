
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 创建数据库连接和会话
engine = create_engine('sqlite:///restaurant_system.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

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

        # 创建支付记录
        payment = Payment(order_id=order.id, payment_method=payment_method, payment_status=payment_status, paid_amount=paid_amount)
        session.add(payment)

        # 更新订单状态为已支付
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

if __name__ == '__main__':
    app.run(debug=True)
