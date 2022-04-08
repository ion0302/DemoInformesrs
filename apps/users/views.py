
from django.contrib.auth.models import User
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.viewsets import GenericViewSet

from apps.users.serializers import UserSerializer, UserListSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop('password')
        user = serializer.save()
        user.set_password(password)
        user.save()

        return Response(data=UserSerializer(user).data)


class UserListViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()
