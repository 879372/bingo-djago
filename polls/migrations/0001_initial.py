# Generated by Django 5.0.4 on 2024-04-29 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cartela",
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
            ],
        ),
        migrations.CreateModel(
            name="Jogo",
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
                ("data_inicio", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="NumeroSorteado",
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
                ("numero", models.IntegerField(unique=True)),
                (
                    "cartelas",
                    models.ManyToManyField(
                        related_name="numeros_sorteado", to="polls.cartela"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cartela",
            name="numeros",
            field=models.ManyToManyField(blank=True, to="polls.numerosorteado"),
        ),
    ]
