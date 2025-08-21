from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50))
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))


    def __repr__(self):
        return f"<Transaction {self.id}: {self.type} {self.amount}>"

with app.app_context():
    db.create_all()

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()

    if 'date' not in data or 'type' not in data or 'amount' not in data:
        return jsonify({"invalid transaction": "date, type, amount not in data"}),400 #bad request

    date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()

    transactions = Transaction (
        date = date_obj,
        type = data.get('type', ''),
        category = data.get('category', ''),
        amount = float(data['amount']),
        description = data.get('description', '')
    )
    db.session.add(transactions)
    db.session.commit()
    return jsonify({"successful transaction": str(transactions)}),201


@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    output = []
    for t in transactions:
        output.append({
            "id": t.id ,
            "date": t.date,
            "type": t.type ,
            "category": t.category ,
            "amount": t.amount,
            "description": t.description
        })
    return jsonify(output)

@app.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    # set the transaction equal to the transaction query and get the id
    transaction = Transaction.query.get(id)

    if not transaction:
        return jsonify({"Transaction not found": "error"}), 400

    data = request.get_json()
    # if date in data - set the transaction date to the data date
    if 'date' in data:
        transaction.date = datetime.strptime(data ['date'], "%Y-%m-%d").date()
    if 'type' in data:
        transaction.type = data['type']
    if 'category' in data:
        transaction.category = data['category']
    if 'amount' in data:
        transaction.amount = float(data['amount'])
    if 'description' in data:
        transaction.description = data['description']

    db.session.commit()

    return jsonify({"Transaction updated successfully": str(transaction)}), 200



@app.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
   transaction = Transaction.query.get(id)

   if not transaction:
    return jsonify({"error": "Transaction not found"}), 404

   db.session.delete(transaction)
   db.session.commit()

   return jsonify({"Success": f"Transaction {id} deleted"}), 200



if __name__ == '__main__':
    app.run(debug=True)
