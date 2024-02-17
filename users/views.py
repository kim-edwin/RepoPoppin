import jwt
import requests
import asyncio
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from .serializers import PrivateUserSerializer
from .models import User

class Me(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user).data
        return Response(serializer)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class Users(APIView):
    def post(self, request):
        password = request.data.get('password')
        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(
            data=request.data
        )
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password) #유저 패스워드 해쉬화해서 저장
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class PublicUser(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)
    
class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class LogIn(APIView):

    def post(self, request):
        username = request.data.get('username')
        print(username)
        password = request.data.get('password')
        print(password)
        if not username or not password:
            raise ParseError
        user = authenticate(
            request, 
            username=username, 
            password=password,
            )
        print(user)
        if user:
            login(request, user)
            print("ok")
            return Response({"ok": "Welcome!"})
        else:
            print("error")
            return Response({"error": "wrong password"})
        
class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok":"bye!"})

class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(
            request, 
            username=username, 
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk" : user.pk}, 
                settings.SECRET_KEY, 
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})
        
class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=60d345cd98fcc45c5bda&client_secret={settings.GH_SECRET}",
                headers={
                    "Accept": "application/json"
                    },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            print(f"==================={user_data}")
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()
            print(f"{user_emails}")
            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login")+"_"+str(user_data.get("id")),
                    email=user_emails[0]["email"],
                    name = user_data.get("name") if user_data.get("name") else "No Name",
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class KakaoLogIn(APIView):

    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token", 
                headers={
                    "Content-type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id" : "d166f87c9d3f4176d1b79841064ba8d4",
                    "redirect_uri" : "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            access_token =  access_token.json().get("access_token");
            user_data = requests.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                    },
                )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email") if kakao_account.get("email") else "No Email",
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class SignUp(APIView):
    def post(self, request):
        try:
            name = request.data.get("name")
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")

            print(
                f"\n\nname: {name}\nusername: {username}\npassword: {password}\nemail: {email}\n\n"
            )

            # name and password are could be overlap
            # but, username and email are could't be overlap

            if User.objects.filter(username=username):
                return Response(
                    {"fail": "이미 사용중인 username 입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if User.objects.filter(email=email):
                return Response(
                    {"fail": "이미 사용중인 email 입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create(
                email=email,
                name=name,
                username=username,
            )
            user.set_password(password)
            user.save()
            login(request, user)
            return Response(
                {
                    "success": "회원가입 성공!",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"fail": "오류가 발생했습니다. 관리자에게 문의하세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )