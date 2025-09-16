from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

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
