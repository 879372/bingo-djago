# Generated by Django 5.0.4 on 2024-04-30 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0003_cartela_numeros_gerados"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartela",
            name="numeros_gerados",
            field=models.JSONField(),
        ),
    ]
