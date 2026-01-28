# 🚀 GUÍA DE DEPLOY EN VERCEL - DrinkGo

## ✅ Tu proyecto YA está listo para Vercel

Esta versión incluye:
- ✅ `vercel.json` configurado
- ✅ `api/index.py` para Vercel
- ✅ `requirements.txt` con dependencias
- ✅ Estructura optimizada

## 📋 MÉTODO 1: Deploy desde GitHub (RECOMENDADO)

### Paso 1: Subir a GitHub

```bash
# 1. Descomprime el ZIP
cd drinkgo-premium

# 2. Inicializa Git
git init

# 3. Agrega archivos
git add .

# 4. Commit inicial
git commit -m "Initial commit - DrinkGo 2026"

# 5. Crea un repositorio en GitHub.com
# Ve a: https://github.com/new
# Nombre: drinkgo-premium
# Descripción: Delivery premium de bebidas alcohólicas
# Visibilidad: Público o Privado

# 6. Conecta con GitHub (reemplaza TU-USUARIO)
git remote add origin https://github.com/TU-USUARIO/drinkgo-premium.git

# 7. Sube el código
git branch -M main
git push -u origin main
```

### Paso 2: Deploy en Vercel

1. **Ve a Vercel.com**
   - https://vercel.com

2. **Sign Up / Login**
   - Usa tu cuenta de GitHub
   - Autoriza Vercel

3. **Import Project**
   - Click en "Add New..."
   - Selecciona "Project"
   - Busca tu repositorio "drinkgo-premium"
   - Click en "Import"

4. **Configuración (Vercel lo detecta automáticamente)**
   - Framework Preset: **Other**
   - Build Command: (dejar vacío)
   - Output Directory: (dejar vacío)
   - Install Command: `pip install -r requirements.txt`

5. **Environment Variables (Opcional pero recomendado)**
   - Click en "Environment Variables"
   - Agrega:
     ```
     FLASK_ENV=production
     SECRET_KEY=tu-clave-super-secreta-aqui
     ```

6. **Deploy**
   - Click en "Deploy"
   - Espera 1-2 minutos
   - ✅ ¡Listo! Tu app está en vivo

7. **Tu URL será algo como:**
   ```
   https://drinkgo-premium.vercel.app
   ```

---

## 📋 MÉTODO 2: Deploy desde CLI (Más rápido)

### Instalación de Vercel CLI

```bash
# Instalar Vercel CLI globalmente
npm install -g vercel

# o si prefieres con yarn
yarn global add vercel
```

### Deploy Paso a Paso

```bash
# 1. Ve a la carpeta del proyecto
cd drinkgo-premium

# 2. Login en Vercel
vercel login
# Sigue las instrucciones en el navegador

# 3. Deploy (modo desarrollo)
vercel

# Te preguntará:
# ? Set up and deploy "~/drinkgo-premium"? [Y/n] → Y
# ? Which scope do you want to deploy to? → Selecciona tu cuenta
# ? Link to existing project? [y/N] → N
# ? What's your project's name? → drinkgo-premium
# ? In which directory is your code located? → ./ (presiona Enter)

# 4. Deploy a producción
vercel --prod

# ✅ Te dará una URL como:
# https://drinkgo-premium.vercel.app
```

---

## 🔧 CONFIGURACIÓN POST-DEPLOY

### 1. Configurar WhatsApp (IMPORTANTE)

Edita `app.py` antes de hacer deploy:

```python
WHATSAPP_NUMBERS = [
    {
        'numero': '+56912345678',  # ← TU NÚMERO REAL
        'nombre': 'Soporte Principal',
        'mensaje_default': 'Hola! Tengo una consulta sobre DrinkGo'
    },
    {
        'numero': '+56987654321',  # ← TU SEGUNDO NÚMERO
        'nombre': 'Soporte Secundario',
        'mensaje_default': 'Hola! Necesito ayuda con mi pedido'
    }
]
```

