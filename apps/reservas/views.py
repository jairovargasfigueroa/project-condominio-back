from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from .serializers import ReservaSerializer
from .services import ReservaService


class ReservaViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            residente_id = request.query_params.get('residente_id')
            area_id = request.query_params.get('area_id')
            estado = request.query_params.get('estado')
            metodo_pago = request.query_params.get('metodo_pago')

            if residente_id:
                reservas = ReservaService.get_reservas_by_residente(residente_id)
            elif area_id:
                reservas = ReservaService.get_reservas_by_area(area_id)
            elif estado:
                reservas = ReservaService.get_reservas_by_estado(estado)
            elif metodo_pago:
                reservas = ReservaService.get_reservas_by_metodo_pago(metodo_pago)
            else:
                reservas = ReservaService.get_active_reservas()

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(reservas, request)

            serializer = ReservaSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener reservas: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            data = request.data.copy()

            # 🔍 LÓGICA INTELIGENTE: Si no viene residente_id, usar el usuario autenticado
            if 'residente_id' not in data or data.get('residente_id') is None:
                # Caso MÓVIL: Obtener residente del usuario autenticado
                from apps.residentes.services import ResidenteService

                residente = ResidenteService.get_residente_by_user(request.user)
                if not residente:
                    return Response({
                        'success': False,
                        'message': 'Usuario no tiene un perfil de residente asociado'
                    }, status=status.HTTP_400_BAD_REQUEST)

                data['residente_id'] = residente.id

            # Si viene residente_id, es el caso WEB (admin eligiendo residente)

            serializer = ReservaSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            reserva = ReservaService.create_reserva(serializer.validated_data)

            response_serializer = ReservaSerializer(reserva)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Reserva creada exitosamente'
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
            reserva = ReservaService.get_reserva_by_id(pk)
            if not reserva:
                return Response({
                    'success': False,
                    'message': 'Reserva no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ReservaSerializer(reserva)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Reserva obtenida exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener reserva: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            reserva = ReservaService.get_reserva_by_id(pk)
            if not reserva:
                return Response({
                    'success': False,
                    'message': 'Reserva no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ReservaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_reserva = ReservaService.update_reserva(reserva, serializer.validated_data)

            response_serializer = ReservaSerializer(updated_reserva)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Reserva actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar reserva: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        try:
            reserva = ReservaService.get_reserva_by_id(pk)
            if not reserva:
                return Response({
                    'success': False,
                    'message': 'Reserva no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ReservaSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_reserva = ReservaService.update_reserva(reserva, serializer.validated_data)

            response_serializer = ReservaSerializer(updated_reserva)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Reserva actualizada exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al actualizar reserva: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            reserva = ReservaService.get_reserva_by_id(pk)
            if not reserva:
                return Response({
                    'success': False,
                    'message': 'Reserva no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

            ReservaService.delete_reserva(reserva)

            return Response({
                'success': True,
                'message': 'Reserva eliminada exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al eliminar reserva: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        try:
            nuevo_estado = request.data.get('estado')
            if not nuevo_estado:
                return Response({
                    'success': False,
                    'message': 'Debe proporcionar el nuevo estado'
                }, status=status.HTTP_400_BAD_REQUEST)

            reserva = ReservaService.cambiar_estado_reserva(pk, nuevo_estado)

            response_serializer = ReservaSerializer(reserva)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': f'Estado cambiado a {nuevo_estado} exitosamente'
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al cambiar estado: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        try:
            stats = ReservaService.get_estadisticas()
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

    @action(detail=False, methods=['get'], url_path='mis-reservas')
    def reservas_usuario(self, request):
        """GET /api/reservas/mis-reservas/ - Obtener MIS reservas del usuario autenticado"""
        try:
            user = request.user

            # ✅ USAR SERVICE para obtener reservas del usuario autenticado
            reservas = ReservaService.get_reservas_by_user(user)

            # Aplicar paginación
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(reservas, request)

            # ✅ USAR SERIALIZER para formatear respuesta
            serializer = ReservaSerializer(paginated_queryset, many=True)

            # Devolver respuesta paginada
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener mis reservas: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
