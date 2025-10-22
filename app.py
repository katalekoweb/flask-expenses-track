from flask import  Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False)

@app.route('/')
def index():
    expenses = [
        {'item': 'Coffee', 'amount': 3.5},
        {'item': 'Books', 'amount': 12.99},
        {'item': 'Groceries', 'amount': 45.23}
    ]
    
    return render_template('index.html', expenses=expenses)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=2030)