from django.shortcuts import render, redirect,get_object_or_404
from admins_toko.models import Produkahm,Promosi,Kategori,Pembayaran,Pembelian,Rating
from admins_toko.forms import FormProduk,PromosiForm,KategoriForm,RatingForm,PembayaranForm,Pesanan,PembelianForm,PemesananForm,RatingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login as login_auth
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.db.models import Q
from django.contrib import admin
from django.db.models import Avg
from .models import Rating
from app_user.models import User
from admins_toko.views import *
from django.shortcuts import render, redirect
from .models import Ratings
from .forms import RatingForm
from .models import Promosi
from django.contrib import messages
from .models import Pembayaran
from .forms import PembayaranForm
import io
from datetime import datetime
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from django.http import FileResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.conf import settings
from .models import Pembelian, Produkahm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import Laporan
from .models import Pesanan, PesananItem
from .forms import PesananForm

@login_required(login_url=settings.LOGIN_URL)
def menu_admin(request):
    return render(request, 'index_admin.html')
@login_required(login_url=settings.LOGIN_URL)
def loginadmin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role == User.ADMIN_ROLE:
                login_auth(request, user)
                return redirect('menu_admin')  # Ganti 'admin' dengan nama URL untuk halaman admin
            else:
                messages.error(request, 'Username/Password bukan yang terdaftar admin')
        else:
            messages.error(request, 'Username/Password salah.')
    return render(request, 'registration/login.html')


def menu_keluser(request):
    return render(request,'pelanggan.html')

#PRODUKKKKKK
@login_required(login_url=settings.LOGIN_URL)
def produk(request):
    products = Produkahm.objects.all()
    konteks ={
        'products' : products,
    }
    return render(request, 'produk.html', konteks)

