from django import forms

class AlamatPenagihanForm(forms.Form):
    nama_pembeli = forms.CharField(max_length=100)
    no_telepon = forms.CharField(max_length=20)
    alamat_pengiriman = forms.CharField(max_length=200)
    kode_pos = forms.CharField(max_length=10)
    catatan_pembeli = forms.CharField(widget=forms.Textarea)


