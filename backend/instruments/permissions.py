from rest_framework.permissions import BasePermission

class CanUpdateBookingStatus(BasePermission):
    """
    Permissão para permitir que apenas o dono do instrumento ou
    o usuário que fez a reserva possam atualizar o status.
    """
    message = "Você não tem permissão para alterar o status deste agendamento."

    def has_object_permission(self, request, view, obj):
        # `obj` aqui é a instância de InstrumentBookings
        
        # Permite se o usuário logado for o mesmo que fez a reserva (aluno)
        is_booker = obj.user_id == request.user
        
        # Permite se o usuário logado for o dono do instrumento (professor/ONG)
        is_instrument_owner = obj.instrument_id.user_id == request.user

        return is_booker or is_instrument_owner
