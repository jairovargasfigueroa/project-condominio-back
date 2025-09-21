from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from .serializers import AreaComunSerializer
from .services import AreaComunService


class AreaComunViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            tipo = request.query_params.get('tipo')

            if tipo:
                areas = AreaComunService.get_areas_by_tipo(tipo)
            else:
                areas = AreaComunService.get_active_areas_comunes()

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(areas, request)

            serializer = AreaComunSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener áreas comunes: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            serializer = AreaComunSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            area_comun = AreaComunService.create_area_comun(serializer.validated_data)

            response_serializer = AreaComunSerializer(area_comun)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Área común creada exitosamente'
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
        try:
            area_comun = AreaComunService.get_area_comun_by_id(pk)
            if not area_comun:
                return Response({
                    'success': False,
                    'message': 'Área común no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = AreaComunSerializer(area_comun)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Área común obtenida exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener área común: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            area_comun = AreaComunService.get_area_comun_by_id(pk)
            if not area_comun:
                return Response({
                    'success': False,
                    'message': 'Área común no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = AreaComunSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_area = AreaComunService.update_area_comun(area_comun, serializer.validated_data)

            response_serializer = AreaComunSerializer(updated_area)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Área común actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar área común: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        try:
            area_comun = AreaComunService.get_area_comun_by_id(pk)
            if not area_comun:
                return Response({
                    'success': False,
                    'message': 'Área común no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = AreaComunSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_area = AreaComunService.update_area_comun(area_comun, serializer.validated_data)

            response_serializer = AreaComunSerializer(updated_area)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Área común actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar área común: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            area_comun = AreaComunService.get_area_comun_by_id(pk)
            if not area_comun:
                return Response({
                    'success': False,
                    'message': 'Área común no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            AreaComunService.delete_area_comun(area_comun)

            return Response({
                'success': True,
                'message': 'Área común eliminada exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar área común: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        try:
            stats = AreaComunService.get_estadisticas()
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
