# SECCIONES FALTANTES PARA AGREGAR AL HTML

## 1. MODAL DE CHECKOUT COMPLETO (después del modal de carrito)

Agregar después de la línea 240 del index.html actual:

```html
<!-- Checkout View -->
<div id="checkoutView" class="hidden">
    <h2 style="margin-bottom:25px;">Finalizar Compra</h2>
    <form onsubmit="submitCheckout(event)">
        <div class="form-section">
            <h3><i class="fas fa-user"></i> Datos de Contacto</h3>
            <div class="form-row">
                <div class="form-group">
                    <label>Nombre *</label>
                    <input type="text" id="checkoutNombre" name="nombre" required readonly>
                </div>
                <div class="form-group">
                    <label>Teléfono *</label>
                    <input type="tel" id="checkoutTelefono" name="telefono" required readonly>
                </div>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="checkoutEmail" name="email" readonly>
            </div>
        </div>

        <div class="form-section">
            <h3><i class="fas fa-map-marker-alt"></i> Dirección de Entrega</h3>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="otraDireccion" onchange="toggleOtraDireccion()">
                    Enviar a otra dirección
                </label>
            </div>
            <div class="form-group">
                <label>Dirección *</label>
                <input type="text" id="checkoutDireccion" name="direccion" required readonly>
            </div>
            <div class="form-group">
                <label>Comuna *</label>
                <select id="checkoutComuna" name="comuna" required disabled onchange="calcularEnvioCheckout()">
                    {% for key, zona in zonas_delivery.items() %}
                    <option value="{{ key }}">{{ zona.nombre }}</option>
                    {% endfor %}
                </select>
            </div>
            <div id="deliveryInfo" class="delivery-info"></div>
            <div class="form-group">
                <label>Observaciones (opcional)</label>
                <textarea name="observaciones" rows="2" placeholder="Ej: Dejar con portero, Timbre 3B"></textarea>
            </div>
        </div>

        <div class="form-section">
            <h3><i class="fas fa-credit-card"></i> Método de Pago</h3>
            <div class="payment-methods">
                <label class="payment-option">
                    <input type="radio" name="pago" value="efectivo" checked>
                    <div class="payment-card">
                        <i class="fas fa-money-bill-wave"></i>
                        <span>Efectivo</span>
                    </div>
                </label>
                <label class="payment-option">
                    <input type="radio" name="pago" value="transferencia">
                    <div class="payment-card">
                        <i class="fas fa-exchange-alt"></i>
                        <span>Transferencia</span>
                    </div>
                </label>
            </div>
        </div>

        <div class="form-section">
            <h3><i class="fas fa-clock"></i> Horario de Entrega</h3>
            <select name="horario" required class="horario-select">
                <option value="">Selecciona horario</option>
                <option value="express">⚡ Lo antes posible (según zona)</option>
                <option value="tarde1">🕐 Hoy 14:00 - 16:00</option>
                <option value="tarde2">🕒 Hoy 16:00 - 18:00</option>
                <option value="noche1">🕕 Hoy 18:00 - 20:00</option>
                <option value="noche2">🕗 Hoy 20:00 - 22:00</option>
            </select>
        </div>

        <div class="cart-summary">
            <div class="summary-row">
                <span>Subtotal</span>
                <span id="checkoutSubtotal">$0</span>
            </div>
            <div class="summary-row">
                <span>Envío</span>
                <span id="checkoutShipping">$0</span>
            </div>
            <div class="summary-row total">
                <span>Total</span>
                <span id="checkoutTotal">$0</span>
            </div>
        </div>

        <div class="form-actions">
            <button type="button" class="btn-secondary" onclick="volverAlCarrito()">
                <i class="fas fa-arrow-left"></i> Volver
            </button>
            <button type="submit" class="btn-primary">
                Confirmar Pedido <i class="fas fa-check"></i>
            </button>
        </div>
    </form>
</div>

<!-- Success View -->
<div id="successView" class="hidden">
    <div class="success-content">
        <div class="success-icon">
            <i class="fas fa-check-circle"></i>
        </div>
        <h2>¡Pedido Confirmado!</h2>
        <p>Tu orden <strong id="orderId"></strong> ha sido recibida.</p>
        <div class="success-details">
            <div><i class="fas fa-clock"></i> <span id="successTiempo"></span></div>
            <div><i class="fas fa-money-bill"></i> Total: <strong id="successTotal"></strong></div>
        </div>
        <button class="btn-primary btn-block" onclick="continuarComprando()">
            Continuar Comprando
        </button>
    </div>
</div>
```

