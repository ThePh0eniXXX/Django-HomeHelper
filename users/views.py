from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserGroup, GroupMembership
from .serializers import GroupSerializer, GroupJoinSerializer

class GroupCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        group = serializer.save()
        # Автоматически добавляем создателя как администратора
        GroupMembership.objects.create(user=self.request.user, group=group, role='admin')

class GroupMembersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer  # или создайте специальный сериализатор для отображения участников

    def get_queryset(self):
        # Предположим, что группой является та, в которой состоит пользователь
        return UserGroup.objects.filter(memberships__user=self.request.user)

class GroupJoinView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupJoinSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation_code = serializer.validated_data['invitation_code']
        try:
            group = UserGroup.objects.get(invitation_code=invitation_code)
        except UserGroup.DoesNotExist:
            return Response({"detail": "Invalid invitation code."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        # Проверяем, не состоит ли пользователь уже в группе
        if GroupMembership.objects.filter(user=user, group=group).exists():
            return Response({"detail": "You are already a member of this group."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем запись членства с ролью по умолчанию ('member')
        GroupMembership.objects.create(user=user, group=group, role='member')
        return Response({"detail": "Successfully joined the group."}, status=status.HTTP_200_OK)