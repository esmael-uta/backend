from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            response.set_cookie(
                'access_token',
                response.data['access'],
                httponly=True,
                samesite='Lax',
                secure=True,
                max_age=60 * 60  # 1 hour
            )
            del response.data['access']

        if response.data.get('refresh'):
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
                httponly=True,
                samesite='Lax',
                secure=True,
                max_age=60 * 60 * 24 * 30
            )
            del response.data['refresh']

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            response.set_cookie(
                'access_token',
                response.data['access'],
                httponly=True,
                samesite='Lax',
                secure=True,
                max_age=60 * 60
            )
            del response.data['access']

        return super().finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            request.data['refresh'] = refresh_token

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request):
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
