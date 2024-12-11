from flask import Flask, render_template, request, redirect, url_for
from baza_db import db, Dish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    dishes = Dish.query.all()
    return render_template('index.html', dishes=dishes)

@app.route('/add', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        new_dish = Dish(name=name, description=description, price=price)
        db.session.add(new_dish)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_dish.html')

@app.route('/edit/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if dish is None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        dish.name = request.form['name']
        dish.description = request.form['description']
        dish.price = request.form['price']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_dish.html', dish=dish)

@app.route('/delete/<int:dish_id>')
def delete_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if dish is None:
        return redirect(url_for('index'))
    db.session.delete(dish)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)