## 2. MODAL DE PERFIL (antes del footer)

```html
<!-- Modal Perfil -->
<div class="modal" id="perfilModal">
    <div class="modal-backdrop"></div>
    <div class="modal-content">
        <div class="modal-header">
            <h2><i class="fas fa-user-circle"></i> Mi Perfil</h2>
            <button class="modal-close" onclick="cerrarPerfil()">×</button>
        </div>
        <div class="perfil-content">
            <div class="perfil-item">
                <i class="fas fa-user"></i>
                <div>
                    <strong>Nombre</strong>
                    <span id="perfilNombre"></span>
                </div>
            </div>
            <div class="perfil-item">
                <i class="fas fa-envelope"></i>
                <div>
                    <strong>Email</strong>
                    <span id="perfilEmail"></span>
                </div>
            </div>
            <div class="perfil-item">
                <i class="fas fa-id-card"></i>
                <div>
                    <strong>RUT</strong>
                    <span id="perfilRut"></span>
                </div>
            </div>
            <div class="perfil-item">
                <i class="fas fa-phone"></i>
                <div>
                    <strong>Teléfono</strong>
                    <span id="perfilTelefono"></span>
                </div>
            </div>
            <div class="perfil-item">
                <i class="fas fa-map-marker-alt"></i>
                <div>
                    <strong>Dirección</strong>
                    <span id="perfilDireccion"></span>
                </div>
            </div>
            <div class="perfil-item">
                <i class="fas fa-city"></i>
                <div>
                    <strong>Comuna</strong>
                    <span id="perfilComuna"></span>
                </div>
            </div>
        </div>
    </div>
</div>
```

## 3. FOOTER COMPLETO CON FAQ (reemplazar footer actual)

```html
<footer class="footer">
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h3><i class="fas fa-cocktail"></i> DrinkGo</h3>
                <p>Delivery premium de bebidas alcohólicas</p>
                <div class="social-links">
                    <a href="https://facebook.com/drinkgo" target="_blank" class="social-link">
                        <i class="fab fa-facebook"></i>
                    </a>
                    <a href="https://instagram.com/drinkgo" target="_blank" class="social-link">
                        <i class="fab fa-instagram"></i>
                    </a>
                    <a href="https://x.com/drinkgo" target="_blank" class="social-link">
                        <i class="fab fa-x-twitter"></i>
                    </a>
                </div>
            </div>
            
            <div class="footer-section">
                <h4>Información</h4>
                <ul>
                    <li><a href="#" onclick="abrirFAQ(); return false;"><i class="fas fa-question-circle"></i> Preguntas Frecuentes</a></li>
                    <li><a href="#" onclick="abrirTerminos(); return false;"><i class="fas fa-file-contract"></i> Términos y Condiciones</a></li>
                    <li><a href="#" onclick="abrirPrivacidad(); return false;"><i class="fas fa-shield-alt"></i> Política de Privacidad</a></li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h4>Contacto</h4>
                <p><i class="fas fa-phone"></i> +56979693753</p>
                <p><i class="fas fa-envelope"></i> contacto@drinkgo.cl</p>
                <p><i class="fas fa-clock"></i> Lun-Dom: 10:00-23:00</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2026 DrinkGo - Todos los derechos reservados</p>
            <p class="footer-warning"><i class="fas fa-exclamation-triangle"></i> Prohibida venta a menores de 18 años</p>
        </div>
    </div>
</footer>

<!-- Modal FAQ -->
<div class="modal" id="faqModal">
    <div class="modal-backdrop"></div>
    <div class="modal-content modal-large">
        <div class="modal-header">
            <h2><i class="fas fa-question-circle"></i> Preguntas Frecuentes</h2>
            <button class="modal-close" onclick="cerrarFAQ()">×</button>
        </div>
        <div class="faq-content">
            <div class="faq-item">
                <h3><i class="fas fa-clock"></i> ¿Cuál es el tiempo de entrega?</h3>
                <p>Valparaíso y Viña del Mar: 30-45 minutos. Quilpué, Villa Alemana, Peñablanca, Limache y Olmué: hasta 120 minutos según tráfico.</p>
            </div>
            <div class="faq-item">
                <h3><i class="fas fa-shipping-fast"></i> ¿Cómo funciona el envío gratis?</h3>
                <p>Envío GRATIS en compras sobre $30.000 solo para Valparaíso y Viña del Mar. Otras zonas tienen recargo de $20.000.</p>
            </div>
            <div class="faq-item">
                <h3><i class="fas fa-id-card"></i> ¿Necesito mostrar identificación?</h3>
                <p>Sí, es obligatorio presentar cédula de identidad vigente. Prohibida venta a menores de 18 años.</p>
            </div>
            <div class="faq-item">
                <h3><i class="fas fa-credit-card"></i> ¿Qué métodos de pago aceptan?</h3>
                <p>Aceptamos efectivo y transferencia bancaria.</p>
            </div>
        </div>
    </div>
</div>

<!-- Modal Términos -->
<div class="modal" id="termsModal">
    <div class="modal-backdrop"></div>
    <div class="modal-content modal-large">
        <div class="modal-header">
            <h2><i class="fas fa-file-contract"></i> Términos y Condiciones</h2>
            <button class="modal-close" onclick="cerrarTerminos()">×</button>
        </div>
        <div class="terms-content">
            <h3>1. Venta de Alcohol</h3>
            <p>Prohibida la venta a menores de 18 años según Ley 19.925.</p>
            
            <h3>2. Zonas de Entrega</h3>
            <p>Valparaíso, Viña del Mar, Quilpué, Villa Alemana, Peñablanca, Limache y Olmué.</p>
            
            <h3>3. Tiempos de Entrega</h3>
            <p>Valpo/Viña: 30-45 min. Otras zonas: hasta 120 min.</p>
            
            <h3>4. Envío Gratis</h3>
            <p>Sobre $30.000 solo en Valparaíso y Viña del Mar.</p>
        </div>
    </div>
</div>

<!-- Modal Privacidad -->
<div class="modal" id="privacyModal">
    <div class="modal-backdrop"></div>
    <div class="modal-content modal-large">
        <div class="modal-header">
            <h2><i class="fas fa-shield-alt"></i> Política de Privacidad</h2>
            <button class="modal-close" onclick="cerrarPrivacidad()">×</button>
        </div>
        <div class="terms-content">
            <h3>1. Datos Recopilados</h3>
            <p>Nombre, RUT, email, teléfono, dirección.</p>
            
            <h3>2. Uso de Datos</h3>
            <p>Solo para procesar pedidos y entregas.</p>
            
            <h3>3. Seguridad</h3>
            <p>Protección contra acceso no autorizado.</p>
        </div>
    </div>
</div>
```

