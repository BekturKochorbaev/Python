from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
    print("✅ Суперпользователь создан!")
else:
    print("⚠️ Суперпользователь уже существует")
