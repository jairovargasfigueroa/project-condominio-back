from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import date
from .models import Reserva
from apps.residentes.services import ResidenteService
from apps.areas_comunes.services import AreaComunService


class ReservaService:

    @staticmethod
    @transaction.atomic
    def create_reserva(validated_data):
        residente_id = validated_data.pop('residente_id')
        area_comun_id = validated_data.pop('area_comun_id')

        residente = ResidenteService.get_residente_by_id(residente_id)
        if not residente:
            raise ValidationError("El residente especificado no existe o no está activo")

        area_comun = AreaComunService.get_area_comun_by_id(area_comun_id)
        if not area_comun:
            raise ValidationError("El área común especificada no existe")

        fecha_reserva = validated_data['fecha_reserva']
        hora_inicio = validated_data['hora_inicio']
        hora_fin = validated_data['hora_fin']

        conflictos = Reserva.objects.filter(
            area_comun=area_comun,
            fecha_reserva=fecha_reserva,
            estado__in=['pendiente', 'confirmada'],
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio
        ).exists()

        if conflictos:
            raise ValidationError("Ya existe una reserva confirmada en ese horario para esta área")

        monto_pagado = area_comun.costo if area_comun.tipo == 'pago' else 0.00

        reserva = Reserva.objects.create(
            residente=residente,
            area_comun=area_comun,
            monto_pagado=monto_pagado,
            **validated_data
        )
        return reserva

    @staticmethod
    def get_active_reservas():
        return Reserva.objects.select_related(
            'residente__usuario', 'area_comun'
        ).all().order_by('-fecha_reserva', 'hora_inicio')

    @staticmethod
    def get_reserva_by_id(reserva_id):
        try:
            return Reserva.objects.select_related(
                'residente__usuario', 'area_comun'
            ).get(id=reserva_id)
        except Reserva.DoesNotExist:
            return None

    @staticmethod
    def get_reservas_by_residente(residente_id):
        return Reserva.objects.filter(
            residente_id=residente_id
        ).select_related('area_comun').order_by('-fecha_reserva')

    @staticmethod
    def get_reservas_by_area(area_id):
        return Reserva.objects.filter(
            area_comun_id=area_id
        ).select_related('residente__usuario').order_by('-fecha_reserva')

    @staticmethod
    def get_reservas_by_estado(estado):
        return Reserva.objects.filter(
            estado=estado
        ).select_related('residente__usuario', 'area_comun').order_by('-fecha_reserva')

    @staticmethod
    def get_reservas_by_metodo_pago(metodo_pago):
        return Reserva.objects.filter(
            metodo_pago=metodo_pago
        ).select_related('residente__usuario', 'area_comun').order_by('-fecha_reserva')

    @staticmethod
    @transaction.atomic
    def update_reserva(reserva, validated_data):
        for field, value in validated_data.items():
            setattr(reserva, field, value)
        reserva.save()
        return reserva

    @staticmethod
    @transaction.atomic
    def cambiar_estado_reserva(reserva_id, nuevo_estado):
        reserva = ReservaService.get_reserva_by_id(reserva_id)
        if not reserva:
            raise ValidationError("La reserva especificada no existe")

        reserva.estado = nuevo_estado
        reserva.save()
        return reserva

    @staticmethod
    @transaction.atomic
    def delete_reserva(reserva):
        reserva.delete()

    @staticmethod
    def get_estadisticas():
        total_reservas = Reserva.objects.count()
        reservas_pendientes = Reserva.objects.filter(estado='pendiente').count()
        reservas_confirmadas = Reserva.objects.filter(estado='confirmada').count()
        reservas_completadas = Reserva.objects.filter(estado='completada').count()
        reservas_canceladas = Reserva.objects.filter(estado='cancelada').count()

        pagos_efectivo = Reserva.objects.filter(metodo_pago='efectivo').count()
        pagos_tarjeta = Reserva.objects.filter(metodo_pago='tarjeta').count()
        pagos_qr = Reserva.objects.filter(metodo_pago='qr').count()

        return {
            'total_reservas': total_reservas,
            'reservas_pendientes': reservas_pendientes,
            'reservas_confirmadas': reservas_confirmadas,
            'reservas_completadas': reservas_completadas,
            'reservas_canceladas': reservas_canceladas,
            'pagos_efectivo': pagos_efectivo,
            'pagos_tarjeta': pagos_tarjeta,
            'pagos_qr': pagos_qr,
        }
