from django.contrib import admin
from .models import (
    Film,
    Studio,
    Kursi,
    JadwalTayang,
    Reservasi,
    Pembayaran,
    Tiket
)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('judul', 'genre', 'durasi', 'status')
    search_fields = ('judul', 'genre')


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('nama_studio', 'kapasitas')


@admin.register(JadwalTayang)
class JadwalTayangAdmin(admin.ModelAdmin):
    list_display = (
        'film',
        'studio',
        'tanggal',
        'jam_mulai',
        'harga_tiket'
    )


@admin.register(Kursi)
class KursiAdmin(admin.ModelAdmin):
    list_display = (
        'nomor_kursi',
        'studio'
    )


@admin.register(Reservasi)
class ReservasiAdmin(admin.ModelAdmin):
    list_display = (
        'kode_reservasi',
        'user',
        'jadwal',
        'status',
        'tanggal_pesan'
    )


@admin.register(Pembayaran)
class PembayaranAdmin(admin.ModelAdmin):
    list_display = (
        'reservasi',
        'metode_pembayaran',
        'status'
    )


@admin.register(Tiket)
class TiketAdmin(admin.ModelAdmin):
    list_display = (
        'kode_tiket',
        'reservasi'
    )