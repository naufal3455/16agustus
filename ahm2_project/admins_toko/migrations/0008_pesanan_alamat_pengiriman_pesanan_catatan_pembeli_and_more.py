# Generated by Django 4.2.1 on 2023-07-09 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins_toko', '0007_alter_pembelian_harga_pembelian_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesanan',
            name='alamat_pengiriman',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pesanan',
            name='catatan_pembeli',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pesanan',
            name='kode_pos',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='pesanan',
            name='nama_pembeli',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pesanan',
            name='no_telepon',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
