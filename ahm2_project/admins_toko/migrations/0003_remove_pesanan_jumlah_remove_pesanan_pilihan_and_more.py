# Generated by Django 4.2.1 on 2023-07-05 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins_toko', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pesanan',
            name='jumlah',
        ),
        migrations.RemoveField(
            model_name='pesanan',
            name='pilihan',
        ),
        migrations.RemoveField(
            model_name='pesanan',
            name='subtotal',
        ),
    ]
