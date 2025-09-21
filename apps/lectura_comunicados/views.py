from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from apps.core.pagination import CustomPagination
from .serializers import LecturaComunicadoSerializer, LecturaComunicadoCreateSerializer
from .services import LecturaComunicadoService


class LecturaComunicadoViewSet(viewsets.ViewSet):

    def list(self, request):
        """Lista todas las lecturas de comunicados"""
        try:
            # Obtener todas las lecturas con información relacionada
            from .models import LecturaComunicado
            lecturas = LecturaComunicado.objects.select_related(
                'residente', 'comunicado'
            ).all().order_by('-fecha_lectura')

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(lecturas, request)

            serializer = LecturaComunicadoSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener lecturas: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """Marca un comunicado como leído"""
        try:
            serializer = LecturaComunicadoCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Error en validación de formato',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            residente_id = serializer.validated_data['residente'].id
            comunicado_id = serializer.validated_data['comunicado'].id

            lectura = LecturaComunicadoService.marcar_como_leido(residente_id, comunicado_id)

            response_serializer = LecturaComunicadoSerializer(lectura)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Comunicado marcado como leído exitosamente'
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

    @action(detail=False, methods=['get'])
    def por_comunicado(self, request):
        """Obtiene lecturas de un comunicado específico"""
        try:
            comunicado_id = request.query_params.get('comunicado_id')
            if not comunicado_id:
                return Response({
                    'success': False,
                    'message': 'Debe proporcionar comunicado_id'
                }, status=status.HTTP_400_BAD_REQUEST)

            lecturas = LecturaComunicadoService.get_lecturas_por_comunicado(comunicado_id)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(lecturas, request)

            serializer = LecturaComunicadoSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener lecturas por comunicado: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def por_residente(self, request):
        """Obtiene lecturas de un residente específico"""
        try:
            residente_id = request.query_params.get('residente_id')
            if not residente_id:
                return Response({
                    'success': False,
                    'message': 'Debe proporcionar residente_id'
                }, status=status.HTTP_400_BAD_REQUEST)

            lecturas = LecturaComunicadoService.get_lecturas_por_residente(residente_id)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(lecturas, request)

            serializer = LecturaComunicadoSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener lecturas por residente: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def verificar_lectura(self, request):
        """Verifica si un residente leyó un comunicado específico"""
        try:
            residente_id = request.query_params.get('residente_id')
            comunicado_id = request.query_params.get('comunicado_id')

            if not residente_id or not comunicado_id:
                return Response({
                    'success': False,
                    'message': 'Debe proporcionar residente_id y comunicado_id'
                }, status=status.HTTP_400_BAD_REQUEST)

            leyo = LecturaComunicadoService.verificar_lectura(residente_id, comunicado_id)

            return Response({
                'success': True,
                'data': {'leyo': leyo},
                'message': 'Verificación completada'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al verificar lectura: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def estadisticas_comunicado(self, request):
        """Obtiene estadísticas de lectura de un comunicado"""
        try:
            comunicado_id = request.query_params.get('comunicado_id')
            if not comunicado_id:
                return Response({
                    'success': False,
                    'message': 'Debe proporcionar comunicado_id'
                }, status=status.HTTP_400_BAD_REQUEST)

            stats = LecturaComunicadoService.get_estadisticas_comunicado(comunicado_id)

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

    @action(detail=False, methods=['get'])
    def estadisticas_generales(self, request):
        """Obtiene estadísticas generales del sistema"""
        try:
            stats = LecturaComunicadoService.get_estadisticas_generales()

            return Response({
                'success': True,
                'data': stats,
                'message': 'Estadísticas generales obtenidas exitosamente'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener estadísticas generales: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def no_leidos(self, request):
        """Obtiene comunicados no leídos por un residente"""
        try:
            residente_id = request.query_params.get('residente_id')
            if not residente_id:
                return Response({
                    'success': False,
                    'message': 'Debe proporcionar residente_id'
                }, status=status.HTTP_400_BAD_REQUEST)

            comunicados = LecturaComunicadoService.get_comunicados_no_leidos_por_residente(residente_id)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(comunicados, request)

            from apps.comunicados.serializers import ComunicadoSerializer
            serializer = ComunicadoSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error al obtener comunicados no leídos: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
