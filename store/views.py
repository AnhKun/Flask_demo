from flask import render_template, redirect, url_for, session
from app import app, db, photos
from models import Product, Order, Order_Item
from forms import AddProduct, AddToCart, Checkout
import random

def handle_cart():
    products = []

    grand_total = 0
    index = 0
    for item in session['cart']:
        product = Product.query.filter(Product.id==item['product_id']).first()
        quantity = int(item['quantity'])
        total = product.price * quantity

        grand_total += total

        products.append({
            'id' : product.id,
            'index' : index,
            'name' : product.name,
            'price' : product.price,
            'image' : product.image,
            'quantity' : quantity,
            'total' : total
        })
        index += 1
    return products, grand_total

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<id>')
def product(id):
    product = Product.query.filter(Product.id==id).first()
    quantity = AddToCart()
    return render_template('view-product.html', product=product, quantity=quantity)

@app.route('/quick-add/<id>')
def quick_add(id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'product_id' : id, 'quantity' : 1})
    session.modified = True

    return redirect(url_for('index'))

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []

    form = AddToCart()
    if form.validate_on_submit():
        session['cart'].append({'product_id' : form.product_id.data, 'quantity': form.quantity.data})
        session.modified = True

    return redirect(url_for('index'))

@app.route('/remove-from_cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    form = AddToCart()

    products, grand_total = handle_cart()

    return render_template('cart.html', products=products, form=form, grand_total=grand_total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = Checkout()

    products, grand_total = handle_cart()
    if form.validate_on_submit():

        order = Order()
        form.populate_obj(order)
        order.reference = ''.join([random.choice('ABCDEFGH') for _ in range(5)])
        order.status = 'PENDING'

        for product in products:
            order_item = Order_Item(quantity=product['quantity'], product_id=product['id'])
            order.items.append(order_item)

            product = Product.query.filter_by(id=product['id']).update({'stock' : Product.stock - product['quantity']})

        db.session.add(order)
        db.session.commit()

        session['cart'] = []
        session.modified = True
        return redirect(url_for('index'))

    return render_template('checkout.html', form=form, products=products, grand_total=grand_total)

@app.route('/admin')
def admin():
    products = Product.query.all()
    products_in_stock = Product.query.filter(Product.stock > 0).count()

    orders = Order.query.all()

    return render_template('admin/index.html', admin=True, products=products, products_in_stock=products_in_stock, orders=orders)

@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = AddProduct()
    
    if form.validate_on_submit():
        image_name = photos.save(form.image.data)
        new_product = Product(
            name = form.name.data, 
            price = form.price.data,
            stock = form.stock.data,
            description = form.description.data,
            image = image_name
        )

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('add'))
    return render_template('admin/add-product.html', admin=True, form=form)

@app.route('/admin/order/<order_id>')
def order(order_id):
    order = Order.query.filter(Order.id == int(order_id)).first()
    return render_template('admin/view-order.html', admin=True, order=order)
