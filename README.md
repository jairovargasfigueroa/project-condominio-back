# Django REST API Base Project

Proyecto base para desarrollar APIs REST con Django, organizado y listo para usar como template en nuevos proyectos.

## 🚀 Características

- ✅ **Django 5.2.5** con Django REST Framework
- ✅ **Autenticación JWT** completa (login, refresh, logout)
- ✅ **Apps organizadas** en carpeta `apps/` para mejor estructura
- ✅ **Paginación reutilizable** en `apps/core/`
- ✅ **Modelo de usuario personalizado** con campos adicionales
- ✅ **CORS configurado** para desarrollo frontend
- ✅ **PostgreSQL** como base de datos
- ✅ **Arquitectura en capas** (Views, Services, Serializers)

## 📁 Estructura del Proyecto

```
project-demo-django/
├── apps/
│   ├── core/                   # Funcionalidades comunes
│   │   ├── pagination.py       # Paginación reutilizable
│   │   └── ...
│   └── usuarios/               # Gestión de usuarios
│       ├── models.py           # Modelo CustomUser
│       ├── views.py            # ViewSet con endpoints REST
│       ├── services.py         # Lógica de negocio
│       ├── serializers.py      # Validaciones
│       └── ...
├── project_condominio/         # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── requirements.txt            # Dependencias
├── manage.py
└── README.md
```

## ⚡ Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd project-demo-django
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 5. Ejecutar servidor
```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## 📡 Endpoints Disponibles

### Autenticación
- `POST /api/usuarios/authenticate/` - Login (devuelve JWT tokens)
- `POST /api/usuarios/refresh_token/` - Renovar access token
- `POST /api/usuarios/logout/` - Logout

### Gestión de Usuarios
- `GET /api/usuarios/` - Listar usuarios (con paginación)
- `POST /api/usuarios/` - Crear usuario
- `GET /api/usuarios/{id}/` - Obtener usuario específico
- `PUT /api/usuarios/{id}/` - Actualizar usuario completo
- `PATCH /api/usuarios/{id}/` - Actualizar campos específicos
- `DELETE /api/usuarios/{id}/` - Eliminar usuario (soft delete)
- `POST /api/usuarios/{id}/change_password/` - Cambiar contraseña

### Paginación
Todos los endpoints de listado soportan paginación:
```
GET /api/usuarios/?page=2&page_size=10
```

## 🔧 Configuración

### Base de Datos
El proyecto está configurado para PostgreSQL. Actualiza las credenciales en `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tu_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### JWT Tokens
- **Access Token**: 1 hora de duración
- **Refresh Token**: 7 días de duración
- **Rotación automática**: Habilitada

## 🏗️ Arquitectura

### Patrón de Capas
- **Views**: Manejo de requests/responses y validaciones de formato
- **Services**: Lógica de negocio y validaciones específicas
- **Models**: Definición de datos y estructura de BD
- **Serializers**: Validación y serialización de datos

### Ejemplo de uso:
```python
# View maneja el request
def create(self, request):
    serializer = UserSerializer(data=request.data)  # Validación formato
    user = UserService.create_user(serializer.validated_data)  # Lógica negocio
    return Response(UserSerializer(user).data)  # Respuesta
```

## 🎯 Uso como Template

Este proyecto está diseñado para ser usado como base para nuevos proyectos:

1. **Clona** este repositorio
2. **Renombra** el proyecto y carpetas según tu necesidad
3. **Actualiza** la configuración en `settings.py`
4. **Agrega** tus propias apps en la carpeta `apps/`
5. **Desarrolla** tu funcionalidad específica

## 🤝 Contribución

Si encuentras mejoras o tienes sugerencias:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

## 🛠️ Stack Tecnológico

- **Backend**: Django 5.2.5
- **API**: Django REST Framework 3.16.1
- **Autenticación**: JWT (djangorestframework-simplejwt 5.5.1)
- **Base de Datos**: PostgreSQL
- **CORS**: django-cors-headers 4.7.0
- **Python**: 3.12+

---

⭐ **¡Si este proyecto te fue útil, dale una estrella!** ⭐