from django.contrib.auth import get_user_model

def run():
    User = get_user_model()
    if not User.objects.filter(username="mustafa").exists():
        User.objects.create_superuser(
            username="mustafa",
            email="mustafa@example.com",
            password="12345"
        )
