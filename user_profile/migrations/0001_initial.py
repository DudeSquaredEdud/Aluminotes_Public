# Generated by Django 4.2.6 on 2024-02-27 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "gender",
                    models.IntegerField(
                        choices=[(1, "Female"), (2, "Male"), (3, "Other")], default=1
                    ),
                ),
                ("age", models.IntegerField(default=1)),
                (
                    "picture",
                    models.ImageField(blank=True, upload_to="profile_pictures/"),
                ),
                (
                    "custom_user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
