from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#장고가 기본으로 생성하는 유저 admin 클래스를 가져와서 커스터마이즈하여 사용한다.
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar", 
                    "username", 
                    "password", 
                    "name", 
                    "email",
                    ),
                    "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login", "date_joined"
                ),
            },
        )
    )
    
    list_display = (
        "username", "email", "name"
    )