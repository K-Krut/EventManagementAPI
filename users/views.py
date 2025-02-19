from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import UserRegisterSerializer


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
