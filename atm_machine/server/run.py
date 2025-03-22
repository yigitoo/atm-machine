# -*- coding: utf-8 -*-
"""
@title: run.py
@author: Yiğit GÜMÜŞ
@date: 2025-03-22 22:37:19
"""
from .server import app

def run():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
  run()
