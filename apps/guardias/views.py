from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from apps.guardias.serializers import GuardiaSerializer
from apps.guardias.services import GuardiaService

# Create your views here.

class GuardiaViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """GET /api/guardias/ - Listar guardias activos"""
        try:

            # Consulta perezosa - solo prepara la consulta
            guardias = GuardiaService.get_active_guardias()

            # Aplicar paginación
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(guardias, request)

            # Serializar solo los elementos paginados
            serializer = GuardiaSerializer(paginated_queryset, many=True)

            # Devolver respuesta paginada
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener guardias: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """POST /api/guardias/ - Crear nuevo guardia"""
        try:
            # 1. Validar FORMATO con serializer
            # De JSON a objeto python
            serializer = GuardiaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 2. Procesar NEGOCIO con service
            guardia = GuardiaService.create_guardia(serializer.validated_data)

            # 3. Serializar respuesta
            # De objeto python a JSON
            response_serializer = GuardiaSerializer(guardia)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Guardia creado exitosamente'
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
        """GET /api/guardias/{pk}/ - Obtener guardia específico"""
        try:
            guardia = GuardiaService.get_guardia_by_id(pk)
            if not guardia:
                return Response({
                    'success': False,
                    'message': 'Guardia no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = GuardiaSerializer(guardia)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Guardia obtenido exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener guardia: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """PUT /api/guardias/{pk}/ - Actualizar guardia completo"""
        try:
            # 1. Buscar guardia
            guardia = GuardiaService.get_guardia_by_id(pk)
            if not guardia:
                return Response({
                    'success': False,
                    'message': 'Guardia no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # 2. Validar formato
            serializer = GuardiaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Procesar negocio
            updated_guardia = GuardiaService.update_guardia(
                guardia, serializer.validated_data
            )

            # 4. Respuesta
            response_serializer = GuardiaSerializer(updated_guardia)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Guardia actualizado exitosamente'
            }, status=status.HTTP_200_OK)

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

    def destroy(self, request, pk=None):
        """DELETE /api/guardias/{pk}/ - Eliminar guardia"""
        try:
            guardia = GuardiaService.get_guardia_by_id(pk)
            if not guardia:
                return Response({
                    'success': False,
                    'message': 'Guardia no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            GuardiaService.delete_guardia(guardia)
            return Response({
                'success': True,
                'message': 'Guardia eliminado exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar guardia: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """GET /api/guardias/search/?q=query - Buscar guardias"""
        try:
            query = request.query_params.get('q', '')
            if not query:
                return Response({
                    'success': False,
                    'message': 'Parámetro de búsqueda requerido'
                }, status=status.HTTP_400_BAD_REQUEST)

            guardias = GuardiaService.search_guardias(query)

            # Aplicar paginación
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(guardias, request)

            serializer = GuardiaSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error en búsqueda: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def perfil(self, request):
        """GET /api/guardias/perfil/ - Obtener MI perfil de guardia autenticado"""
        try:
            user = request.user

            # ✅ USAR SERVICE para obtener datos (siguiendo tu patrón)
            guardia = GuardiaService.get_guardia_by_user(user)

            if not guardia:
                return Response({
                    'success': False,
                    'message': 'Usuario no tiene perfil de guardia asociado'
                }, status=status.HTTP_404_NOT_FOUND)

            # ✅ USAR SERIALIZER para formatear respuesta (siguiendo tu patrón)
            # Tu serializer ya tiene usuario = UserSerializer() anidado
            serializer = GuardiaSerializer(guardia)

            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Perfil obtenido exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener perfil: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
