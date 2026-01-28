@echo off
echo 🍹 Iniciando DrinkGo...
python -m venv venv
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
cls
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🍹 DrinkGo - Servidor Local  
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🌐 http://localhost:5000
echo.
python app.py
pause
