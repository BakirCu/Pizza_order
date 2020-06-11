# Generated by Django 2.2.6 on 2020-06-10 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0007_auto_20200610_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.CreateModel(
            name='CartProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza.Cart')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza.Product')),
            ],
        ),
    ]
