from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from .serializers import MascotaSerializer
from .services import MascotaService

# Create your views here.

class MascotaViewSet(viewsets.ViewSet):
    """ViewSet para manejar operaciones CRUD de mascotas"""

    def list(self, request):
        """GET /api/mascotas/ - Listar mascotas"""
        try:
            residente_id = request.query_params.get('residente_id')

            if residente_id:
                mascotas = MascotaService.get_mascotas_by_residente(residente_id)
            else:
                mascotas = MascotaService.get_active_mascotas()

            # Aplicar paginación
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(mascotas, request)

            serializer = MascotaSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener mascotas: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """POST /api/mascotas/ - Crear nueva mascota"""
        try:
            serializer = MascotaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            mascota = MascotaService.create_mascota(serializer.validated_data)

            response_serializer = MascotaSerializer(mascota)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Mascota creada exitosamente'
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
        """GET /api/mascotas/{pk}/ - Obtener mascota específica"""
        try:
            mascota = MascotaService.get_mascota_by_id(pk)
            if not mascota:
                return Response({
                    'success': False,
                    'message': 'Mascota no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = MascotaSerializer(mascota)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Mascota obtenida exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener mascota: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """PUT /api/mascotas/{pk}/ - Actualizar mascota completa"""
        try:
            mascota = MascotaService.get_mascota_by_id(pk)
            if not mascota:
                return Response({
                    'success': False,
                    'message': 'Mascota no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = MascotaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_mascota = MascotaService.update_mascota(mascota, serializer.validated_data)

            response_serializer = MascotaSerializer(updated_mascota)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Mascota actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar mascota: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        """PATCH /api/mascotas/{pk}/ - Actualizar campos específicos"""
        try:
            mascota = MascotaService.get_mascota_by_id(pk)
            if not mascota:
                return Response({
                    'success': False,
                    'message': 'Mascota no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = MascotaSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_mascota = MascotaService.update_mascota(mascota, serializer.validated_data)

            response_serializer = MascotaSerializer(updated_mascota)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Mascota actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar mascota: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """DELETE /api/mascotas/{pk}/ - Eliminar mascota"""
        try:
            mascota = MascotaService.get_mascota_by_id(pk)
            if not mascota:
                return Response({
                    'success': False,
                    'message': 'Mascota no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            MascotaService.delete_mascota(mascota)

            return Response({
                'success': True,
                'message': 'Mascota eliminada exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar mascota: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """GET /api/mascotas/estadisticas/ - Estadísticas de mascotas"""
        try:
            stats = MascotaService.get_estadisticas()
            return Response({
                'success': True,
                'data': stats,
                'message': 'Estadísticas obtenidas exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener estadísticas: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
