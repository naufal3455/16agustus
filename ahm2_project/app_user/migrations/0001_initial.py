# Generated by Django 4.2.1 on 2023-07-05 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admins_toko', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('User', 'User'), ('Admin', 'Admin')], default='User', max_length=10)),
            ],
            options={
                'db_table': 'pengguna',
            },
        ),
        migrations.CreateModel(
            name='Keranjang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totals', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KeranjangItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pilihan', models.CharField(max_length=100)),
                ('jumlah', models.IntegerField()),
                ('subtotal', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('keranjang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app_user.keranjang')),
                ('produk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins_toko.produkahm')),
            ],
        ),
    ]