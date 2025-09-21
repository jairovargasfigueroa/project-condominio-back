from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from apps.copropietarios.serializers import CopropietarioSerializer
from apps.copropietarios.services import CopropietarioService

# Create your views here.

class CopropietarioViewSet(viewsets.ViewSet):

  def list(self, request):
        """GET /api/copropietarios/ - Listar copropietarios activos"""
        try:

            # Consulta perezosa - solo prepara la consulta
            copropietarios = CopropietarioService.get_active_copropietarios()

            # Aplicar paginación
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(copropietarios, request)

            # Serializar solo los elementos paginados
            serializer = CopropietarioSerializer(paginated_queryset, many=True)

            # Devolver respuesta paginada
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener copropietarios: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def create(self, request):
        """POST /api/copropietarios/ - Crear nuevo copropietario"""
        try:
            # 1. Validar FORMATO con serializer
            # De JSON a objeto python
            serializer = CopropietarioSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 2. Procesar NEGOCIO con service
            copropietario = CopropietarioService.create_copropietario(serializer.validated_data)

            # 3. Serializar respuesta
            # De objeto python a JSON
            response_serializer = CopropietarioSerializer(copropietario)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Copropietario creado exitosamente'
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
        """GET /api/copropietarios/{pk}/ - Obtener copropietario específico"""
        try:
            copropietario = CopropietarioService.get_copropietario_by_id(pk)
            if not copropietario:
                return Response({
                    'success': False,
                    'message': 'Copropietario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = CopropietarioSerializer(copropietario)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Copropietario obtenido exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener copropietario: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def update(self, request, pk=None):
        """PUT /api/copropietarios/{pk}/ - Actualizar copropietario completo"""
        try:
            # 1. Buscar copropietario
            copropietario = CopropietarioService.get_copropietario_by_id(pk)
            if not copropietario:
                return Response({
                    'success': False,
                    'message': 'Copropietario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # 2. Validar formato
            serializer = CopropietarioSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Procesar negocio
            updated_copropietario = CopropietarioService.update_copropietario(
                copropietario, serializer.validated_data
            )

            # 4. Respuesta
            response_serializer = CopropietarioSerializer(updated_copropietario)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Copropietario actualizado exitosamente'
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
        """DELETE /api/copropietarios/{pk}/ - Eliminar copropietario"""
        try:
            copropietario = CopropietarioService.get_copropietario_by_id(pk)
            if not copropietario:
                return Response({
                    'success': False,
                    'message': 'Copropietario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            CopropietarioService.delete_copropietario(copropietario)
            return Response({
                'success': True,
                'message': 'Copropietario eliminado exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar copropietario: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
