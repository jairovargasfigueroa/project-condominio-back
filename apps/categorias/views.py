from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from .serializers import CategoriaSerializer
from .services import CategoriaService


class CategoriaViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            categorias = CategoriaService.get_active_categorias()

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(categorias, request)

            serializer = CategoriaSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener categorías: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            serializer = CategoriaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            categoria = CategoriaService.create_categoria(serializer.validated_data)

            response_serializer = CategoriaSerializer(categoria)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Categoría creada exitosamente'
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
            categoria = CategoriaService.get_categoria_by_id(pk)
            if not categoria:
                return Response({
                    'success': False,
                    'message': 'Categoría no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = CategoriaSerializer(categoria)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Categoría obtenida exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener categoría: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            categoria = CategoriaService.get_categoria_by_id(pk)
            if not categoria:
                return Response({
                    'success': False,
                    'message': 'Categoría no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = CategoriaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_categoria = CategoriaService.update_categoria(categoria, serializer.validated_data)

            response_serializer = CategoriaSerializer(updated_categoria)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Categoría actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar categoría: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        try:
            categoria = CategoriaService.get_categoria_by_id(pk)
            if not categoria:
                return Response({
                    'success': False,
                    'message': 'Categoría no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = CategoriaSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_categoria = CategoriaService.update_categoria(categoria, serializer.validated_data)

            response_serializer = CategoriaSerializer(updated_categoria)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Categoría actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar categoría: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            categoria = CategoriaService.get_categoria_by_id(pk)
            if not categoria:
                return Response({
                    'success': False,
                    'message': 'Categoría no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            CategoriaService.delete_categoria(categoria)

            return Response({
                'success': True,
                'message': 'Categoría eliminada exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar categoría: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        try:
            stats = CategoriaService.get_estadisticas()
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
