from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from apps.residentes.serializers import ResidenteSerializer
from apps.residentes.services import ResidenteService

# Create your views here.

class ResidenteViewSet(viewsets.ViewSet):


  def list(self, request):
        """GET /api/residentes/ - Listar residentes activos"""
        try:

            # Consulta perezosa - solo prepara la consulta
            residentes = ResidenteService.get_active_residentes()

            # Aplicar paginación
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(residentes, request)

            # Serializar solo los elementos paginados
            serializer = ResidenteSerializer(paginated_queryset, many=True)

            # Devolver respuesta paginada
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener residentes: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def create(self, request):
        """POST /api/residentes/ - Crear nuevo residente"""
        try:
            # 1. Validar FORMATO con serializer
            # De JSON a objeto python
            serializer = ResidenteSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 2. Procesar NEGOCIO con service
            residente = ResidenteService.create_residente(serializer.validated_data)

            # 3. Serializar respuesta
            # De objeto python a JSON
            response_serializer = ResidenteSerializer(residente)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Residente creado exitosamente'
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
        """GET /api/residentes/{pk}/ - Obtener residente específico"""
        try:
            residente = ResidenteService.get_residente_by_id(pk)
            if not residente:
                return Response({
                    'success': False,
                    'message': 'Residente no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ResidenteSerializer(residente)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Residente obtenido exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener residente: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def update(self, request, pk=None):
        """PUT /api/residentes/{pk}/ - Actualizar residente completo"""
        try:
            # 1. Obtener residente
            residente = ResidenteService.get_residente_by_id(pk)
            if not residente:
                return Response({
                    'success': False,
                    'message': 'Residente no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # 2. Validar FORMATO
            serializer = ResidenteSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Actualizar con NEGOCIO
            updated_residente = ResidenteService.update_residente(residente, serializer.validated_data)

            # 4. Respuesta
            response_serializer = ResidenteSerializer(updated_residente)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Residente actualizado exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar residente: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def partial_update(self, request, pk=None):
        """PATCH /api/residentes/{pk}/ - Actualizar campos específicos"""
        try:
            # 1. Obtener residente
            residente = ResidenteService.get_residente_by_id(pk)
            if not residente:
                return Response({
                    'success': False,
                    'message': 'Residente no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # 2. Validar FORMATO (partial=True)
            serializer = ResidenteSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Actualizar con NEGOCIO
            updated_residente = ResidenteService.update_residente(residente, serializer.validated_data)

            # 4. Respuesta
            response_serializer = ResidenteSerializer(updated_residente)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Residente actualizado exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar residente: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def destroy(self, request, pk=None):
        """DELETE /api/residentes/{pk}/ - Eliminar residente (soft delete)"""
        try:
            residente = ResidenteService.get_residente_by_id(pk)
            if not residente:
                return Response({
                    'success': False,
                    'message': 'Residente no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            # Eliminar residente (puede incluir soft delete del usuario)
            ResidenteService.delete_residente(residente)

            return Response({
                'success': True,
                'message': 'Residente eliminado exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar residente: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  @action(detail=False, methods=['get'])
  def estadisticas(self, request):
        """GET /api/residentes/estadisticas/ - Obtener estadísticas de residentes"""
        try:
            stats = ResidenteService.get_estadisticas()
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

  @action(detail=True, methods=['post'])
  def cambiar_zona(self, request, pk=None):
        """POST /api/residentes/{pk}/cambiar_zona/ - Cambiar zona del residente"""
        try:
            residente = ResidenteService.get_residente_by_id(pk)
            if not residente:
                return Response({
                    'success': False,
                    'message': 'Residente no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

            nueva_zona = request.data.get('zona')
            if not nueva_zona:
                return Response({
                    'success': False,
                    'message': 'La zona es requerida'
                }, status=status.HTTP_400_BAD_REQUEST)

            residente_actualizado = ResidenteService.cambiar_zona(residente, nueva_zona)

            serializer = ResidenteSerializer(residente_actualizado)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Zona cambiada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al cambiar zona: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
