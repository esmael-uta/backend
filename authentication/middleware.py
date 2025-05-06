from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


class TokenRefreshMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 401 and 'refresh_token' in request.COOKIES:
            try:
                refresh_token = request.COOKIES.get('refresh_token')

                refresh = RefreshToken(refresh_token)

                new_access_token = str(refresh.access_token)

                response.set_cookie(
                    'access_token',
                    new_access_token,
                    httponly=True,
                    samesite='Lax',
                    secure=True,
                    max_age=60 * 60  # 1 hour
                )

                return JsonResponse({'detail': 'Token refreshed, please retry request'}, status=200)

            except Exception as e:
                response.delete_cookie('access_token')
                response.delete_cookie('refresh_token')

        return response
