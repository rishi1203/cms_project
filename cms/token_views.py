from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status

class ObtainCustomTokenPairView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                "access": access_token,
                "refresh": refresh_token
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class RefreshCustomTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({
                "access": access_token
            })
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
