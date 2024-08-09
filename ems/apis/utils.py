from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def get_tokens_for_user(user_data):
    user, _ = User.objects.get_or_create(username=user_data.get('username'))

    refresh = RefreshToken.for_user(user)

    # Add custom claims
    refresh['user_type'] = user_data.get('user_type')
    refresh['custom_user_id'] = user_data.get('id')

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }