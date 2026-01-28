# 🍹 DrinkGo - Delivery Premium de Bebidas Alcohólicas

**Valparaíso y alrededores - 2026**

## 🚀 Inicio Rápido

### Windows:
```bash
start.bat
```

### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

Abre: `http://localhost:5000`

## 📦 Instalación

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

## 🌐 Deploy Vercel

```bash
vercel login
vercel
vercel --prod
```

## ✨ Características

- ✅ Integración Webpay (Transbank)
- ✅ WhatsApp dual (2 números)  
- ✅ Buscador funcional
- ✅ Selector de horarios visible
- ✅ Zonas de delivery con recargos
- ✅ Promociones y combos
- ✅ Regalos premium
- ✅ Tragos listos para servir
- ✅ 100% Responsive
- ✅ Fondo con imágenes de bebidas
- ✅ Más de 30 productos

## 📍 Zonas de Entrega

**Envío GRATIS sobre $30.000:**
- Valparaíso
- Viña del Mar
- Quilpué

**Recargo $2.000:**
- Villa Alemana
- Limache
- Olmué

## 📞 Configuración WhatsApp

Edita en `app.py` líneas 19-30:

```python
WHATSAPP_NUMBERS = [
    {
        'numero': '+56912345678',  # TU NÚMERO 1
        'nombre': 'Soporte Principal',
    },
    {
        'numero': '+56987654321',  # TU NÚMERO 2
        'nombre': 'Soporte Secundario',
    }
]
```

## 💳 Configuración Webpay

1. Regístrate en Transbank
2. Obtén tus credenciales
3. Edita `app.py` líneas 33-39

## 📄 Licencia

MIT License - 2026 DrinkGo

⚠️ Venta prohibida a menores de 18 años