Luego:
```bash
git add app.py
git commit -m "Actualizar números WhatsApp"
git push
# Vercel hará deploy automático
```

### 2. Dominio Personalizado (Opcional)

En el dashboard de Vercel:
1. Ve a tu proyecto
2. Click en "Settings"
3. Click en "Domains"
4. Agrega tu dominio: `drinkgo.cl`
5. Sigue las instrucciones para configurar DNS

### 3. Variables de Entorno en Vercel

En el dashboard:
1. Settings → Environment Variables
2. Agrega:
   ```
   SECRET_KEY=genera-una-clave-aleatoria-larga
   WEBPAY_COMMERCE_CODE=tu-codigo-webpay
   WEBPAY_API_KEY=tu-api-key-webpay
   ```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Build failed"

**Solución:**
```bash
# Verifica que requirements.txt esté en la raíz
ls requirements.txt

# Verifica que api/index.py exista
ls api/index.py

# Re-deploy
vercel --prod
```

### Error: "Module not found"

**Solución:**
Verifica `requirements.txt`:
```
Flask==3.0.0
Werkzeug==3.0.1
MarkupSafe==2.1.3
```

### Las imágenes no cargan

**Solución:**
Las imágenes vienen de Unsplash. Verifica tu conexión a internet.
Si necesitas cambiar las URLs, edita `app.py` en la sección `PRODUCTOS`.

### Error 500 en producción

**Solución:**
1. Ve a Vercel Dashboard → Tu proyecto → Deployments
2. Click en el deployment más reciente
3. Click en "View Function Logs"
4. Revisa los errores

---

## 📊 MONITOREO

### Ver Logs en Tiempo Real

```bash
vercel logs
```

### Analytics

Vercel incluye analytics gratis:
1. Dashboard → Tu proyecto → Analytics
2. Ve visitas, rendimiento, etc.

---

## 🔄 ACTUALIZACIONES

### Cada vez que hagas cambios:

**Si usas GitHub:**
```bash
git add .
git commit -m "Descripción del cambio"
git push
# Vercel hace deploy automático ✨
```

**Si usas CLI:**
```bash
vercel --prod
```

---

## ✅ CHECKLIST PRE-DEPLOY

- [ ] Cambiar números de WhatsApp en `app.py`
- [ ] Cambiar email de contacto
- [ ] Verificar que las zonas de delivery son correctas
- [ ] Revisar precios de productos
- [ ] Configurar credenciales Webpay (si vas a usar)
- [ ] Agregar SECRET_KEY en variables de entorno
- [ ] Probar localmente primero (`python app.py`)
- [ ] Subir a GitHub
- [ ] Deploy en Vercel
- [ ] Probar la app en producción
- [ ] Compartir la URL 🎉

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Deploy básico
2. 🔧 Configurar Webpay con credenciales reales
3. 📱 Probar pedidos de prueba
4. 🎨 Personalizar diseño si lo necesitas
5. 📊 Monitorear analytics
6. 🚀 ¡Empezar a vender!

---

## 📞 SOPORTE

Si tienes problemas con el deploy:

1. Revisa los logs de Vercel
2. Verifica que todos los archivos estén en GitHub
3. Consulta: https://vercel.com/docs
4. Discord de Vercel: https://vercel.com/discord

---

## 🎉 ¡LISTO!

Tu DrinkGo ya está en vivo y accesible desde cualquier parte del mundo.

**URL de ejemplo:**
```
https://drinkgo-premium.vercel.app
```

**Con dominio personalizado:**
```
https://drinkgo.cl
```

---

💡 **TIP PRO:** Vercel incluye:
- ✅ HTTPS automático (SSL gratis)
- ✅ CDN global (velocidad en todo el mundo)
- ✅ Deploy automático al hacer push a GitHub
- ✅ Preview deployments (URLs únicas por cada commit)
- ✅ Analytics y logs

**¡A vender bebidas! 🍹🚀**
