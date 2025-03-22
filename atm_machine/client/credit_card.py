# -*- coding: utf-8 -*-
"""
@title: credit_card.py
@author: Yiğit GÜMÜŞ
@date: 2025-03-22 22:31:57
"""

class CreditCard:
  def __init__(self, **props):
    self.card_id = props.get('card_id')
    self.cvc = props.get('cvc')
    self.expireDate = props.get('expireDate')
    self.cardholder_name = props.get('cardholder_name')
    self.pin = props.get('pin')
    self.balance = props.get('balance')

  def __str__(self):
    return f"Card ID: {self.card_id}\nCardholder Name: {self.cardholder_name}\nCVC: {self.cvc}\nExpire Date: {self.expireDate}\nBalance: {self.balance}"