@login_required(login_url=settings.LOGIN_URL)
def tambah_produk(request):
    if request.method == 'POST':
        form = FormProduk(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pesan = "Data berhasil disimpan"
            konteks = {
                'form': form,
                'pesan': pesan,
            }
            return render(request, 'tambah-produk.html', konteks)
    else:
        form = FormProduk()

    konteks = {
        'form': form,
    }
    return render(request, 'tambah-produk.html', konteks)

@login_required(login_url=settings.LOGIN_URL) 
def edit_produk(request, id_produk):
    produk = get_object_or_404(Produkahm, id_produk=id_produk)
    template = 'ubah-produk.html'

    if request.method == 'POST':
        form = FormProduk(request.POST or None, request.FILES or None, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, "Data berhasil diperbaharui")
            return redirect('edit_produk', id_produk=id_produk)
    else:
        form = FormProduk(instance=produk)
    
    konteks = {
        'form': form,
        'produk': produk,
    }
    
    return render(request, template, konteks)

@login_required(login_url=settings.LOGIN_URL)
def hapus_produk(request,id_produk):
    produk = Produkahm.objects.filter(id_produk=id_produk)
    produk.delete()

    messages.success(request, "Data berhasil dihapus !")

    return redirect('produk')


#Penjualan
@login_required(login_url=settings.LOGIN_URL)
def pembelian(request):
    pembelian =Pembelian.objects.all()
    konteks = {
        'pembelian': pembelian,
    }
    return render(request, 'pembelian.html', konteks)

@login_required(login_url=settings.LOGIN_URL)
def tambah_pembelian(request):
    if request.method == 'POST':
        form = PembelianForm(request.POST)
        if form.is_valid():
            pembelian = form.save(commit=False)
            jumlah_dibeli = pembelian.jumlah
            produk = pembelian.id_produk  # Mengambil objek ProdukAHM langsung dari form

            if produk and jumlah_dibeli > 0:
                if not pembelian.pk:  # Periksa apakah pembelian baru
                    produk.update_stock(jumlah_dibeli)  # Memanggil metode `update_stock` pada objek `produk`
                pembelian.save()
                return redirect('pembelian')
            else:
                error_message = "Produk tidak valid atau jumlah pembelian tidak positif."
                return render(request, 'tambah_pembelian.html', {'form': form, 'error_message': error_message})
    else:
        form = PembelianForm()
    return render(request, 'tambah_pembelian.html', {'form': form})




@login_required(login_url=settings.LOGIN_URL)
def edit_pembelian(request, id_pembelian):
    pembelian = Pembelian.objects.get(id_pembelian=id_pembelian)
    if request.method == 'POST':
        form = PembelianForm(request.POST, instance=pembelian)
        if form.is_valid():
            form.save()
            return redirect('pembelian')
    else:
        form = PembelianForm(instance=pembelian)
    return render(request, 'edit_pembelian.html', {'form': form, 'pembelian': pembelian})

@login_required(login_url=settings.LOGIN_URL)
def hapus_pembelian(request, id_pembelian):
    pembelian = Pembelian.objects.filter(id_pembelian=id_pembelian)
    pembelian.delete()

    messages.success(request, "Data berhasil dihapus!")

    return redirect('pembelian')

#data promosi
# ...
@login_required(login_url=settings.LOGIN_URL)
def data_promosi(request):
    promos = Promosi.objects.all()
    return render(request, 'data_promosi.html', {'promos': promos})

def tambah_promosi(request):
    if request.method == 'POST':
        form = PromosiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('data_promosi')
    else:
        form = PromosiForm()
    return render(request, 'tambah_promosi.html', {'form': form})

def edit_promosi(request, id_promosi):
    promosi = Promosi.objects.get(id_promosi=id_promosi)
    if request.method == 'POST':
        form = PromosiForm(request.POST or None, request.FILES or None, instance=promosi)
        if form.is_valid():
            form.save()
            return redirect('data_promosi')
    else:
        form = PromosiForm(instance=promosi)
    return render(request, 'edit_promosi.html', {'form': form, 'promosi': promosi})

def hapus_promosi(request, id_promosi):
    promosi = Promosi.objects.filter(id_promosi=id_promosi)
    promosi.delete()

    messages.success(request, "Promosi berhasil dihapus!")
    return redirect('data_promosi')


# kategoriiiiiiiii
def kategori(request):
    kategoris = Kategori.objects.all()
    context = {
        'kategoris': kategoris
    }
    return render(request, 'kategori.html', context)

def tambah_kategori(request):
    if request.method == 'POST':
        form = KategoriForm(request.POST)
        if form.is_valid():
            form.save()
            pesan = "Kategori berhasil ditambahkan"
            context = {
                'form': form,
                'pesan': pesan,
            }
            return redirect('kategori')
    else:
        form = KategoriForm()

    context = {
        'form': form,
    }
    return render(request, 'tambah_kategori.html', context)

def edit_kategori(request, id_kategori):
    kategori = Kategori.objects.get(id_kategori=id_kategori)
    if request.method == 'POST':
        form = KategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            return redirect('kategori')
    else:
        form = KategoriForm(instance=kategori)
    return render(request, 'edit_kategori.html', {'form': form, 'id_kategori': id_kategori})


def hapus_kategori(request, id_kategori):
    kategori = Kategori.objects.filter(id_kategori=id_kategori)
    kategori.delete()

    messages.success(request, "Kategori berhasil dihapus!")
    return redirect('kategori')


#rating

# views.py

def kelola_rating(request):
    ratings = Rating.objects.all()
    average_rating = Rating.objects.aggregate(Avg('rating'))['rating__avg']

    # Menambahkan nilai rata-rata rating ke dalam konteks
    context = {
        'ratings': ratings,
        'average_rating': average_rating
    }

    return render(request, 'kelola_rating.html', context)
#pembayaran
def pembayaran(request):
    pembayarans = Pembayaran.objects.all()
    return render(request, 'pembayaran.html', {'pembayarans': pembayarans})

def tambah_pembayaran(request):
    if request.method == 'POST':
        form = PembayaranForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pembayaran')
    else:
        form = PembayaranForm()
    
    return render(request, 'tambah_pembayaran.html', {'form': form})

def edit_pembayaran(request, id_pembayaran):
    pembayaran = get_object_or_404(Pembayaran, id_pembayaran=id_pembayaran)
    if request.method == 'POST':
        form = PembayaranForm(request.POST or None, request.FILES or None, instance=pembayaran)
        if form.is_valid():
            form.save()
            return redirect('pembayaran')
    else:
        form = PembayaranForm(instance=pembayaran)
    
    return render(request, 'edit_pembayaran.html', {'form': form, 'pembayaran': pembayaran})

def hapus_pembayaran(request, id_pembayaran):
    pembayaran = get_object_or_404(Pembayaran, id_pembayaran=id_pembayaran)
    pembayaran.delete()
    return redirect('pembayaran')

@login_required(login_url=settings.LOGIN_URL)
def pesanan(request):
    pesanans = Pesanan.objects.prefetch_related('pesanan_items').all()

    for pesanan in pesanans:
        subtotal = 0
        for pesanan_item in pesanan.pesanan_items.all():
            subtotal += pesanan_item.subtotal
        pesanan.subtotal = subtotal

    return render(request, 'pesanan.html', {'pesanans': pesanans})

@login_required(login_url=settings.LOGIN_URL)
def edit_pesanan(request, id_pesanan):
    pesanan = get_object_or_404(Pesanan, id_pesanan=id_pesanan)
    if request.method == 'POST':
        form = PesananForm(request.POST, instance=pesanan)
        if form.is_valid():
            form.save()
            return redirect('pesanan')
    else:
        form = PesananForm(instance=pesanan)
    return render(request, 'edit_pesanan.html', {'form': form, 'pesanan': pesanan})

@login_required(login_url=settings.LOGIN_URL)
def hapus_pesanan(request, id_pesanan):
    pesanan = Pesanan.objects.filter(id_pesanan=id_pesanan)
    pesanan.delete()
    messages.success(request, "Pesanan berhasil dihapus!")
    return redirect('pesanan')

def kelola_laporan(request):
    laporan = Laporan.objects.all()
    context = {
        'Laporan': laporan,
    }
    pembelian = Pembelian.objects.all()
    context = {
        'pembelian': pembelian,
    }
    product = Produkahm.objects.all()
    context = {
        'product' : product,
    }
    return render(request, 'laporan.html', {'Laporan': laporan,'pembelian':pembelian,'product':product})


@login_required(login_url=settings.LOGIN_URL)
def laporantoko_pdf(request):
    buffer = io.BytesIO()
    pembelians = Pembelian.objects.select_related('id_produk')
    
    data = [['ID Pembelian', 'Nama Produk', 'Harga per dus pembelian',
             'Jumlah stok yang dibeli', 'Tanggal pembelian', 'stok produk', 'harga penjualan']]

    for pembelian in pembelians:
        try:
            product_data = pembelian.id_produk
            row = [
                pembelian.id_pembelian if pembelian.id_pembelian else '',
                product_data.nama_produk,
                pembelian.harga if pembelian.id_pembelian else '',
                pembelian.jumlah if pembelian.id_pembelian else '',
                pembelian.tanggal if pembelian.id_pembelian else '',
                product_data.stok_per_dus,
                product_data.harga_idr,
            ]
            data.append(row)
        except Produkahm.DoesNotExist:
            # Handle the case when the Produkahm object does not exist
            pass
    
    # Continue your code here...

        
    # Lanjutan kode Anda ...

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 6),  # Update the font size to 6
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ])
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    title = Paragraph(f"LAPORAN PEMBELIAN UNTUK MELIHAT PERUBAHAN HARGA DAN PENAMBAHAN STOK",
                  style=ParagraphStyle(name='Title', fontSize=18, alignment=1, spaceAfter=10, leading=18))
    elements.append(title)
    
    # Add table to the elements list
    table = Table(data)
    table.setStyle(style)
    elements.append(table)
    
    pdf.build(elements)
    
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='laporan_toko.pdf')

@login_required(login_url=settings.LOGIN_USER)
def edit_pemesanan(request, id_pesanan):
    pesanan = get_object_or_404(Pesanan, id_pesanan=id_pesanan)
    if request.method == 'POST':
        form = PemesananForm(request.POST or None,request.FILES or None, instance=pesanan)
        if form.is_valid():
            form.save()
            return redirect('riwayat_pesanan')
    else:
        form = PemesananForm(instance=pesanan)
    return render(request, 'edit_pemesanan.html', {'form': form, 'pesanan': pesanan}) 


@login_required(login_url=settings.LOGIN_USER)
def submit_rating(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.save()
            return redirect('riwayat_pesanan')  # Replace with the appropriate URL or view name for the success page
    else:
        form = RatingForm()
    
    return render(request, 'submit_rating.html', {'form': form})