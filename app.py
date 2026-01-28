from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from markupsafe import escape
import re
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Configuración de seguridad
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Clave secreta aleatoria
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Filtro personalizado para formatear números
@app.template_filter('format_number')
def format_number_filter(value):
    """Formatear números con separador de miles"""
    try:
        return "{:,}".format(int(value)).replace(",", ".")
    except (ValueError, TypeError):
        return value

# Base de datos simulada (en producción usar PostgreSQL/MySQL)
USERS_DB = {}  # {email: {password_hash, rut, nombre, telefono, direccion, comuna, verificado}}
ORDERS_DB = {}  # {order_id: {user_email, items, total, fecha, estado}}

# Configuración de WhatsApp
WHATSAPP_NUMBERS = [
    {
        'numero': '+56979693753',
        'nombre': 'Soporte Principal',
        'mensaje_default': 'Hola! Tengo una consulta sobre DrinkGo'
    },
    {
        'numero': '+56930053299',
        'nombre': 'Soporte Secundario',
        'mensaje_default': 'Hola! Necesito ayuda con mi pedido'
    }
]

# Configuración Email (SMTP)
EMAIL_CONFIG = {
    'enabled': False,  # Cambiar a True cuando configures
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'tu-email@gmail.com',  # CAMBIAR
    'password': 'tu-password-app'   # CAMBIAR
}

# Zonas de delivery con tiempos
ZONAS_DELIVERY = {
    'valparaiso': {'nombre': 'Valparaíso', 'recargo': 0, 'tiempo': '30-45 min'},
    'vina': {'nombre': 'Viña del Mar', 'recargo': 0, 'tiempo': '30-45 min'},
    'quilpue': {'nombre': 'Quilpué', 'recargo': 20000, 'tiempo': '90-120 min'},
    'villa_alemana': {'nombre': 'Villa Alemana', 'recargo': 20000, 'tiempo': '90-120 min'},
    'penablanca': {'nombre': 'Peñablanca', 'recargo': 20000, 'tiempo': '90-120 min'},
    'limache': {'nombre': 'Limache', 'recargo': 20000, 'tiempo': '90-120 min'},
    'olmue': {'nombre': 'Olmué', 'recargo': 20000, 'tiempo': '90-120 min'}
}

