# accounts/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .models import CustomUser
from .serializers import UserSerializer
from .services import UserService
from apps.core.pagination import CustomPagination
from django.db import connection


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet manual para control total sobre endpoints de usuarios
    """

    def list(self, request):
        """GET /api/usuarios/ - Listar usuarios activos"""
        try:
            # consulta perezosa todavia no trae datos
            # es lazy loading solo prepara al consulta
            # se ejecuta solo si se hace algo con ella
            # ejemplo: lis .length  for in etc cosas que manejen sus datos
            users = UserService.get_active_users()
            # print("ANTES DE PAGINAR:")
            # print("Queries:", len(connection.queries))  # ✅ Debería ser 0
            # print(connection.queries)


             # 2. Aplicar paginación
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(users, request)
            # print("DESPUÉS DE PAGINAR:")
            # print("Queries:", len(connection.queries))  # ✅ Debería ser 1 (la SELECT)
            # print(connection.queries)


            # 3. Serializar solo los elementos paginados
            serializer = UserSerializer(paginated_queryset, many=True)
            # print('Usuarios ya cagados y serializados', serializer)
            # return Response({
            #     'success': True,
            #     'data': serializer.data,
            #     'message': 'Usuarios obtenidos exitosamente'
            # }, status=status.HTTP_200_OK)
            # 4. Devolver respuesta paginada
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener usuarios: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """POST /api/usuarios/ - Crear nuevo usuario"""
        try:
            # 1. Validar FORMATO con serializer
            # DeJSON a objeto python
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 2. Procesar NEGOCIO con service
            user = UserService.create_user(serializer.validated_data)

            # 3. Serializar respuesta
            # De objeto python a JSON
            response_serializer = UserSerializer(user)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Usuario creado exitosamente'
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """GET /api/usuarios/{pk}/ - Obtener usuario específico"""
        try:
            user = UserService.get_user_by_id(pk)
            if not user:
                return Response({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Usuario obtenido exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener usuario: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """PUT /api/usuarios/{pk}/ - Actualizar usuario completo"""
        try:
            # 1. Obtener usuario
            user = UserService.get_user_by_id(pk)
            if not user:
                return Response({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # 2. Validar FORMATO
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Actualizar con NEGOCIO
            updated_user = UserService.update_user(user, serializer.validated_data)

            # 4. Respuesta
            response_serializer = UserSerializer(updated_user)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Usuario actualizado exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar usuario: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        """PATCH /api/usuarios/{pk}/ - Actualizar campos específicos"""
        try:
            # 1. Obtener usuario
            user = UserService.get_user_by_id(pk)
            if not user:
                return Response({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # 2. Validar FORMATO (partial=True)
            serializer = UserSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Actualizar con NEGOCIO
            updated_user = UserService.update_user(user, serializer.validated_data)

            # 4. Respuesta
            response_serializer = UserSerializer(updated_user)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Usuario actualizado exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar usuario: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """DELETE /api/usuarios/{pk}/ - Eliminar usuario (soft delete)"""
        try:
            user = UserService.get_user_by_id(pk)
            if not user:
                return Response({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # Soft delete - marcar como inactivo
            user.is_active = False
            user.save()

            return Response({
                'success': True,
                'message': 'Usuario eliminado exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar usuario: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def authenticate(self, request):
        """POST /api/usuarios/authenticate/ - Autenticar usuario y devolver JWT tokens"""
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                return Response({
                    'success': False,
                    'message': 'Username y password son requeridos'
                }, status=status.HTTP_400_BAD_REQUEST)

            user = UserService.authenticate_user(username, password)
            if not user:
                return Response({
                    'success': False,
                    'message': 'Credenciales inválidas'
                }, status=status.HTTP_401_UNAUTHORIZED)

            # GENERAR TOKENS JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            serializer = UserSerializer(user)
            return Response({
                'success': True,
                'data': {
                    'user': serializer.data,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'token_type': 'Bearer'
                },
                'message': 'Autenticación exitosa'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error en autenticación: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """POST /api/usuarios/{pk}/change_password/ - Cambiar contraseña"""
        try:
            user = UserService.get_user_by_id(pk)
            if not user:
                return Response({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')

            if not old_password or not new_password:
                return Response({
                    'success': False,
                    'message': 'old_password y new_password son requeridos'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Verificar contraseña actual
            if not user.check_password(old_password):
                return Response({
                    'success': False,
                    'message': 'Contraseña actual incorrecta'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validar nueva contraseña
            if len(new_password) < 8:
                return Response({
                    'success': False,
                    'message': 'La nueva contraseña debe tener al menos 8 caracteres'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Actualizar contraseña
            user.set_password(new_password)
            user.save()

            return Response({
                'success': True,
                'message': 'Contraseña actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al cambiar contraseña: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """POST /api/usuarios/refresh_token/ - Renovar access token"""
        try:
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return Response({
                    'success': False,
                    'message': 'Refresh token es requerido'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Validar y renovar token
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)

                # Si ROTATE_REFRESH_TOKENS está True, también devuelve nuevo refresh
                new_refresh_token = str(refresh)

                return Response({
                    'success': True,
                    'data': {
                        'access_token': new_access_token,
                        'refresh_token': new_refresh_token,
                        'token_type': 'Bearer'
                    },
                    'message': 'Token renovado exitosamente'
                }, status=status.HTTP_200_OK)

            except TokenError as e:
                return Response({
                    'success': False,
                    'message': 'Refresh token inválido o expirado'
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al renovar token: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """POST /api/usuarios/logout/ - Cerrar sesión (simple)"""
        try:
            # Solo responder que el logout fue exitoso
            # El frontend debe limpiar los tokens
            return Response({
                'success': True,
                'message': 'Logout exitoso. Tokens removidos del cliente.'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error en logout: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
