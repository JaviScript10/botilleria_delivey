#!/bin/bash
echo "🍹 Iniciando DrinkGo..."
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🍹 DrinkGo - Servidor Local"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 http://localhost:5000"
echo ""
python app.py