# Productos
PRODUCTOS = [
    {
        'id': 1, 'nombre': 'Johnnie Walker Black Label', 'precio': 25990,
        'categoria': 'whisky', 'descripcion': '750ml - Whisky Escocés Premium 12 años',
        'imagen': 'https://images.unsplash.com/photo-1569529465841-dfecdab7503b?w=500',
        'stock': 25, 'destacado': True
    },
    {
        'id': 2, 'nombre': 'Jack Daniels Old No.7', 'precio': 28990,
        'categoria': 'whisky', 'descripcion': '750ml - Tennessee Whiskey Original',
        'imagen': 'https://images.unsplash.com/photo-1527281400294-5b2ca0bc8696?w=500',
        'stock': 20
    },
    {
        'id': 3, 'nombre': 'Chivas Regal 12 Años', 'precio': 32990,
        'categoria': 'whisky', 'descripcion': '750ml - Scotch Whisky Premium',
        'imagen': 'https://images.unsplash.com/photo-1582824042922-e1dd63a29c1f?w=500',
        'stock': 15
    },
    {
        'id': 4, 'nombre': 'Absolut Vodka', 'precio': 15990,
        'categoria': 'vodka', 'descripcion': '750ml - Vodka Sueco Premium',
        'imagen': 'https://images.unsplash.com/photo-1560512823-829485e49540?w=500',
        'stock': 30
    },
    {
        'id': 5, 'nombre': 'Smirnoff Red', 'precio': 11990,
        'categoria': 'vodka', 'descripcion': '750ml - Triple Destilado',
        'imagen': 'https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=500',
        'stock': 40
    },
    {
        'id': 6, 'nombre': 'Grey Goose', 'precio': 39990,
        'categoria': 'vodka', 'descripcion': '750ml - Vodka Francés Super Premium',
        'imagen': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500',
        'stock': 12, 'destacado': True
    },
    {
        'id': 7, 'nombre': 'Bacardí Carta Blanca', 'precio': 16990,
        'categoria': 'ron', 'descripcion': '750ml - Ron Blanco Clásico',
        'imagen': 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=500',
        'stock': 35
    },
    {
        'id': 8, 'nombre': 'Havana Club 7 Años', 'precio': 22990,
        'categoria': 'ron', 'descripcion': '700ml - Ron Cubano Añejo',
        'imagen': 'https://images.unsplash.com/photo-1470337458703-46ad1756a187?w=500',
        'stock': 18
    },
    {
        'id': 9, 'nombre': 'Corona Extra Pack 12', 'precio': 12990,
        'categoria': 'cerveza', 'descripcion': '12 unidades x 355ml',
        'imagen': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=500',
        'stock': 50
    },
    {
        'id': 10, 'nombre': 'Heineken Pack 12', 'precio': 14990,
        'categoria': 'cerveza', 'descripcion': '12 unidades x 330ml',
        'imagen': 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=500',
        'stock': 45
    },
    {
        'id': 11, 'nombre': 'Casillero del Diablo Reserva', 'precio': 8990,
        'categoria': 'vino', 'descripcion': '750ml - Cabernet Sauvignon',
        'imagen': 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=500',
        'stock': 60
    },
    {
        'id': 12, 'nombre': 'Concha y Toro Gran Reserva', 'precio': 12990,
        'categoria': 'vino', 'descripcion': '750ml - Merlot Premium',
        'imagen': 'https://images.unsplash.com/photo-1586370434639-0fe43b2d32d6?w=500',
        'stock': 55
    },
    {
        'id': 13, 'nombre': 'Pisco Capel Reservado 40°', 'precio': 14990,
        'categoria': 'pisco', 'descripcion': '750ml - Premium',
        'imagen': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500',
        'stock': 35
    },
    {
        'id': 14, 'nombre': 'Alto del Carmen 43°', 'precio': 16990,
        'categoria': 'pisco', 'descripcion': '750ml - Pisco Extra',
        'imagen': 'https://images.unsplash.com/photo-1527281400294-5b2ca0bc8696?w=500',
        'stock': 28
    }
]

# Promociones
PROMOCIONES = [
    {
        'id': 101, 'nombre': 'Piscola Lista - Combo Premium', 'precio': 18990,
        'precio_normal': 25980, 'categoria': 'promociones',
        'descripcion': 'Pisco Capel 750ml + Coca Cola 3L + Limones + Hielo',
        'imagen': 'https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=500',
        'stock': 25, 'destacado': True, 'ahorro': 6990
    },
    {
        'id': 102, 'nombre': 'Terraza Combo - 2x1 Cerveza', 'precio': 24990,
        'precio_normal': 32980, 'categoria': 'promociones',
        'descripcion': 'Pack 12 Corona + Pack 12 Heineken',
        'imagen': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=500',
        'stock': 15, 'destacado': True, 'ahorro': 7990
    }
]

TODOS_PRODUCTOS = PRODUCTOS + PROMOCIONES

# ==================== FUNCIONES DE SEGURIDAD ====================

def sanitize_input(text):
    """Sanitizar entrada para prevenir XSS"""
    if not text:
        return ""
    return escape(str(text))

def validate_rut(rut):
    """Validar RUT chileno"""
    rut = rut.upper().replace(".", "").replace("-", "").strip()
    if not rut or len(rut) < 2:
        return False
    
    try:
        rut_body = rut[:-1]
        dv = rut[-1]
        
        if not rut_body.isdigit():
            return False
        
        # Calcular dígito verificador
        suma = 0
        multiplo = 2
        for r in reversed(rut_body):
            suma += int(r) * multiplo
            multiplo = multiplo + 1 if multiplo < 7 else 2
        
        dv_calculado = 11 - (suma % 11)
        if dv_calculado == 11:
            dv_calculado = '0'
        elif dv_calculado == 10:
            dv_calculado = 'K'
        else:
            dv_calculado = str(dv_calculado)
        
        return dv == dv_calculado
    except:
        return False

def validate_email(email):
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validar teléfono chileno"""
    phone = phone.replace(" ", "").replace("-", "").replace("+", "")
    return len(phone) >= 9 and phone.isdigit()

def hash_password(password):
    """Hash seguro de contraseña"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${pwd_hash.hex()}"

