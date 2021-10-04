# Generated by Django 4.0a1 on 2021-10-04 14:11

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_alter_utilisateur_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portailrenseignement',
            name='ancienne_valeur',
            field=django_cryptography.fields.encrypt(models.TextField(blank=True, null=True, verbose_name='Ancienne valeur')),
        ),
    ]
