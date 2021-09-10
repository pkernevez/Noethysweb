# Generated by Django 3.2.7 on 2021-09-09 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_adressemail_defaut'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='adresse_exp',
            field=models.ForeignKey(blank=True, help_text="Sélectionnez une des adresses d'expédition d'emails dans la liste. Il est possible de créer de nouvelles adresses depuis le menu Paramétrage > Adresses d'expédition.", null=True, on_delete=django.db.models.deletion.PROTECT, related_name='utilisateur_adresse_exp', to='core.adressemail', verbose_name="Adresse d'expédition"),
        ),
        migrations.AlterField(
            model_name='structure',
            name='adresse_exp',
            field=models.ForeignKey(blank=True, help_text="Sélectionnez une des adresses d'expédition d'emails dans la liste. Il est possible de créer de nouvelles adresses depuis le menu Paramétrage > Adresses d'expédition.", null=True, on_delete=django.db.models.deletion.PROTECT, to='core.adressemail', verbose_name="Adresse d'expédition"),
        ),
    ]