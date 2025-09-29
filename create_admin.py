from django.db import migrations

def create_admin(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    if not User.objects.filter(email="mustafa@example.com").exists():
        User.objects.create_superuser(
            email="mustafa@example.com",
            full_name="Mustafa",
            password="12345",
            role="admin"
        )

class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
