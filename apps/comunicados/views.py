from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from .serializers import ComunicadoSerializer
from .services import ComunicadoService


class ComunicadoViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            comunicados = ComunicadoService.get_all_comunicados()

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(comunicados, request)

            serializer = ComunicadoSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener comunicados: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            serializer = ComunicadoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            comunicado = ComunicadoService.create_comunicado(serializer.validated_data)

            response_serializer = ComunicadoSerializer(comunicado)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Comunicado creado exitosamente'
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
            comunicado = ComunicadoService.get_comunicado_by_id(pk)
            if not comunicado:
                return Response({
                    'success': False,
                    'message': 'Comunicado no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ComunicadoSerializer(comunicado)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Comunicado obtenido exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener comunicado: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            comunicado = ComunicadoService.get_comunicado_by_id(pk)
            if not comunicado:
                return Response({
                    'success': False,
                    'message': 'Comunicado no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ComunicadoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_comunicado = ComunicadoService.update_comunicado(comunicado, serializer.validated_data)

            response_serializer = ComunicadoSerializer(updated_comunicado)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Comunicado actualizado exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar comunicado: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        try:
            comunicado = ComunicadoService.get_comunicado_by_id(pk)
            if not comunicado:
                return Response({
                    'success': False,
                    'message': 'Comunicado no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ComunicadoSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_comunicado = ComunicadoService.update_comunicado(comunicado, serializer.validated_data)

            response_serializer = ComunicadoSerializer(updated_comunicado)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Comunicado actualizado exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar comunicado: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            comunicado = ComunicadoService.get_comunicado_by_id(pk)
            if not comunicado:
                return Response({
                    'success': False,
                    'message': 'Comunicado no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            ComunicadoService.delete_comunicado(comunicado)

            return Response({
                'success': True,
                'message': 'Comunicado eliminado exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar comunicado: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def recientes(self, request):
        try:
            limit = int(request.query_params.get('limit', 10))
            comunicados = ComunicadoService.get_comunicados_recientes(limit)
            serializer = ComunicadoSerializer(comunicados, many=True)

            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Comunicados recientes obtenidos exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener comunicados recientes: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        try:
            titulo = request.query_params.get('titulo', '')
            if not titulo:
                return Response({
                    'success': False,
                    'message': 'Debe proporcionar un título para buscar'
                }, status=status.HTTP_400_BAD_REQUEST)

            comunicados = ComunicadoService.get_comunicados_by_titulo(titulo)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(comunicados, request)

            serializer = ComunicadoSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al buscar comunicados: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        try:
            stats = ComunicadoService.get_estadisticas()
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
