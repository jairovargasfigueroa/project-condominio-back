from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from apps.administradores.serializers import AdministradorSerializer
from apps.administradores.services import AdministradorService

# Create your views here.

class AdministradorViewSet(viewsets.ViewSet):

    def list(self, request):
        """GET /api/administradores/ - Listar administradores activos"""
        try:

            # Consulta perezosa - solo prepara la consulta
            administradores = AdministradorService.get_active_administradores()

            # Aplicar paginación
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(administradores, request)

            # Serializar solo los elementos paginados
            serializer = AdministradorSerializer(paginated_queryset, many=True)

            # Devolver respuesta paginada
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener administradores: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """POST /api/administradores/ - Crear nuevo administrador"""
        try:
            # 1. Validar FORMATO con serializer
            # De JSON a objeto python
            serializer = AdministradorSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 2. Procesar NEGOCIO con service
            administrador = AdministradorService.create_administrador(serializer.validated_data)

            # 3. Serializar respuesta
            # De objeto python a JSON
            response_serializer = AdministradorSerializer(administrador)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Administrador creado exitosamente'
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
        """GET /api/administradores/{pk}/ - Obtener administrador específico"""
        try:
            administrador = AdministradorService.get_administrador_by_id(pk)
            if not administrador:
                return Response({
                    'success': False,
                    'message': 'Administrador no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = AdministradorSerializer(administrador)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Administrador obtenido exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener administrador: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """PUT /api/administradores/{pk}/ - Actualizar administrador completo"""
        try:
            # 1. Buscar administrador
            administrador = AdministradorService.get_administrador_by_id(pk)
            if not administrador:
                return Response({
                    'success': False,
                    'message': 'Administrador no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # 2. Validar formato
            serializer = AdministradorSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Procesar negocio
            updated_administrador = AdministradorService.update_administrador(
                administrador, serializer.validated_data
            )

            # 4. Respuesta
            response_serializer = AdministradorSerializer(updated_administrador)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Administrador actualizado exitosamente'
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
        """DELETE /api/administradores/{pk}/ - Eliminar administrador"""
        try:
            administrador = AdministradorService.get_administrador_by_id(pk)
            if not administrador:
                return Response({
                    'success': False,
                    'message': 'Administrador no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            AdministradorService.delete_administrador(administrador)
            return Response({
                'success': True,
                'message': 'Administrador eliminado exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar administrador: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """GET /api/administradores/search/?q=query - Buscar administradores"""
        try:
            query = request.query_params.get('q', '')
            if not query:
                return Response({
                    'success': False,
                    'message': 'Parámetro de búsqueda requerido'
                }, status=status.HTTP_400_BAD_REQUEST)

            administradores = AdministradorService.search_administradores(query)

            # Aplicar paginación
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(administradores, request)

            serializer = AdministradorSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error en búsqueda: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
