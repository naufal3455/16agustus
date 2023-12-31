# Generated by Django 4.2.1 on 2023-07-05 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id_kategori', models.AutoField(primary_key=True, serialize=False)),
                ('nama_kategori', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Laporan',
            fields=[
                ('id_laporan', models.AutoField(primary_key=True, serialize=False)),
                ('catatan', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pembayaran',
            fields=[
                ('id_pembayaran', models.AutoField(primary_key=True, serialize=False)),
                ('tanggal_pembayaran', models.DateField(null=True)),
                ('metode_pembayaran', models.CharField(choices=[('BRI', 'BRI'), ('BCA', 'BCA'), ('COD', 'COD')], max_length=10)),
                ('bukti_transfer', models.ImageField(blank=True, null=True, upload_to='bukti_transfer/%Y/%m/%d/')),
                ('status', models.CharField(max_length=100)),
                ('total_harga', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pembelian',
            fields=[
                ('id_pembelian', models.AutoField(primary_key=True, serialize=False)),
                ('harga_pembelian', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('jumlah', models.IntegerField()),
                ('total_harga', models.DecimalField(decimal_places=3, max_digits=10)),
                ('tanggal', models.DateField(auto_now_add=True)),
                ('catatan', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pesanan',
            fields=[
                ('id_pesanan', models.AutoField(primary_key=True, serialize=False)),
                ('konfirmasi_pembayaran', models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid'), ('failed', 'Failed')], default='unpaid', max_length=10)),
                ('jumlah', models.IntegerField(default=0)),
                ('pilihan', models.CharField(choices=[('dus', 'Dus'), ('lusin', 'Lusin')], default='dus', max_length=50)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('status', models.CharField(default='Pesanan Belum Terkirim Ke Penjual', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Promosi',
            fields=[
                ('id_promosi', models.AutoField(primary_key=True, serialize=False)),
                ('nama_promosi', models.CharField(max_length=100)),
                ('deskripsi', models.TextField()),
                ('gambar_promosi', models.ImageField(blank=True, null=True, upload_to='promosi/%Y/%m/%d/')),
                ('tanggal_mulai', models.DateField(auto_now_add=True)),
                ('tanggal_berakhir', models.DateField()),
                ('kode_promosi', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id_rating', models.AutoField(primary_key=True, serialize=False)),
                ('komentar', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Produkahm',
            fields=[
                ('id_produk', models.AutoField(primary_key=True, serialize=False)),
                ('nama_produk', models.CharField(max_length=100, null=True)),
                ('stok_per_dus', models.IntegerField(default=0)),
                ('gambar_produk', models.ImageField(blank=True, default='images/2023/06/09/torpedo.jpg', null=True, upload_to='images/%Y/%m/%d/')),
                ('harga_per_dus', models.DecimalField(decimal_places=3, max_digits=10)),
                ('kategori', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admins_toko.kategori')),
            ],
        ),
        migrations.CreateModel(
            name='PesananItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah', models.IntegerField(default=0)),
                ('pilihan', models.CharField(choices=[('dus', 'Dus'), ('lusin', 'Lusin')], default='dus', max_length=50)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('pesanan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pesanan_items', to='admins_toko.pesanan')),
                ('produk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admins_toko.produkahm')),
            ],
        ),
        migrations.AddField(
            model_name='pesanan',
            name='produk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admins_toko.produkahm'),
        ),
    ]
