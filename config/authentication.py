import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get('Jwt')
        if not token:
            return None
        
        decoded = jwt.decode(
            token, 
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get('pk')
        if not pk:
            raise AuthenticationFailed("Invaild Token")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")