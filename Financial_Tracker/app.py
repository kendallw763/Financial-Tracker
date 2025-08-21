# 1️⃣ Import dependencies
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 2️⃣ Initialize Flask app
app = Flask(__name__)

# 3️⃣ Configure database (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4️⃣ Initialize SQLAlchemy
db = SQLAlchemy(app)

# 5️⃣ Define Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # "income" or "expense"
    category = db.Column(db.String(50))
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

    # Optional: string representation
    def __repr__(self):
        return f"<Transaction {self.id}: {self.type} {self.amount}>"

# 6️⃣ Create database tables
with app.app_context():
    db.create_all()

# 7️⃣ Define routes (endpoints)
@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()

    if 'date' not in data or 'type' not in data or 'amount' not in data:
        return jsonify({"invalid transaction": "date, type, amount not in data"}),400 #bad request

    date_obj= datetime.strptime(data['date'], '%Y-%m-%d').date()

    transaction = Transaction (
        date = date_obj,
        type = data[type],
        category = data.get('category', ''),
        amount = float(data['amount']),
        description = data.get('description', '')
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"successful transaction":  str(transaction)}),201


@app.route('/transactions', methods=['GET'])
def get_transactions():
    # TODO: query all transactions, return as JSON
    return jsonify({"message": "Get transactions logic goes here"})

@app.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    # TODO: find transaction by ID, update fields, commit changes
    return jsonify({"message": "Update transaction logic goes here"})

@app.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    # TODO: find transaction by ID, delete, commit changes
    return jsonify({"message": "Delete transaction logic goes here"})

# Optional: analytics route
@app.route('/summary', methods=['GET'])
def summary():
    # TODO: calculate total income, total expenses
    return jsonify({"message": "Summary logic goes here"})

# 8️⃣ Run server
if __name__ == '__main__':
    app.run(debug=True)
