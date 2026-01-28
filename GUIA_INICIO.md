# 🍹 GUÍA RÁPIDA - DrinkGo 2026

## ⚡ Inicio Express

**Windows:** Doble click en `start.bat`  
**Linux/Mac:** `./start.sh`  
**Abre:** http://localhost:5000

## 🔧 Configuración Importante

### 1. WhatsApp (2 números)
Edita `app.py` líneas 19-30:
```python
WHATSAPP_NUMBERS = [
    {'numero': '+56912345678', 'nombre': 'Soporte Principal'},
    {'numero': '+56987654321', 'nombre': 'Soporte Secundario'}
]
```

### 2. Webpay (Transbank)
1. Regístrate en: https://www.transbank.cl
2. Obtén credenciales
3. Edita `app.py` líneas 33-39

## 📍 Zonas de Delivery

✅ **GRATIS sobre $30.000:**
- Valparaíso
- Viña del Mar
- Quilpué

💰 **Recargo $2.000:**
- Villa Alemana  
- Limache
- Olmué

## 🚀 Deploy en Vercel

```bash
npm install -g vercel
vercel login
vercel
vercel --prod
```

## ✨ Mejoras Implementadas

✅ Buscador funcional
✅ Selector de horarios visible
✅ Integración Webpay
✅ WhatsApp dual
✅ 100% Responsive
✅ Fondo con imágenes de bebidas
✅ +30 productos con marcas reales
✅ Promociones tipo "Piscola Lista"
✅ Regalos premium
✅ Tragos listos para servir
✅ FAQ y Términos
✅ Redes sociales en footer
✅ Año 2026

## 🎨 Categorías

- 🏷️ Promociones
- 🎁 Regalos
- 🍸 Tragos Listos
- 🥃 Whisky
- 🍸 Vodka
- 🍹 Ron
- 🍺 Cerveza
- 🍷 Vino
- 🥃 Pisco

## 📞 Soporte

WhatsApp: +569 XXXX XXXX  
Email: contacto@drinkgo.cl  
Horario: Lun-Dom 10:00-23:00

---

⚠️ **PROHIBIDA LA VENTA A MENORES DE 18 AÑOS**

© 2026 DrinkGo - Todos los derechos reservados
