from rest_framework import serializers
from .models import LecturaComunicado
from apps.residentes.serializers import ResidenteSerializer
from apps.comunicados.serializers import ComunicadoSerializer


class LecturaComunicadoSerializer(serializers.ModelSerializer):
    residente_info = ResidenteSerializer(source='residente', read_only=True)
    comunicado_info = ComunicadoSerializer(source='comunicado', read_only=True)

    class Meta:
        model = LecturaComunicado
        fields = ['id', 'residente', 'comunicado', 'fecha_lectura', 'residente_info', 'comunicado_info']
        read_only_fields = ['fecha_lectura']

    def validate(self, data):
        # Validar que no exista ya una lectura para este residente y comunicado
        residente = data.get('residente')
        comunicado = data.get('comunicado')

        if residente and comunicado:
            if LecturaComunicado.objects.filter(residente=residente, comunicado=comunicado).exists():
                raise serializers.ValidationError("Este residente ya marcó como leído este comunicado")

        return data

    def create(self, validated_data):
        raise NotImplementedError("Use LecturaComunicadoService.marcar_como_leido() instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Las lecturas de comunicados no se pueden modificar")


class LecturaComunicadoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturaComunicado
        fields = ['residente', 'comunicado']

    def validate(self, data):
        residente = data.get('residente')
        comunicado = data.get('comunicado')

        if residente and comunicado:
            if LecturaComunicado.objects.filter(residente=residente, comunicado=comunicado).exists():
                raise serializers.ValidationError("Este residente ya marcó como leído este comunicado")

        return data
