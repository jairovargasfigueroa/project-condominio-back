from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from .serializers import ViviendaSerializer
from .services import ViviendaService


class ViviendaViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            categoria_id = request.query_params.get('categoria_id')
            numero = request.query_params.get('numero')

            if categoria_id:
                viviendas = ViviendaService.get_viviendas_by_categoria(categoria_id)
            elif numero:
                viviendas = ViviendaService.get_viviendas_by_numero(numero)
            else:
                viviendas = ViviendaService.get_active_viviendas()

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(viviendas, request)

            serializer = ViviendaSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener viviendas: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            serializer = ViviendaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            vivienda = ViviendaService.create_vivienda(serializer.validated_data)

            response_serializer = ViviendaSerializer(vivienda)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Vivienda creada exitosamente'
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
            vivienda = ViviendaService.get_vivienda_by_id(pk)
            if not vivienda:
                return Response({
                    'success': False,
                    'message': 'Vivienda no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ViviendaSerializer(vivienda)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Vivienda obtenida exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener vivienda: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            vivienda = ViviendaService.get_vivienda_by_id(pk)
            if not vivienda:
                return Response({
                    'success': False,
                    'message': 'Vivienda no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ViviendaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_vivienda = ViviendaService.update_vivienda(vivienda, serializer.validated_data)

            response_serializer = ViviendaSerializer(updated_vivienda)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Vivienda actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar vivienda: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        try:
            vivienda = ViviendaService.get_vivienda_by_id(pk)
            if not vivienda:
                return Response({
                    'success': False,
                    'message': 'Vivienda no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ViviendaSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_vivienda = ViviendaService.update_vivienda(vivienda, serializer.validated_data)

            response_serializer = ViviendaSerializer(updated_vivienda)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Vivienda actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar vivienda: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            vivienda = ViviendaService.get_vivienda_by_id(pk)
            if not vivienda:
                return Response({
                    'success': False,
                    'message': 'Vivienda no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            ViviendaService.delete_vivienda(vivienda)

            return Response({
                'success': True,
                'message': 'Vivienda eliminada exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar vivienda: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        try:
            stats = ViviendaService.get_estadisticas()
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
