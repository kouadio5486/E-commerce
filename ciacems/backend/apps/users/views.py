from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.serializers import RegisterSerializer


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token requis"}, status=400)
        try:
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        return Response({"message": "Déconnexion réussie"})
