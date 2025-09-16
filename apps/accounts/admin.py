from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, Permission
from .models import CustomUser

# Registrar CustomUser con mejor interfaz
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin personalizado para CustomUser"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Agregar campos personalizados al formulario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('telefono', 'fecha_nacimiento')
        }),
    )

# Personalizar admin de Groups para mostrar usuarios
class CustomGroupAdmin(GroupAdmin):
    """Admin personalizado para Groups"""
    filter_horizontal = ('permissions',)
    list_display = ('name', 'get_users_count')
    
    def get_users_count(self, obj):
        return obj.user_set.count()
    get_users_count.short_description = 'Usuarios en este grupo'

# Registrar Permission para que sea visible
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin para ver permisos"""
    list_display = ('name', 'codename', 'content_type')
    list_filter = ('content_type',)
    search_fields = ('name', 'codename')

# Re-registrar Group con la configuración personalizada
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
