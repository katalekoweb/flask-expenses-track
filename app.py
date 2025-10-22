from flask import  Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False)

# cRud
@app.route('/')
def index():
    expenses = Expenses.query.order_by(Expenses.id.desc()).all()
    total = db.session.query(func.sum(Expenses.amount)).scalar()
    return render_template('index.html', expenses=expenses, total=total)

# Crud
@app.route('/store', methods=['POST'])
def create_expense():
    item = request.form['item']
    amount = request.form['amount']
    # description = request.form['description']
    date = request.form['date']
    data_obj = datetime.strptime(date, '%Y-%m-%d').date()
    
    # check if the item exists
    exisiting_expense = Expenses.query.filter_by(item=item).first()
    
    if exisiting_expense:
        return "Erro: Este gasto já foi registado.", 400
    
    new_expense = Expenses(item=item, amount=amount, date=data_obj)
    db.session.add(new_expense)
    
    db.session.commit()
    return redirect('/')

# cruD
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    expense = Expenses.query.get(expense_id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect('/')

@app.route('/update/<int:expense_id>', methods=['GET', 'POST'])
def update_expense(expense_id):
    expense = Expenses.query.get(expense_id)
    if request.method == 'POST':
        expense.item = request.form['item']
        expense.amount = request.form['amount']
        # expense.description = request.form['description']
        # date = request.form['date']
        # expense.date = datetime.strptime(date, '%Y-%m-%d').date()
        
        db.session.commit()
        return redirect('/')
    
    return render_template('update.html', expense=expense)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=2030)