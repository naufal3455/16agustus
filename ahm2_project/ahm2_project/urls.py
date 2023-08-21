
from django.contrib import admin
from django.urls import path
from app_user.views import *
from admins_toko.views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('', menu_index),
   path('index/', menu_index, name= 'menu_index'),
   path('shop/', menu_produk , name= 'menu_produk'),
   path('produk/<int:id_produk>/', detail_produk, name='detail_produk'),
   path('cart/',menu_cart ,name='keranjang'),
   path('create_pesanan/', create_pesanan, name='create_pesanan'),
   path('checkout/', checkout, name='cekout'),
   path('hapus_keranjang/<int:id>/',hapus_keranjang, name='hapus_keranjang'),
   path('riwayat/', riwayat_pesanan, name='riwayat_pesanan'),
   path('contact/',menu_kontak),
   path('loginn/', login, name='loginn'),
   path('logoutuser/', LogoutView.as_view(next_page='loginn'), name='logoutuser'),
   path('register/',regist),

   path('laporan_toko_pdf/', laporantoko_pdf, name='laporan_toko_pdf'),
   path('laporan/', kelola_laporan, name='kelola_laporan'),
   #after login
   path('beranda/', beranda, name= 'beranda'),
   path('shop1/', menu_produk , name= 'menu_produk'),

   
   path('menu_admin/',menu_admin, name = 'menu_admin'),
   path('produk/',produk, name ='produk' ),
   path('tambah_produk/',tambah_produk, name = 'tambah_produk'),
   path('produk/ubah/<int:id_produk>', edit_produk, name = 'edit_produk'),
   path('produk/hapus/<int:id_produk>', hapus_produk, name = 'hapus_produk'),
   #penjualan
   path('pembelian/',pembelian, name='pembelian'),
   path('tambah-pembelian/',tambah_pembelian, name='tambah_pembelian'),
   path('pembelian/edit/<str:id_pembelian>/',edit_pembelian, name='edit_pembelian'),
   path('pembelian/hapus/<str:id_pembelian>/',hapus_pembelian, name='hapus_pembelian'),
   #PROMOSI
   path('data-promosi/',data_promosi, name='data_promosi'),
   path('tambah-promosi/',tambah_promosi, name='tambah_promosi'),
   path('edit-promosi/<str:id_promosi>/',edit_promosi, name='edit_promosi'),
   path('hapus-promosi/<str:id_promosi>/',hapus_promosi, name='hapus_promosi'),

   #kategori
   path('kategori/',kategori, name='kategori'),
   path('tambah_kategori/',tambah_kategori, name='tambah_kategori'),
   path('edit_kategori/<str:id_kategori>/', edit_kategori, name='edit_kategori'),
   path('hapus_kategori/<str:id_kategori>/',hapus_kategori, name='hapus_kategori'),

   #rating
   path('rating/', kelola_rating, name='kelola_rating'),

   #pembayaran
   path('pembayaran/',pembayaran, name='pembayaran'),
   path('tambah_pembayaran/', tambah_pembayaran, name='tambah_pembayaran'),
   path('edit_pembayaran/<str:id_pembayaran>/', edit_pembayaran, name='edit_pembayaran'),
   path('hapus_pembayaran/<str:id_pembayaran>/', hapus_pembayaran, name='hapus_pembayaran'),

   #pesanan
   path('pesanan/', pesanan, name='pesanan'),
   path('pesanan/tambah/', tambah_pesanan, name='tambah_pesanan'),
   path('pesanan/edit/<str:id_pesanan>/', edit_pesanan, name='edit_pesanan'),
   path('riwayat_pemesanan/edit/<str:id_pesanan>/', edit_pemesanan, name='edit_pemesanan'),
   path('pesanan/hapus/<str:id_pesanan>/', hapus_pesanan, name='hapus_pesanan'),
   path('menu_user/',menu_keluser),
   path('login/',loginadmin,name='login'),
   path('logout/',LogoutView.as_view(next_page='loginn'),name='logout'),
   path('admin/', admin.site.urls),
   path('submit_rating/', submit_rating, name='submit_rating'),


   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

