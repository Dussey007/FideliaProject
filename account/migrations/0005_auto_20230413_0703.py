# Generated by Django 3.1.2 on 2023-04-13 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20230413_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='categorie',
            field=models.ForeignKey(default='vide', on_delete=django.db.models.deletion.PROTECT, to='account.categorie', verbose_name='categorie'),
        ),
    ]
