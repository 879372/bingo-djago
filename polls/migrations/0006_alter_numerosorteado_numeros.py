# Generated by Django 5.0.4 on 2024-04-30 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0005_remove_numerosorteado_cartelas_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="numerosorteado",
            name="numeros",
            field=models.CharField(max_length=255),
        ),
    ]
