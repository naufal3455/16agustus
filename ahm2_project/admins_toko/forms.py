from django.forms import ModelForm
from admins_toko.models import Produkahm,Kategori,Pembelian,Promosi,Ratings,Pembayaran
from django import forms
from .models import Promosi
from .models import Kategori
from django import forms
from .models import Ratings
from django import forms
from .models import Pesanan
from django import forms
from .models import Pembayaran, Pembelian, PesananItem


class FormProduk(ModelForm):
    class Meta: 
        model = Produkahm
        fields = ['id_produk','kategori', 'nama_produk','deskripsi_produk','stok_per_dus','gambar_produk','harga_per_dus']

        widgets = {
            'id_produk': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-control'}),
            'nama_produk': forms.TextInput(attrs={'class': 'form-control'}),
            'deskripsi_produk': forms.Textarea(attrs={'class': 'form-control'}),
            'stok_per_dus': forms.NumberInput(attrs={'class': 'form-control'}),
            'harga_per_dus': forms.TextInput(attrs={'class': 'form-control'}),
            # Tambahkan field lainnya di sini
        }

class PembelianForm(forms.ModelForm):
    class Meta:
        model = Pembelian
        fields = ['id_pembelian', 'id_produk','harga_pembelian' ,'jumlah', 'catatan']
        widgets = {
            'id_pembelian': forms.TextInput(attrs={'class': 'form-control'}),
            'id_produk': forms.Select(attrs={'class': 'form-control'}),
            'harga_pembelian': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah': forms.TextInput(attrs={'class': 'form-control'}),
            'catatan': forms.TextInput(attrs={'class': 'form-control'}),
        }

#promosi foms

class PromosiForm(forms.ModelForm):
    class Meta:
        model = Promosi
        fields = ['id_promosi', 'nama_promosi', 'deskripsi','gambar_promosi' ,'tanggal_berakhir', 'kode_promosi']
        widgets = {
            'id_promosi': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_promosi': forms.TextInput(attrs={'class': 'form-control'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control'}),
            'tanggal_berakhir': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'kode_promosi': forms.TextInput(attrs={'class': 'form-control'}),
        }

class KategoriForm(ModelForm):
    class Meta:
        model = Kategori
        fields = ('id_kategori', 'nama_kategori')
        widgets = {
            'id_kategori': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID Kategori'}),
            'nama_kategori': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Kategori'}),
        }


#ulasan
# forms.py

class RatingForm(forms.ModelForm):
    class Meta:
        model = Ratings
        fields = ['komentar']
        widgets = {
            'komentar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PembayaranForm(forms.ModelForm):
    id_pembelian = forms.ModelChoiceField(queryset=Pembelian.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label=None)

    class Meta:
        model = Pembayaran
        fields = ['id_pembayaran', 'id_pembelian', 'tanggal_pembayaran', 'metode_pembayaran', 'status', 'total_harga']
        widgets = {
            'id_pembayaran': forms.TextInput(attrs={'class': 'form-control', 'readonly': False}),
            'tanggal_pembayaran': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'metode_pembayaran': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'readonly': False}),
            'total_harga': forms.NumberInput(attrs={'class': 'form-control', 'readonly': False}),
        }   


#pemesanan

class PesananForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['konfirmasi_pembayaran']
        widgets = {
            'konfirmasi_pembayaran': forms.Select(attrs={'class': 'form-control'}),
          
            
        }   

class PemesananForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['konfirmasi_pesanan','bukti_pembayaran']
        widgets = {
            'konfirmasi_pesanan': forms.Select(attrs={'class': 'form-control'}),

        }   

from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']