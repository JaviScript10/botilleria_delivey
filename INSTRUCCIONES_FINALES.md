# 📋 INSTRUCCIONES FINALES - DrinkGo

## 🎯 Cambios Críticos que Debes Hacer Manualmente:

### 1. **Logo Clickeable** (templates/index.html)

Busca la línea 23-27 y cambia:

```html
<!-- ANTES -->
<div class="logo">

<!-- DESPUÉS -->
<a href="#" class="logo" onclick="scrollToTop(); return false;">
```

Y al final del `</div>` del logo, cierra con `</a>`:

```html
<!-- ANTES -->
</div>

<!-- DESPUÉS -->
</a>
```

### 2. **Nota de Tiempo de Entrega** (templates/index.html)

Después de la línea 73 (después del subtitle), agrega:

```html
<div class="delivery-time-note">
    <strong>⏱️ Tiempos de entrega:</strong> 30-45 min para Valparaíso, Viña y Quilpué. 
    <br>* Villa Alemana, Peñablanca, Limache y Olmué: hasta 120 minutos (según tráfico).
</div>
```

### 3. **Actualizar FAQ** (templates/index.html)

Busca la sección FAQ (línea ~450) y cambia:

```html
<!-- Pregunta de tiempo -->
<p>Nuestro tiempo promedio de entrega es de 30-45 minutos para Valparaíso, Viña y Quilpué. Para Villa Alemana, Peñablanca, Limache y Olmué puede extenderse hasta 120 minutos según tráfico.</p>

<!-- Pregunta de envío -->
<p>El envío es GRATIS en compras sobre $30.000 para Valparaíso, Viña del Mar y Quilpué. Para Villa Alemana, Peñablanca, Limache y Olmué siempre hay un recargo de $20.000.</p>
```

### 4. **Agregar Modal de Política de Privacidad** (templates/index.html)

Después del modal de Términos (línea ~520), agrega:

```html
<!-- Modal Política de Privacidad -->
<div class="modal" id="privacyModal">
    <div class="modal-backdrop"></div>
    <div class="modal-content modal-large">
        <div class="modal-header">
            <h2 class="modal-title">
                <i class="fas fa-shield-alt"></i>
                Política de Privacidad
            </h2>
            <button class="modal-close close-privacy">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="terms-content">
            <h3>1. Recopilación de Datos</h3>
            <p>DrinkGo recopila información personal necesaria para procesar pedidos: nombre, RUT, dirección, teléfono y email.</p>
            
            <h3>2. Uso de la Información</h3>
            <p>Los datos se utilizan exclusivamente para: procesar pedidos, envío de productos, comunicación sobre pedidos y mejora del servicio.</p>
            
            <h3>3. Protección de Datos</h3>
            <p>Implementamos medidas de seguridad para proteger tu información personal contra acceso no autorizado.</p>
            
            <h3>4. Compartir Información</h3>
            <p>No vendemos ni compartimos tus datos personales con terceros, excepto lo necesario para procesar pagos y entregas.</p>
            
            <h3>5. Cookies</h3>
            <p>Usamos cookies para mejorar tu experiencia. Puedes deshabilitarlas en tu navegador.</p>
            
            <h3>6. Tus Derechos</h3>
            <p>Tienes derecho a acceder, rectificar o eliminar tus datos personales. Contacta: contacto@drinkgo.cl</p>
            
            <h3>7. Verificación de Edad</h3>
            <p>Verificamos que todos los usuarios sean mayores de 18 años según la ley chilena.</p>
            
            <p class="terms-date">Última actualización: Enero 2026</p>
        </div>
    </div>
</div>
```

### 5. **JavaScript para Política de Privacidad** (static/js/app.js)

Al final del archivo, agrega:

```javascript
// Link de Política de Privacidad
const privacyLink = document.getElementById('privacyLink');
const privacyModal = document.getElementById('privacyModal');

if (privacyLink) {
    privacyLink.addEventListener('click', (e) => {
        e.preventDefault();
        privacyModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
}

document.querySelectorAll('.close-privacy').forEach(btn => {
    btn.addEventListener('click', () => {
        privacyModal.classList.remove('active');
        document.body.style.overflow = 'auto';
    });
});

// Scroll to top
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
```

---

## 🔧 Webpay - Configuración Futura

### Opción 1: Hosting con Webpay Integrado

**Recomendado: Heroku**
- Costo: Desde $7 USD/mes
- Soporte Python/Flask
- SSL incluido
- Fácil integración Transbank

**Pasos:**
1. Crear cuenta Heroku
2. Instalar Heroku CLI
3. Deploy con: `git push heroku main`
4. Configurar variables de entorno Webpay

### Opción 2: VPS (Más Control)

**DigitalOcean / AWS:**
- Costo: Desde $5 USD/mes
- Más flexible
- Requiere configuración manual

### Credenciales Transbank

Necesitas registrarte en:
https://www.transbank.cl/contacto

Documentos requeridos:
- RUT empresa
- Certificado inicio actividades
- Cuenta bancaria empresa
- Contrato afiliación

**Tiempo aprobación:** 5-10 días hábiles

---

## 📧 Configurar Email para Confirmaciones

### Gmail (Gratis):

1. Ve a: https://myaccount.google.com/apppasswords
2. Genera contraseña de aplicación
3. Edita `app.py`:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'drinkgo.valparaiso@gmail.com',  # TU EMAIL
    'password': 'abcd efgh ijkl mnop'  # PASSWORD APP (16 dígitos)
}
```

### Alternativa: SendGrid (Profesional)

- Gratis hasta 100 emails/día
- Más confiable
- Mejor deliverability

Regístrate en: https://sendgrid.com

---

## ✅ Checklist Pre-Launch:

- [ ] Cambiar números WhatsApp (YA HECHO)
- [ ] Logo clickeable
- [ ] Nota tiempo entrega
- [ ] FAQ actualizado
- [ ] Modal privacidad funcional
- [ ] Configurar email
- [ ] Probar registro usuarios
- [ ] Probar pedido completo
- [ ] Verificar todas las zonas
- [ ] Deploy Vercel
- [ ] Prueba en móvil
- [ ] Prueba en desktop
- [ ] Compartir con equipo
- [ ] 🚀 LANZAR

---

## 🆘 Soporte

Si necesitas ayuda con alguna configuración:

WhatsApp: +56979693753
Email: contacto@drinkgo.cl

---

## 🎉 ¡Casi Listo!

Con estos cambios manuales + el ZIP actualizado, tendrás DrinkGo 100% funcional.

Solo falta:
1. Configurar email
2. (Futuro) Contratar hosting Webpay
3. (Futuro) Credenciales Transbank

**¡A vender bebidas! 🍹🚀**
