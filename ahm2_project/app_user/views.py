from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import logout,authenticate, login as auth_login, get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django import forms 
from admins_toko.models import Produkahm, Promosi,Pesanan,PesananItem
from django.db import models
from django.http import HttpResponse,HttpResponseNotAllowed
from .models import Keranjang, KeranjangItem, Produkahm
from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Keranjang, KeranjangItem, Pesanan
from django.shortcuts import redirect
from django.core.paginator import Paginator


User = get_user_model()

# Create your views here.
def menu_index(request):
    user_id = request.user.id
    pesanans = Pesanan.objects.filter(user_id=user_id)
    product = Produkahm.objects.all()
    promos = Promosi.objects.all() 
    produk_terlaris = Produkahm.objects.annotate(jumlah_pesanan=Count('pesananitem')).order_by('-jumlah_pesanan')
    pesanans_count = pesanans.count()
    return render(request,'index.html',{'product':product,'promos':promos,'pesanans':pesanans,'pesanans_count': pesanans_count,'produk_terlaris': produk_terlaris})
from django.db.models import Count

@login_required(login_url=settings.LOGIN_USER)
def beranda(request):
    user_id = request.user.id
    pesanans = Pesanan.objects.filter(user_id=user_id)
    promos = Promosi.objects.all() 
    produk_terlaris = Produkahm.objects.annotate(jumlah_pesanan=Count('pesananitem')).order_by('-jumlah_pesanan')[:8]
    pesanans_count = pesanans.count()
    current_category = ""

    if 'category' in request.GET:
        selected_category = request.GET['category']
        product = Produkahm.objects.filter(kategori__nama_kategori=selected_category)
        current_category = selected_category
    else:
        product = Produkahm.objects.all()[:8]

    context = {
        'product': product,
        'promos': promos,
        'pesanans': pesanans,
        'pesanans_count': pesanans_count,
        'produk_terlaris': produk_terlaris,
        'current_category': current_category,
    }

    return render(request, 'afterlogin/beranda.html', context)


from django.db.models import Count

from django.core.paginator import Paginator
from django.db.models import F

def menu_produk(request):
    query = request.GET.get('search_query')
    kategori = request.GET.get('kategori')
    
    products = Produkahm.objects.all()
    
    if query:
        products = products.filter(nama_produk__icontains=query)
        
    if kategori:
        products = products.filter(kategori__icontains=kategori)
    
    products = products.order_by(F('id_produk').asc())  # Mengurutkan produk berdasarkan kolom 'id_produk'
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    
    product = paginator.get_page(page_number)
    
    user_id = request.user.id
    pesanans = Pesanan.objects.filter(user_id=user_id)
    pesanans_count = pesanans.count()
    
    context = {
        'query': query,
        'product': product,
        'pesanans': pesanans,
        'pesanans_count': pesanans_count,
        'current_category': kategori,
    }
    
    return render(request, 'shop.html', context)






#detailproduk

def detail_produk(request, id_produk):
    if request.method == 'POST':
        pilihan = request.POST.get('size')
        jumlah = int(request.POST.get('jumlah'))
        produk = get_object_or_404(Produkahm, id_produk=id_produk)

        keranjang, created = Keranjang.objects.get_or_create(user=request.user)

        # Check if the product already exists in the cart
        item, created = KeranjangItem.objects.get_or_create(keranjang=keranjang, produk=produk, pilihan=pilihan)
        if not created:
            item.jumlah += jumlah
        else:
            item.jumlah = jumlah
        item.save()

        return redirect('keranjang')

    else:
        product = get_object_or_404(Produkahm, id_produk=id_produk)  # Retrieve the desired product
        related_products = Produkahm.objects.exclude(id_produk=id_produk).order_by('?')[:6]
        return render(request, 'detail_produk.html', {'product': product, 'related_products': related_products})

@login_required(login_url=settings.LOGIN_USER)
def menu_cart(request):
    if request.method == 'POST':
        produk_id = request.POST.get('id_produk')
        pilihan = request.POST.get('size')
        jumlah = int(request.POST.get('jumlah'))

        try:
            produk = Produkahm.objects.get(id_produk=produk_id)
        except Produkahm.DoesNotExist:
            print("Produk not found")
            return redirect('keranjang')

        keranjang, _ = Keranjang.objects.get_or_create(user=request.user)

        subtotal = produk.harga_per_dus * jumlah  # Calculate the subtotal

        KeranjangItem.objects.create(keranjang=keranjang, produk=produk, pilihan=pilihan, jumlah=jumlah, subtotal=subtotal)

        return redirect('keranjang')
    else:
        keranjang, _ = Keranjang.objects.get_or_create(user=request.user)
        keranjang.update_total()
        items = keranjang.items.all()
        total = keranjang.total
        user_id = request.user.id
        pesanans = Pesanan.objects.filter(user_id=user_id)
        pesanans_count = pesanans.count()

        context = {
            'keranjang': keranjang,
            'items': items,
            'total': total,
            'pesanans':pesanans,
            'pesanans_count': pesanans_count,
        }
        return render(request, 'cart.html', context)

@login_required(login_url=settings.LOGIN_USER)
def hapus_keranjang(request, id):
    item = get_object_or_404(KeranjangItem, id=id)
    item.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect('keranjang')

