// Estado global
let carrito = [];
let currentUser = USER_DATA || null;
let productos = [];

// ========== INICIALIZACIÓN ==========
document.addEventListener('DOMContentLoaded', () => {
    inicializarEventos();
    cargarProductos();
    cargarCarritoLocalStorage();
    actualizarContador();
});

function inicializarEventos() {
    // Tabs autenticación
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById('loginForm').classList.toggle('hidden', targetTab !== 'login');
            document.getElementById('registerForm').classList.toggle('hidden', targetTab !== 'register');
        });
    });
    
    // WhatsApp
    const wspTrigger = document.getElementById('whatsappTrigger');
    const wspMenu = document.getElementById('whatsappMenu');
    const closeWsp = document.getElementById('closeWhatsapp');
    
    if (wspTrigger) wspTrigger.onclick = () => wspMenu.classList.toggle('active');
    if (closeWsp) closeWsp.onclick = () => wspMenu.classList.remove('active');
    
    // User menu
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    if (userMenuBtn) {
        userMenuBtn.onclick = () => userDropdown.classList.toggle('active');
    }
    
    // Buscador
    const searchInput = document.getElementById('searchInput');
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => buscarProductos(e.target.value), 300);
    });
    
    // Categorías
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filtrarCategoria(btn.dataset.category);
        });
    });
    
    // Carrito
    document.getElementById('cartBtn').onclick = () => abrirCarrito();
}

