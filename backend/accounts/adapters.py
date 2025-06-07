from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from backend.accounts.models import User, UserType


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        extra_data = sociallogin.account.extra_data

        email = extra_data.get("email", "")
        sso_id = extra_data.get("sub", "")
        picture = extra_data.get("picture", "")
        name = extra_data.get("name", "")

        user.email = email
        user.username = email.split("@")[0]
        user.first_name = name
        user.save()

        if not hasattr(user, "userprofile"):
            default_type, _ = UserType.objects.get_or_create(name="Padrão")
            User.objects.create(
                username=user,
                auth_provider="google",
                sso_id=sso_id,
                profile_picture=picture,
                user_type=default_type,
            )
