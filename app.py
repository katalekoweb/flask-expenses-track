from flask import  Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'

@app.route('/')
def index():
    expenses = [
        {'item': 'Coffee', 'amount': 3.5},
        {'item': 'Books', 'amount': 12.99},
        {'item': 'Groceries', 'amount': 45.23}
    ]
    
    return render_template('index.html', expenses=expenses)


if __name__ == '__main__':
    app.run(debug=True, port=2030)