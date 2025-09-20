from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from .serializers import VehiculoSerializer
from .services import VehiculoService


class VehiculoViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            usuario_id = request.query_params.get('usuario_id')

            if usuario_id:
                vehiculos = VehiculoService.get_vehiculos_by_usuario(usuario_id)
            else:
                vehiculos = VehiculoService.get_active_vehiculos()

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(vehiculos, request)

            serializer = VehiculoSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener vehículos: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            serializer = VehiculoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            vehiculo = VehiculoService.create_vehiculo(serializer.validated_data)

            response_serializer = VehiculoSerializer(vehiculo)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Vehículo creado exitosamente'
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
            vehiculo = VehiculoService.get_vehiculo_by_id(pk)
            if not vehiculo:
                return Response({
                    'success': False,
                    'message': 'Vehículo no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = VehiculoSerializer(vehiculo)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Vehículo obtenido exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener vehículo: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            vehiculo = VehiculoService.get_vehiculo_by_id(pk)
            if not vehiculo:
                return Response({
                    'success': False,
                    'message': 'Vehículo no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = VehiculoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_vehiculo = VehiculoService.update_vehiculo(vehiculo, serializer.validated_data)

            response_serializer = VehiculoSerializer(updated_vehiculo)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Vehículo actualizado exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar vehículo: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        try:
            vehiculo = VehiculoService.get_vehiculo_by_id(pk)
            if not vehiculo:
                return Response({
                    'success': False,
                    'message': 'Vehículo no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = VehiculoSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_vehiculo = VehiculoService.update_vehiculo(vehiculo, serializer.validated_data)

            response_serializer = VehiculoSerializer(updated_vehiculo)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Vehículo actualizado exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar vehículo: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            vehiculo = VehiculoService.get_vehiculo_by_id(pk)
            if not vehiculo:
                return Response({
                    'success': False,
                    'message': 'Vehículo no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            VehiculoService.delete_vehiculo(vehiculo)

            return Response({
                'success': True,
                'message': 'Vehículo eliminado exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar vehículo: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        try:
            stats = VehiculoService.get_estadisticas()
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
