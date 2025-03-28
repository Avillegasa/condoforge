# Generated by Django 5.1.7 on 2025-03-12 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Alarma",
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
                    "tipo",
                    models.CharField(
                        choices=[
                            ("accidente", "Accidente"),
                            ("extravio_mascota", "Extravío de Mascota"),
                            ("otro", "Otro Evento"),
                        ],
                        max_length=20,
                    ),
                ),
                ("descripcion", models.TextField()),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