## 4. CSS ADICIONAL NECESARIO

Agregar al final de styles.css:

```css
.perfil-content {
    padding: 30px;
}

.perfil-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    border-bottom: 1px solid var(--border);
}

.perfil-item i {
    font-size: 24px;
    color: var(--primary);
    width: 40px;
}

.perfil-item div {
    flex: 1;
}

.perfil-item strong {
    display: block;
    color: var(--text-gray);
    font-size: 12px;
    margin-bottom: 5px;
}

.perfil-item span {
    display: block;
    font-size: 16px;
}

.social-links {
    display: flex;
    gap: 12px;
    margin-top: 15px;
}

.social-link {
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-light);
    transition: all 0.3s ease;
}

.social-link:hover {
    background: var(--primary);
    border-color: var(--primary);
    transform: translateY(-3px);
}

.footer-section ul {
    list-style: none;
    padding: 0;
}

.footer-section ul li {
    margin-bottom: 10px;
}

.footer-section ul li a {
    color: var(--text-gray);
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-section ul li a:hover {
    color: var(--primary);
}

.faq-content, .terms-content {
    padding: 30px;
    max-height: 60vh;
    overflow-y: auto;
}

.faq-item {
    margin-bottom: 25px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
}

.faq-item h3 {
    color: var(--primary);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.terms-content h3 {
    color: var(--primary);
    margin: 25px 0 15px 0;
}

.modal-large {
    max-width: 900px;
}

.success-content {
    padding: 60px 30px;
    text-align: center;
}

.success-icon {
    width: 100px;
    height: 100px;
    margin: 0 auto 30px;
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.success-icon i {
    font-size: 60px;
    color: white;
}

.success-details {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 25px;
    margin: 30px 0;
}

.success-details div {
    padding: 12px;
    font-size: 16px;
}

.delivery-info {
    margin-top: 15px;
    padding: 15px;
    background: rgba(255, 107, 107, 0.1);
    border: 1px solid rgba(255, 107, 107, 0.3);
    border-radius: 12px;
    font-size: 14px;
}

.delivery-info.free {
    background: rgba(76, 175, 80, 0.1);
    border-color: rgba(76, 175, 80, 0.3);
}
```

---

## INSTRUCCIONES:

Estos son los fragmentos que faltan. El HTML completo con todo integrado se generará automáticamente en el próximo ZIP.