// ========== AUTENTICACIÓN ==========
function openLoginModal() {
    document.getElementById('authModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeAuthModal() {
    document.getElementById('authModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

async function handleLogin(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                email: formData.get('email'),
                password: formData.get('password')
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarNotificacion('¡Bienvenido ' + data.user.nombre.split(' ')[0] + '!', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            mostrarNotificacion(data.error || 'Error al iniciar sesión', 'error');
        }
    } catch (error) {
        mostrarNotificacion('Error de conexión', 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const userData = {
        email: formData.get('email'),
        password: formData.get('password'),
        nombre: formData.get('nombre'),
        rut: formData.get('rut'),
        telefono: formData.get('telefono'),
        direccion: formData.get('direccion'),
        comuna: formData.get('comuna')
    };
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarNotificacion('¡Cuenta creada! Ahora puedes iniciar sesión.', 'success');
            setTimeout(() => {
                document.querySelector('[data-tab="login"]').click();
                e.target.reset();
            }, 2000);
        } else {
            mostrarNotificacion(data.error || 'Error al registrar', 'error');
        }
    } catch (error) {
        mostrarNotificacion('Error de conexión', 'error');
    }
}

async function logout() {
    try {
        await fetch('/api/logout', {method: 'POST'});
        location.reload();
    } catch (error) {
        mostrarNotificacion('Error al cerrar sesión', 'error');
    }
}

// ========== PRODUCTOS ==========
async function cargarProductos(categoria = 'all') {
    try {
        const response = await fetch(`/api/productos?categoria=${categoria}`);
        productos = await response.json();
        renderizarProductos(productos);
    } catch (error) {
        console.error('Error:', error);
    }
}

function renderizarProductos(prods) {
    const grid = document.getElementById('productsGrid');
    
    if (prods.length === 0) {
        grid.innerHTML = '<p style="grid-column:1/-1;text-align:center;padding:40px;color:#999;">No se encontraron productos</p>';
        return;
    }
    
    grid.innerHTML = prods.map(p => `
        <div class="product-card">
            <div class="product-image" style="background-image: url('${p.imagen}')"></div>
            <div class="product-info">
                <div class="product-category">${p.categoria}</div>
                <h3 class="product-name">${p.nombre}</h3>
                <p class="product-description">${p.descripcion}</p>
                <div class="product-footer">
                    <div class="product-price">$${formatNumber(p.precio)}</div>
                    <button class="add-to-cart-btn" onclick="agregarAlCarrito(${p.id})">
                        <i class="fas fa-plus"></i> Agregar
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

async function buscarProductos(query) {
    try {
        const response = await fetch(`/api/productos?search=${encodeURIComponent(query)}`);
        const prods = await response.json();
        renderizarProductos(prods);
    } catch (error) {
        console.error('Error:', error);
    }
}

function filtrarCategoria(categoria) {
    cargarProductos(categoria);
}

// ========== CARRITO ==========
function agregarAlCarrito(productoId) {
    const producto = productos.find(p => p.id === productoId);
    if (!producto) return;
    
    const itemExistente = carrito.find(item => item.id === productoId);
    
    if (itemExistente) {
        itemExistente.cantidad++;
    } else {
        carrito.push({
            id: producto.id,
            nombre: producto.nombre,
            precio: producto.precio,
            imagen: producto.imagen,
            cantidad: 1
        });
    }
    
    actualizarContador();
    guardarCarritoLocalStorage();
    mostrarNotificacion(producto.nombre + ' agregado al carrito', 'success');
    
    // Animación del botón
    event.target.style.transform = 'scale(0.9)';
    setTimeout(() => event.target.style.transform = '', 200);
}

function abrirCarrito() {
    document.getElementById('cartModal').classList.add('active');
    document.getElementById('cartView').style.display = 'block';
    document.getElementById('checkoutView').classList.add('hidden');
    document.getElementById('successView').classList.add('hidden');
    renderizarCarrito();
    document.body.style.overflow = 'hidden';
}

function closeCart() {
    document.getElementById('cartModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function renderizarCarrito() {
    const cartItems = document.getElementById('cartItems');
    
    if (carrito.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart" style="font-size:60px;color:#666;margin-bottom:20px;"></i>
                <h3>Tu carrito está vacío</h3>
                <p>Agrega productos para comenzar tu compra</p>
            </div>
        `;
        document.querySelector('.cart-summary').style.display = 'none';
        document.querySelector('#proceedCheckoutBtn').style.display = 'none';
        return;
    }
    
    cartItems.innerHTML = carrito.map(item => `
        <div class="cart-item">
            <div class="cart-item-image" style="background-image: url('${item.imagen}')"></div>
            <div class="cart-item-details">
                <div class="cart-item-name">${item.nombre}</div>
                <div class="cart-item-price">$${formatNumber(item.precio)}</div>
            </div>
            <div class="cart-item-controls">
                <div class="quantity-controls">
                    <button class="qty-btn" onclick="cambiarCantidad(${item.id}, -1)">−</button>
                    <span class="qty-display">${item.cantidad}</span>
                    <button class="qty-btn" onclick="cambiarCantidad(${item.id}, 1)">+</button>
                </div>
                <button class="remove-btn" onclick="eliminarDelCarrito(${item.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    const subtotal = calcularSubtotal();
    document.getElementById('subtotal').textContent = '$' + formatNumber(subtotal);
    document.getElementById('shipping').textContent = 'Calcular en checkout';
    document.getElementById('total').textContent = '$' + formatNumber(subtotal);
    
    document.querySelector('.cart-summary').style.display = 'block';
    document.querySelector('#proceedCheckoutBtn').style.display = 'block';
}

function cambiarCantidad(productoId, cambio) {
    const item = carrito.find(i => i.id === productoId);
    if (!item) return;
    
    item.cantidad += cambio;
    
    if (item.cantidad <= 0) {
        eliminarDelCarrito(productoId);
        return;
    }
    
    actualizarContador();
    renderizarCarrito();
    guardarCarritoLocalStorage();
}

function eliminarDelCarrito(productoId) {
    carrito = carrito.filter(item => item.id !== productoId);
    actualizarContador();
    renderizarCarrito();
    guardarCarritoLocalStorage();
    mostrarNotificacion('Producto eliminado', 'info');
}

function calcularSubtotal() {
    return carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
}

function actualizarContador() {
    const count = carrito.reduce((sum, item) => sum + item.cantidad, 0);
    document.getElementById('cartCount').textContent = count;
}

function guardarCarritoLocalStorage() {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

function cargarCarritoLocalStorage() {
    const saved = localStorage.getItem('carrito');
    if (saved) {
        carrito = JSON.parse(saved);
    }
}

// ========== CHECKOUT ==========
function proceedCheckout() {
    if (!currentUser) {
        closeCart();
        mostrarNotificacion('Debes iniciar sesión para continuar', 'error');
        setTimeout(() => openLoginModal(), 500);
        return;
    }
    
    document.getElementById('cartView').style.display = 'none';
    document.getElementById('checkoutView').classList.remove('hidden');
    
    // Auto-completar datos del usuario
    if (currentUser) {
        document.getElementById('checkoutNombre').value = currentUser.nombre;
        document.getElementById('checkoutTelefono').value = currentUser.telefono;
        document.getElementById('checkoutEmail').value = currentUser.email;
        document.getElementById('checkoutDireccion').value = currentUser.direccion;
        document.getElementById('checkoutComuna').value = currentUser.comuna;
    }
    
    calcularEnvioCheckout();
}

function volverAlCarrito() {
    document.getElementById('cartView').style.display = 'block';
    document.getElementById('checkoutView').classList.add('hidden');
}

function toggleOtraDireccion() {
    const checkbox = document.getElementById('otraDireccion');
    const isChecked = checkbox.checked;
    
    document.getElementById('checkoutDireccion').readOnly = !isChecked;
    document.getElementById('checkoutComuna').disabled = !isChecked;
    
    if (!isChecked && currentUser) {
        document.getElementById('checkoutDireccion').value = currentUser.direccion;
        document.getElementById('checkoutComuna').value = currentUser.comuna;
    } else if (isChecked) {
        document.getElementById('checkoutDireccion').value = '';
    }
}

async function calcularEnvioCheckout() {
    const comuna = document.getElementById('checkoutComuna').value;
    const subtotal = calcularSubtotal();
    
    if (!comuna) return;
    
    try {
        const response = await fetch('/api/calcular-envio', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ comuna, subtotal })
        });
        
        const data = await response.json();
        
        const costoEnvio = data.costo_envio;
        const total = subtotal + costoEnvio;
        
        document.getElementById('checkoutSubtotal').textContent = '$' + formatNumber(subtotal);
        document.getElementById('checkoutShipping').textContent = data.envio_gratis ? 'GRATIS' : '$' + formatNumber(costoEnvio);
        document.getElementById('checkoutTotal').textContent = '$' + formatNumber(total);
        
        const infoDiv = document.getElementById('deliveryInfo');
        infoDiv.className = 'delivery-info ' + (data.envio_gratis ? 'free' : '');
        infoDiv.innerHTML = `
            <i class="fas fa-info-circle"></i>
            <strong>${data.zona}</strong>: ${data.tiempo_entrega}<br>
            ${data.envio_gratis ? '¡Envío GRATIS!' : 'Costo de envío: $' + formatNumber(costoEnvio)}
            ${data.recargo_extra > 0 ? '<br><small>Incluye recargo de zona: $' + formatNumber(data.recargo_extra) + '</small>' : ''}
        `;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function submitCheckout(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const usarDireccionGuardada = !document.getElementById('otraDireccion').checked;
    
    const orderData = {
        usar_direccion_guardada: usarDireccionGuardada,
        nombre: formData.get('nombre'),
        telefono: formData.get('telefono'),
        email: formData.get('email'),
        direccion: formData.get('direccion'),
        comuna: formData.get('comuna'),
        observaciones: formData.get('observaciones'),
        metodoPago: formData.get('pago'),
        horario: formData.get('horario'),
        items: carrito
    };
    
    try {
        const response = await fetch('/api/orden', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(orderData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarExito(data.orden_id, data.total, data.tiempo_entrega);
        } else {
            mostrarNotificacion(data.error || 'Error al procesar orden', 'error');
        }
    } catch (error) {
        mostrarNotificacion('Error de conexión', 'error');
    }
}

function mostrarExito(ordenId, total, tiempoEntrega) {
    document.getElementById('checkoutView').classList.add('hidden');
    document.getElementById('successView').classList.remove('hidden');
    
    document.getElementById('orderId').textContent = ordenId;
    document.getElementById('successTotal').textContent = '$' + formatNumber(total);
    document.getElementById('successTiempo').textContent = tiempoEntrega;
    
    // Limpiar carrito
    carrito = [];
    actualizarContador();
    localStorage.removeItem('carrito');
}

function continuarComprando() {
    closeCart();
    document.getElementById('successView').classList.add('hidden');
    document.getElementById('cartView').style.display = 'block';
}

// ========== PERFIL ==========
function verPerfil() {
    document.getElementById('perfilModal').classList.add('active');
    document.body.style.overflow = 'hidden';
    
    if (currentUser) {
        document.getElementById('perfilNombre').textContent = currentUser.nombre;
        document.getElementById('perfilEmail').textContent = currentUser.email;
        document.getElementById('perfilRut').textContent = currentUser.rut;
        document.getElementById('perfilTelefono').textContent = currentUser.telefono;
        document.getElementById('perfilDireccion').textContent = currentUser.direccion;
        document.getElementById('perfilComuna').textContent = currentUser.comuna;
    }
}

function cerrarPerfil() {
    document.getElementById('perfilModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function verPedidos() {
    mostrarNotificacion('Funcionalidad de pedidos próximamente', 'info');
}

// ========== MODALS FAQ/TERMS ==========
function abrirFAQ() {
    document.getElementById('faqModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function cerrarFAQ() {
    document.getElementById('faqModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function abrirTerminos() {
    document.getElementById('termsModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function cerrarTerminos() {
    document.getElementById('termsModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function abrirPrivacidad() {
    document.getElementById('privacyModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function cerrarPrivacidad() {
    document.getElementById('privacyModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

// ========== UTILIDADES ==========
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function scrollToTop() {
    window.scrollTo({top: 0, behavior: 'smooth'});
}

function mostrarNotificacion(mensaje, tipo = 'success') {
    const colors = {
        success: '#4CAF50',
        error: '#ef4444',
        info: '#4ECDC4'
    };
    
    const notif = document.createElement('div');
    notif.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        background: ${colors[tipo]};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 3000;
        font-weight: 600;
        animation: slideIn 0.3s ease;
    `;
    notif.textContent = mensaje;
    document.body.appendChild(notif);
    
    setTimeout(() => {
        notif.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// Animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);