def verify_password(password, hash_str):
    """Verificar contraseña"""
    try:
        salt, pwd_hash = hash_str.split('$')
        new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return pwd_hash == new_hash.hex()
    except:
        return False

def send_verification_email(email, nombre):
    """Enviar email de verificación (simulado)"""
    # En producción, usar SMTP real
    verification_token = secrets.token_urlsafe(32)
    print(f"Email de verificación enviado a {email}")
    print(f"Token: {verification_token}")
    return verification_token

# ==================== RUTAS ====================

@app.route('/')
def index():
    """Página principal"""
    user = None
    if 'user_email' in session:
        user = USERS_DB.get(session['user_email'])
    
    return render_template('index.html',
                         whatsapp_numbers=WHATSAPP_NUMBERS,
                         zonas_delivery=ZONAS_DELIVERY,
                         user=user)

@app.route('/api/productos', methods=['GET'])
def get_productos():
    """Obtener productos (con búsqueda)"""
    categoria = sanitize_input(request.args.get('categoria', 'all'))
    search = sanitize_input(request.args.get('search', '')).lower()
    
    productos_filtrados = TODOS_PRODUCTOS
    
    # Filtrar por categoría
    if categoria != 'all':
        productos_filtrados = [p for p in productos_filtrados if p['categoria'] == categoria]
    
    # Filtrar por búsqueda
    if search:
        productos_filtrados = [p for p in productos_filtrados 
                             if search in p['nombre'].lower() 
                             or search in p['descripcion'].lower()
                             or search in p['categoria'].lower()]
    
    return jsonify(productos_filtrados)

