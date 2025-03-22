from flask import (
  Flask,
  request,
  jsonify
)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from atm_machine.client.ui import (
  sample_card_id,
  sample_cardholder_name,
  sample_cvc,
  sample_expireDate,
  sample_balance,
  sample_pin
)

curr_balance = sample_balance

@app.route('/updateCardBalance', methods=['POST'])
def update_card_balance():

  data = request.json
  card_id = data.get('card_id')
  balance = data.get('balance')

  if card_id == sample_card_id:
    curr_balance = float(balance)
    return jsonify({
      'success': True
    })

  return jsonify({
    'success': False
  })

@app.route('/card/<string:card_id>', methods=['GET'])
def get_card_details(card_id: str):
  if card_id == sample_card_id:
    return jsonify({
      'card_id': card_id,
      'cardholder_name': sample_cardholder_name,
      'cvc': sample_cvc,
      'expireDate': sample_expireDate,
      'balance': sample_balance,
      'pin': sample_pin
    })

  return jsonify({
    'error': 'Card not found'
  })

@app.route('/loginATM', methods=['POST'])
def login_atm():
  data = request.json
  card_id = data.get('card_id')
  pin = data.get('pin')

  if card_id == sample_card_id and pin == '1234':
    return jsonify({
      'success': True
    })

  return jsonify({
    'success': False
  })