@login_required(login_url=settings.LOGIN_USER)
def tambah_pesanan(request):
    if request.method == 'POST':
        produk = request.POST.get('id_produk')
        pilihan = request.POST.get('pilihan')
        jumlah = int(request.POST.get('jumlah'))

        # Mendapatkan produk dari database berdasarkan ID
        produk = Produkahm.objects.get(id=produk)

        # Mendapatkan atau membuat objek keranjang untuk pengguna saat ini
        keranjang, created = Keranjang.objects.get_or_create(user=request.user)

        # Cek apakah produk sudah ada di dalam keranjang
        item = KeranjangItem.objects.filter(keranjang=keranjang, produk=produk, pilihan=pilihan).first()
        if item:
            item.jumlah += jumlah
            item.save()
        else:
            KeranjangItem.objects.create(keranjang=keranjang, produk=produk, pilihan=pilihan, jumlah=jumlah)

        return redirect('keranjang')

@login_required(login_url=settings.LOGIN_USER)
def riwayat_pesanan(request):
    user_id = request.user.id
    pesanans = Pesanan.objects.filter(user_id=user_id)
    pesanans_count = pesanans.count()


    if request.method == 'POST':
        form = Pesanan(request.POST or None, request.FILES or None, instance=pesanans)
        if form.is_valid():
            form.save()
            return redirect('riwayat_pesanan')
    else:
        form = Pesanan()

    
    for pesanan in pesanans:
        subtotal = 0
        for pesanan_item in pesanan.pesanan_items.all():
            subtotal += pesanan_item.subtotal
        pesanan.subtotal = subtotal

    return render(request, 'riwayat.html', {'pesanans': pesanans,'form': form, 'pesanans_count': pesanans_count,})

def menu_kontak(request):
    promos = Promosi.objects.all()
    return render(request, 'contact.html', {'promos': promos})

@login_required(login_url=settings.LOGIN_USER)
def checkout(request):
    # Get the cart object for the current user
    keranjang = Keranjang.objects.get(user=request.user)
    items = keranjang.items.all()
    total = keranjang.total
    user_id = request.user.id
    pesanans = Pesanan.objects.filter(user_id=user_id)
    pesanans_count = pesanans.count()

    context = {
        'keranjang': keranjang,
        'items': items,
        'total': total,
        'pesanans':pesanans,
        'pesanans_count': pesanans_count,
    }
    return render(request, 'checkout.html', context)

@login_required(login_url=settings.LOGIN_URL)
def create_pesanan(request):
    if request.method == 'POST':
        # Get the cart object for the current user
        keranjang = Keranjang.objects.get(user=request.user)
        
        # Retrieve form data from the request
        nama_pembeli = request.POST.get('nama_pembeli')
        no_telepon = request.POST.get('no_telepon')
        alamat_pengiriman = request.POST.get('alamat_pengiriman')
        kode_pos = request.POST.get('kode_pos')
        catatan_pembeli = request.POST.get('catatan_pembeli')

        # Get cart items to be transferred to the order
        keranjang_items = KeranjangItem.objects.filter(keranjang=keranjang)
        
        if keranjang_items.exists():
            # Create a new order object
            pesanan = Pesanan.objects.create(
                user=request.user,
                konfirmasi_pembayaran='unpaid',
                konfirmasi_pesanan ='BELUM DITERIMA',
                nama_pembeli=nama_pembeli,
                no_telepon=no_telepon,
                alamat_pengiriman=alamat_pengiriman,
                kode_pos=kode_pos,
                catatan_pembeli=catatan_pembeli,
                # Add other attributes as needed
            )

            for keranjang_item in keranjang_items:
                # Add items from cart to the order
                subtotal = keranjang_item.produk.harga_per_dus * keranjang_item.jumlah
                pesanan_item = PesananItem.objects.create(
                    pesanan=pesanan,
                    produk=keranjang_item.produk,
                    jumlah=keranjang_item.jumlah,
                    pilihan=keranjang_item.pilihan,
                    subtotal=subtotal,
                )

            # Delete cart items after transferring to the order
            keranjang_items.delete()

            # Perform any other necessary operations for the order

            # Render a template with a 3-second delay and redirect script
            return render(request, 'pesanan_sukses.html')
        else:
            # Handle case when the cart is empty
            return redirect('beranda')
    else:
        return HttpResponseNotAllowed(['POST'])


def menu_login(request):
    return render(request,'loginn.html')

def regist(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        hashed_password = make_password(password)
        confirm_password=hashed_password
        user=User(username=username, email=email, password=hashed_password)
        user.save()
        
        messages.success(request, "Akun Kamu Berhasil Dibuat")
        return redirect('/loginn/')
    else:
        return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role == User.ADMIN_ROLE:
                auth_login(request, user)
                messages.error(request, 'Anda Admin')
                return redirect('menu_admin')
            if user.role == User.USER_ROLE:
                auth_login(request, user)
                messages.success(request,'Silahkan login untuk melanjutkan')
                return redirect('/beranda/')  # Ganti 'user_dashboard' dengan nama URL untuk dashboard user
            else:
                messages.error(request, 'Anda tidak memiliki izin untuk mengakses halaman ini.')
        else:
            messages.error(request, 'Username/Password salah.')

    return render(request,'loginn.html')

def logoutuser(request):
    return redirect('loginn')



