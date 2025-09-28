<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Ordering System</title>
</head>
<body>
    <h1>Welcome to the Restaurant Ordering System!</h1>
    <a href="{{ url_for('menu') }}">Order Now</a> | 
    <a href="{{ url_for('order_history') }}">View Order History</a>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu</title>
</head>
<body>
    <h1>Menu</h1>
    <form method="POST" action="{{ url_for('menu') }}">
        <ul>
            {% for item in menu_items %}
                <li>
                    {{ item.name }} - ${{ item.price }}<br>
                    Quantity: <input type="number" name="quantity_{{ item.id }}" min="0" value="0">
                </li>
            {% endfor %}
        </ul>
        <input type="submit" value="Place Order">
    </form>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Details</title>
</head>
<body>
    <h1>Order Details</h1>
    <p>Order ID: {{ order.id }}</p>
    <p>Status: {{ order.status }}</p>
    <p>Total Price: ${{ order.total_price }}</p>

    <h2>Items</h2>
    <ul>
        {% for item in order.order_items %}
            <li>{{ item.menu_item.name }} x{{ item.quantity }} - ${{ item.price }}</li>
        {% endfor %}
    </ul>

    {% if order.payment %}
    <h2>Payment Information</h2>
    <p>Payment Method: {{ order.payment.payment_method }}</p>
    <p>Paid Amount: ${{ order.payment.paid_amount }}</p>
    <p>Payment Status: {{ order.payment.payment_status }}</p>
    <p>Payment Time: {{ order.payment.payment_time }}</p>
    {% else %}
    <p>No payment has been made for this order.</p>
    <a href="{{ url_for('pay', order_id=order.id) }}">Proceed to Payment</a>
    {% endif %}
</body>
</html>

