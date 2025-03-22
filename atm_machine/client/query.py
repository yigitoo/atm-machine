# -*- coding: utf-8 -*-
"""
@title: query.py
@author: Yiğit GÜMÜŞ
@date: 2025-03-22 22:32:01
"""

import requests

from .credit_card import CreditCard

SERVER_URL = "localhost:5000"

class Query:
  @classmethod
  def getCardDetails(cls, cardId):
    url = f"http://{SERVER_URL}/card/{cardId}"
    response = requests.get(url)
    response = response.json()
    cc = CreditCard(
            card_id = response.get('card_id'),
            cardholder_name = response.get('cardholder_name'),
            cvc = response.get('cvc'),
            expireDate = response.get('expireDate'),
            balance = response.get('balance'),
            pin = response.get('pin')
        )
    return cc
  @classmethod
  def loginATM(cls, cardId, pin):
    url = f"http://{SERVER_URL}/loginATM"
    data = {
      "card_id": cardId,
      "pin": pin
    }
    response = requests.post(url, json=data)
    return response.json()

  @classmethod
  def updateCardBalance(cls, balance, cardId):
    url = f"http://{SERVER_URL}/updateCardBalance"
    data = {
      "balance": balance,
      "card_id": cardId
    }
    response = requests.post(url, json=data)
    return response.json()

