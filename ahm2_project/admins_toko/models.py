from django.db import models
from django.contrib.humanize.templatetags import humanize
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

DEFAULT_IMAGE = 'images/2023/06/09/torpedo.jpg'
class Produkahm(models.Model):
    id_produk= models.AutoField(primary_key =True )
    kategori = models.ForeignKey('Kategori', on_delete=models.CASCADE, null=True)
    nama_produk= models.CharField(max_length=100, null=True)
    deskripsi_produk = models.TextField(null=True)
    stok_per_dus= models.IntegerField(default=0)
    gambar_produk= models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True ,default=DEFAULT_IMAGE)
    harga_per_dus= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.nama_produk}'
    
    @property
    def harga_idr(self):
        return f'Rp {humanize.intcomma(self.harga_per_dus)}'
    
    def update_stock(self, jumlah):
        self.stok_per_dus = self.stok_per_dus + jumlah
        self.save(update_fields=['stok_per_dus'])

    

class Pembelian(models.Model):
    id_pembelian = models.AutoField(primary_key=True)
    id_produk = models.ForeignKey(Produkahm, on_delete=models.CASCADE, null=True)
    harga_pembelian = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    jumlah = models.IntegerField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal = models.DateField(auto_now_add=True)
    catatan = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return f'{self.id_pembelian} - {self.id_produk.nama_produk} - {self.tanggal}'

    @property
    def total(self):
        return f'Rp {humanize.intcomma(self.total_harga)}'
    
    @property
    def harga(self):
        return f'Rp {humanize.intcomma(self.harga_pembelian)}'
    
    
    def save(self, *args, **kwargs):
        # Menghitung total_harga
        self.total_harga = Decimal(self.harga_pembelian) * self.jumlah

        super().save(*args, **kwargs)  # Simpan objek pembelian terlebih dahulu

        produk = self.id_produk
        jumlah = self.jumlah
        if produk and jumlah:
            try:
                produk = Produkahm.objects.get(id_produk=produk.id_produk)
                if produk.stok_per_dus >= jumlah:
                    # Periksa apakah pembelian ini sudah ada dalam database
                    if not self.pk:
                        # Penambahan stok hanya pada pembelian baru
                        produk.stok_per_dus += jumlah
                        produk.save()
            except Produkahm.DoesNotExist:
                # Handle ketika objek Produkahm tidak ditemukan
                # Misalnya, tampilkan pesan kesalahan atau lakukan tindakan lainnya
                pass


  
# promosi

class Promosi(models.Model):
    id_promosi = models.AutoField(primary_key=True)
    nama_promosi = models.CharField(max_length=100)
    deskripsi = models.TextField()
    gambar_promosi= models.ImageField(upload_to='promosi/%Y/%m/%d/', null=True, blank=True)
    tanggal_mulai = models.DateField(auto_now_add=True ,editable=False)
    tanggal_berakhir = models.DateField()
    kode_promosi = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_promosi
    


class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_kategori

#RATING

class Ratings(models.Model):
    id_rating = models.AutoField(primary_key=True)
    komentar = models.TextField()
    def __str__(self):
        return self.komentar


    
class Pembayaran(models.Model):
    CHOICES = (
        ('BRI', 'BRI'),
        ('BCA', 'BCA'),
        ('COD', 'COD'),
    )
    id_pembayaran = models.AutoField(primary_key=True)
    id_pembelian = models.ForeignKey('Pembelian', on_delete=models.CASCADE, null=True)
    tanggal_pembayaran = models.DateField(null=True, editable=True)
    metode_pembayaran = models.CharField(max_length=10, choices=CHOICES)
    bukti_transfer = models.ImageField(upload_to='bukti_transfer/%Y/%m/%d/', null=True, blank=True)
    status = models.CharField(max_length=100)
    total_harga = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.id_produk:
            self.harga_idr = self.id_produk.total_harga
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pembayaran - id_pembayaran: {self.id_pembayaran}"
    
    @property
    def total(self):
        return f'Rp {humanize.intcomma(self.total_harga)}'


class Pesanan(models.Model):
    KONFIRMASI_PEMBAYARAN_CHOICES = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('failed', 'Failed'),
    )
    KONFIRMASI_PESANAN_CHOICES = (
        ('DITERIMA', 'DITERIMA'),
        ('BELUM DITERIMA', 'BELUM DITERIMA'),
    )
    id_pesanan = models.AutoField(primary_key=True)
    konfirmasi_pembayaran = models.CharField(max_length=10, choices=KONFIRMASI_PEMBAYARAN_CHOICES, default='unpaid')
    konfirmasi_pesanan = models.CharField(max_length=30, choices=KONFIRMASI_PESANAN_CHOICES, default='BELUM DITERIMA ')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nama_pembeli = models.CharField(max_length=100,null=True)
    no_telepon = models.CharField(max_length=20,null=True)
    alamat_pengiriman = models.CharField(max_length=200, null=True)
    kode_pos = models.CharField(max_length=10, null=True)
    catatan_pembeli = models.TextField( null=True)
    bukti_pembayaran = models.ImageField(upload_to='bukti_pemabayaran/%Y/%m/%d/', null=True, blank=True)

    def hitung_subtotal(self):
        subtotal = 0
        for produk in self.produk.all():
            subtotal += produk.harga_per_dus * self.jumlah
        self.subtotal = subtotal
        self.save()
        return subtotal

    def __str__(self):
        return f"Pemesanan {self.id_pesanan}"

    @property
    def total(self):
        return f'Rp {humanize.intcomma(self.subtotal)}'
    
    

class PesananItem(models.Model):
    PILIHAN_CHOICES = (
        ('dus', 'Dus'),
        ('lusin', 'Lusin'),
    )
    pesanan = models.ForeignKey(Pesanan, on_delete=models.CASCADE, related_name='pesanan_items')
    produk = models.ForeignKey(Produkahm, on_delete=models.CASCADE, null=True)
    jumlah = models.IntegerField(default=0)
    pilihan = models.CharField(max_length=50, choices=PILIHAN_CHOICES, default='dus')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):

        id_produk = self.produk_id
        jumlah = self.jumlah
        if id_produk and jumlah:
            try:
                produk = Produkahm.objects.get(id_produk=id_produk)
                produk.stok_per_dus -= jumlah
                produk.save()
            except ObjectDoesNotExist:
                # Handle ketika objek Produkahm tidak ditemukan
                # Misalnya, tampilkan pesan kesalahan atau lakukan tindakan lainnya
                pass
        
        super().save(*args, **kwargs)


class Laporan(models.Model):
    id_laporan = models.AutoField(primary_key=True)
    id_pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    id_produk = models.ForeignKey(Produkahm, on_delete=models.CASCADE)
    catatan = models.TextField()

    def __str__(self):
        return f"Laporan {self.id_laporan}"

from django.db.models import Avg
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()

    # Add any additional fields as needed

    def __str__(self):
        return f"Rating {self.rating} by {self.user.username}" 




