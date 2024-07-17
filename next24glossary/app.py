from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MongoDB Configuration
uri = "mongodb+srv://saiteja:saiteja@saidev.pmtwzvn.mongodb.net/?retryWrites=true&w=majority&appName=saidev"

# Create a new client and connect to the server
mongo = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    mongo.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse')
def browse():
    products = mongo.groceryDB.products.find()
    return render_template('browse.html', products=products)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    products = mongo.groceryDB.products.find({"_id": {"$in": [ObjectId(item) for item in cart_items]}})
    return render_template('cart.html', products=products)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('browse'))

@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'].remove(product_id)
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', [])
    products = list(mongo.groceryDB.products.find({"_id": {"$in": [ObjectId(item) for item in cart_items]}}))

    total_items = len(products)
    total_price = sum(product['price'] for product in products)

    if request.method == 'POST':
        # Process the payment (this is a placeholder)
        order = {
            "user": session.get('user', 'anonymous'),  # Assuming user info is not implemented yet
            "items": cart_items,
            "status": "Processing",
            "total_price": total_price,
            "total_items": total_items
        }
        order_id = mongo.groceryDB.orders.insert_one(order).inserted_id
        session['cart'] = []
        return redirect(url_for('track_order', order_id=order_id))

    return render_template('checkout.html', total_items=total_items, total_price=total_price)

@app.route('/track_order/<order_id>')
def track_order(order_id):
    order = mongo.groceryDB.orders.find_one({"_id": ObjectId(order_id)})
    if order:
        # Retrieve item details
        item_ids = order.get('items', [])
        if item_ids:
            # Convert item_ids to ObjectId for querying
            item_ids = [ObjectId(item_id) for item_id in item_ids]
            # Query products collection for items with matching ids
            order_items = list(mongo.groceryDB.products.find({"_id": {"$in": item_ids}}))
            order['items'] = order_items  # Attach item details to order
            print(f"Order Items: {order_items}")  # Debug print
        else:
            order['items'] = []  # No items found
    else:
        print(f"Order not found for id: {order_id}")  # Debug print

    return render_template('track_order.html', order=order)



if __name__ == '__main__':
    app.run(debug=True)


