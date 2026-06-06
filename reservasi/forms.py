from django import forms
from .models import Kursi

from .models import (
    Film,
    Studio,
    JadwalTayang,
    Reservasi,
    Pembayaran
)


# =====================================================
# FILM
# =====================================================

class FilmForm(forms.ModelForm):

    class Meta:
        model = Film

        fields = [
            'judul',
            'genre',
            'durasi',
            'rating_usia',
            'sinopsis',
            'poster',
            'trailer_url',
            'tanggal_rilis',
            'status'
        ]


# =====================================================
# STUDIO
# =====================================================

class StudioForm(forms.ModelForm):

    class Meta:
        model = Studio

        fields = [
            'nama_studio',
            'kapasitas'
        ]


# =====================================================
# JADWAL TAYANG
# =====================================================

class JadwalTayangForm(forms.ModelForm):

    class Meta:
        model = JadwalTayang

        fields = [
            'film',
            'studio',
            'tanggal',
            'jam_mulai',
            'harga_tiket'
        ]


# =====================================================
# RESERVASI
# =====================================================

class ReservasiForm(forms.ModelForm):

    class Meta:

        model = Reservasi

        fields = [
            'jadwal',
            'kursi',
            'jumlah_tiket'
        ]

    def clean(self):

        cleaned_data = super().clean()

        jadwal = cleaned_data.get(
            'jadwal'
        )

        kursi = cleaned_data.get(
            'kursi'
        )

        if jadwal and kursi:

            if kursi.studio != jadwal.studio:

                raise forms.ValidationError(
                    'Kursi tidak berada pada studio yang sama.'
                )

        return cleaned_data

# =====================================================
# PEMBAYARAN
# =====================================================

class PembayaranForm(forms.ModelForm):

    class Meta:
        model = Pembayaran

        fields = [
            'metode_pembayaran',
            'bukti_pembayaran'
        ]
        
# =====================================================
# KURSI
# =====================================================

class KursiForm(forms.ModelForm):

    class Meta:
        model = Kursi

        fields = [
            'studio',
            'nomor_kursi'
        ]