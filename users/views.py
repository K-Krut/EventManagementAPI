from django.core.serializers import serialize
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as error:
            return Response({"errors": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginAPIView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)

            if not serializer.is_valid():
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            response = serializer.save()
            return Response(response, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({"errors": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({"errors": 'refresh_token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as error:
            return Response({"errors": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