@app.route('/api/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    try:
        data = request.get_json()
        
        # Sanitizar y validar
        email = sanitize_input(data.get('email', '')).lower()
        password = data.get('password', '')
        nombre = sanitize_input(data.get('nombre', ''))
        rut = sanitize_input(data.get('rut', ''))
        telefono = sanitize_input(data.get('telefono', ''))
        direccion = sanitize_input(data.get('direccion', ''))
        comuna = sanitize_input(data.get('comuna', ''))
        
        # Validaciones
        if not validate_email(email):
            return jsonify({'error': 'Email inválido'}), 400
        
        if email in USERS_DB:
            return jsonify({'error': 'Email ya registrado'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Contraseña debe tener al menos 6 caracteres'}), 400
        
        if not validate_rut(rut):
            return jsonify({'error': 'RUT inválido'}), 400
        
        if not validate_phone(telefono):
            return jsonify({'error': 'Teléfono inválido'}), 400
        
        if len(nombre) < 3:
            return jsonify({'error': 'Nombre muy corto'}), 400
        
        if len(direccion) < 5:
            return jsonify({'error': 'Dirección inválida'}), 400
        
        # Crear usuario
        USERS_DB[email] = {
            'password_hash': hash_password(password),
            'nombre': nombre,
            'rut': rut.upper(),
            'telefono': telefono,
            'direccion': direccion,
            'comuna': comuna,
            'verificado': False,
            'fecha_registro': datetime.now().isoformat(),
            'pedidos_completados': 0
        }
        
        # Enviar email de verificación
        token = send_verification_email(email, nombre)
        
        return jsonify({
            'success': True,
            'message': 'Usuario registrado. Por favor verifica tu email.',
            'email': email
        }), 201
        
    except Exception as e:
        print(f"Error en registro: {str(e)}")
        return jsonify({'error': 'Error al registrar usuario'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    try:
        data = request.get_json()
        
        email = sanitize_input(data.get('email', '')).lower()
        password = data.get('password', '')
        
        # Validar
        if not validate_email(email):
            return jsonify({'error': 'Email inválido'}), 400
        
        user = USERS_DB.get(email)
        
        if not user or not verify_password(password, user['password_hash']):
            return jsonify({'error': 'Credenciales incorrectas'}), 401
        
        # Crear sesión
        session.permanent = True
        session['user_email'] = email
        
        return jsonify({
            'success': True,
            'user': {
                'email': email,
                'nombre': user['nombre'],
                'rut': user['rut'],
                'telefono': user['telefono'],
                'direccion': user['direccion'],
                'comuna': user['comuna'],
                'verificado': user['verificado']
            }
        })
        
    except Exception as e:
        print(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error al iniciar sesión'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Cerrar sesión"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/user', methods=['GET'])
def get_user():
    """Obtener datos del usuario actual"""
    if 'user_email' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    user = USERS_DB.get(session['user_email'])
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({
        'email': session['user_email'],
        'nombre': user['nombre'],
        'rut': user['rut'],
        'telefono': user['telefono'],
        'direccion': user['direccion'],
        'comuna': user['comuna'],
        'verificado': user['verificado']
    })

@app.route('/api/calcular-envio', methods=['POST'])
def calcular_envio():
    """Calcular costo de envío"""
    try:
        data = request.get_json()
        comuna = sanitize_input(data.get('comuna', ''))
        subtotal = float(data.get('subtotal', 0))
        
        zona = ZONAS_DELIVERY.get(comuna.lower().replace(' ', '_'))
        
        if not zona:
            return jsonify({'error': 'Comuna no válida'}), 400
        
        # Envío gratis solo para Valparaíso y Viña sobre $30.000
        envio_gratis = subtotal >= 30000 and zona['recargo'] == 0
        costo_envio = 0 if envio_gratis else (2990 + zona['recargo'])
        
        return jsonify({
            'costo_envio': costo_envio,
            'envio_gratis': envio_gratis,
            'zona': zona['nombre'],
            'tiempo_entrega': zona['tiempo'],
            'recargo_extra': zona['recargo']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/orden', methods=['POST'])
def crear_orden():
    """Crear nueva orden"""
    try:
        data = request.get_json()
        
        # Verificar si usa dirección guardada o nueva
        usar_direccion_guardada = data.get('usar_direccion_guardada', True)
        
        if 'user_email' in session and usar_direccion_guardada:
            user = USERS_DB.get(session['user_email'])
            nombre = user['nombre']
            telefono = user['telefono']
            direccion = user['direccion']
            comuna = user['comuna']
            email = session['user_email']
        else:
            nombre = sanitize_input(data.get('nombre', ''))
            telefono = sanitize_input(data.get('telefono', ''))
            email = sanitize_input(data.get('email', ''))
            direccion = sanitize_input(data.get('direccion', ''))
            comuna = sanitize_input(data.get('comuna', ''))
        
        # Observaciones adicionales
        observaciones = sanitize_input(data.get('observaciones', ''))
        
        # Validar items
        items = data.get('items', [])
        if not items:
            return jsonify({'error': 'Carrito vacío'}), 400
        
        # Calcular totales
        subtotal = sum(
            next((p['precio'] for p in TODOS_PRODUCTOS if p['id'] == item['id']), 0) * item['cantidad']
            for item in items
        )
        
        zona = ZONAS_DELIVERY.get(comuna.lower().replace(' ', '_'))
        envio_gratis = subtotal >= 30000 and zona['recargo'] == 0
        costo_envio = 0 if envio_gratis else (2990 + zona['recargo'])
        total = subtotal + costo_envio
        
        # Generar ID de orden
        orden_id = f"DG{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Guardar orden
        ORDERS_DB[orden_id] = {
            'user_email': session.get('user_email'),
            'nombre': nombre,
            'telefono': telefono,
            'email': email,
            'direccion': direccion,
            'comuna': comuna,
            'observaciones': observaciones,
            'items': items,
            'subtotal': subtotal,
            'costo_envio': costo_envio,
            'total': total,
            'fecha': datetime.now().isoformat(),
            'estado': 'pendiente',
            'metodo_pago': data.get('metodoPago'),
            'tiempo_entrega': zona['tiempo']
        }
        
        return jsonify({
            'success': True,
            'orden_id': orden_id,
            'total': total,
            'tiempo_entrega': zona['tiempo'],
            'mensaje': f'Orden {orden_id} creada exitosamente'
        }), 201
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Error al procesar la orden'}), 500

@app.after_request
def set_security_headers(response):
    """Headers de seguridad"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    response.headers['Content-Security-Policy'] = "default-src 'self' https://images.unsplash.com https://cdnjs.cloudflare.com https://fonts.googleapis.com https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline'; img-src 'self' https://images.unsplash.com data:;"
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
