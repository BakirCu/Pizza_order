# Generated by Django 2.2.6 on 2020-06-10 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0006_auto_20200609_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.CharField(default='s', max_length=120),
            preserve_default=False,
        ),
    ]
