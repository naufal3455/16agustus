from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from admins_toko.models import Produkahm,Pesanan
from django.contrib.humanize.templatetags import humanize
from decimal import Decimal
from admins_toko.models import Produkahm
from django.db.models.signals import post_delete
from django.dispatch import receiver



class UserManager(BaseUserManager):
    def create_user(self,username,password=None, **extra_fields):
        username = self.normalize_email(username)
        user= self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        # Buat user biasa dengan metode create_user
        user = self.create_user(username, password, **extra_fields)
        # Set atribut is_staff dan is_superuser menjadi True
        user.is_staff = True
        user.is_superuser = True
        user.role = 'Admin' 
        # Simpan perubahan pada user
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    USER_ROLE = 'User'
    ADMIN_ROLE = 'Admin'
    ROLE_CHOICES = [
        (USER_ROLE, 'User'),
        (ADMIN_ROLE, 'Admin'),
        
    ]
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER_ROLE)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "pengguna"
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "pengguna"

    def is_admin(self):
        return self.role == self.ADMIN_ROLE
    
    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.role == self.ADMIN_ROLE

    def has_module_perms(self, app_label):
        return self.role == self.ADMIN_ROLE

class Keranjang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    totals = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    @property
    def total(self):
        total = sum(item.subtotal for item in self.items.all() if item.subtotal is not None)
        return f'Rp {humanize.intcomma(total)}' if total is not None else f'Rp {humanize.intcomma(Decimal(0))}'

    def update_total(self):
        total = sum(item.subtotal for item in self.items.all() if item.subtotal is not None)
        self.totals = Decimal(total) if total is not None else Decimal(0)
        self.save()


class KeranjangItem(models.Model):
    keranjang = models.ForeignKey(Keranjang, on_delete=models.CASCADE, null=True, related_name='items')
    produk = models.ForeignKey(Produkahm, on_delete=models.CASCADE)
    pilihan = models.CharField(max_length=100)
    jumlah = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f'{self.produk} - Rp {humanize.intcomma(self.produk.harga_per_dus)}'

    @property
    def hitung_subtotal(self):
        subtotal = self.produk.harga_per_dus * self.jumlah
        self.subtotal = subtotal
        self.save()
        return f'Rp {humanize.intcomma(self.subtotal)}' 

@receiver(post_delete, sender=KeranjangItem)
def update_keranjang_total(sender, instance, **kwargs):
        instance.keranjang.update_total()






    



    



