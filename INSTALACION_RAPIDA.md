# 🚀 INSTALACIÓN RÁPIDA - DrinkGo

## ❌ El Problema:
Los archivos del ZIP no están en `C:\drinkgo`

## ✅ Solución:

### PASO 1: Descomprimir el ZIP correctamente

1. **Descarga** el archivo `drinkgo-completo-final.zip`

2. **Click derecho** sobre el ZIP → **Extraer aquí** o **Extraer todo**

3. Se creará una carpeta llamada `drinkgo-premium`

4. **IMPORTANTE:** Entra a esa carpeta:
   ```
   C:\drinkgo-premium\
   ```

### PASO 2: Abre PowerShell en esa carpeta

**Opción A - Desde el Explorador:**
1. Abre la carpeta `drinkgo-premium`
2. En la barra de direcciones, escribe `powershell`
3. Presiona Enter

**Opción B - Desde PowerShell:**
```powershell
cd C:\drinkgo-premium
```

### PASO 3: Verifica que los archivos estén ahí

```powershell
dir
```

Deberías ver:
```
app.py
requirements.txt
templates/
static/
start.bat
...
```

### PASO 4: Instala dependencias

```powershell
pip install Flask==3.0.0 Werkzeug==3.0.1 MarkupSafe==2.1.3
```

### PASO 5: Ejecuta la aplicación

```powershell
python app.py
```

### PASO 6: Abre el navegador

```
http://localhost:5000
```

---

## 🎯 MÉTODO MÁS FÁCIL (Recomendado):

### Simplemente haz doble click en:
```
start.bat
```

¡Eso es todo! Se instalará y ejecutará automáticamente.

---

## 📋 Si sigue sin funcionar:

### Verifica Python instalado:
```powershell
python --version
```

Debe mostrar: `Python 3.8` o superior

### Si no tienes Python:
1. Ve a: https://www.python.org/downloads/
2. Descarga Python 3.11 o 3.12
3. **IMPORTANTE:** Marca "Add Python to PATH" durante instalación
4. Instala
5. Reinicia PowerShell
6. Intenta de nuevo

---

## 🆘 ERROR COMÚN:

### "No such file or directory"

**Causa:** Estás en la carpeta incorrecta

**Solución:**
```powershell
# Encuentra donde está el ZIP
cd C:\Users\TU_USUARIO\Downloads\drinkgo-premium

# O busca manualmente la carpeta y navega ahí
```

---

## ✅ CHECKLIST:

- [ ] ZIP descargado
- [ ] ZIP descomprimido
- [ ] Entraste a la carpeta `drinkgo-premium`
- [ ] Ves `app.py` en esa carpeta
- [ ] Python instalado (python --version)
- [ ] Ejecutaste: `pip install Flask Werkzeug MarkupSafe`
- [ ] Ejecutaste: `python app.py`
- [ ] Abriste: http://localhost:5000

---

## 🎉 Una vez funcionando:

Verás en PowerShell:
```
* Running on http://127.0.0.1:5000
* Running on http://192.168.X.X:5000
```

Abre tu navegador en: **http://localhost:5000**

¡Listo! 🍹
