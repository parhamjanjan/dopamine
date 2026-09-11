import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_ADMIN_USERNAME")
email = os.getenv("DJANGO_ADMIN_EMAIL")
password = os.getenv("DJANGO_ADMIN_PASSWORD")

if not username or not email or not password:
    print("Admin environment variables are not configured.")
else:
    user = User.objects.filter(username=username).first()

    if user:
        if not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()

        print("Superuser already exists and was updated.")

    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        print("Superuser created successfully.")