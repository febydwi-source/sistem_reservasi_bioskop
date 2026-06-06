from django.urls import path

from .views import (
film_list,
film_detail,
film_create,
film_update,
film_delete,

studio_list,
studio_create,
studio_update,
studio_delete,

kursi_list,
kursi_create,
kursi_update,
kursi_delete,
generate_kursi,

jadwal_list,
jadwal_create,
jadwal_update,
jadwal_delete,

reservasi_list,
reservasi_create,
reservasi_saya,
reservasi_status,

pembayaran_list,
pembayaran_create,
pembayaran_verifikasi,

tiket_saya,
tiket_list,
tiket_scan,
tiket_detail,
tiket_pdf,
validasi_tiket,

)

urlpatterns = [

# =====================================================
# FILM
# =====================================================

path(
    'film/',
    film_list,
    name='film_list'
),

path(
    'film/<int:pk>/',
    film_detail,
    name='film_detail'
),

path(
    'film/tambah/',
    film_create,
    name='film_create'
),

path(
    'film/edit/<int:pk>/',
    film_update,
    name='film_update'
),

path(
    'film/delete/<int:pk>/',
    film_delete,
    name='film_delete'
),

# =====================================================
# STUDIO
# =====================================================

path(
    'studio/',
    studio_list,
    name='studio_list'
),

path(
    'studio/tambah/',
    studio_create,
    name='studio_create'
),

path(
    'studio/edit/<int:pk>/',
    studio_update,
    name='studio_update'
),

path(
    'studio/delete/<int:pk>/',
    studio_delete,
    name='studio_delete'
),

# =====================================================
# KURSI
# =====================================================

path(
    'kursi/',
    kursi_list,
    name='kursi_list'
),

path(
    'kursi/tambah/',
    kursi_create,
    name='kursi_create'
),

path(
    'kursi/edit/<int:pk>/',
    kursi_update,
    name='kursi_update'
),

path(
    'kursi/delete/<int:pk>/',
    kursi_delete,
    name='kursi_delete'
),

path(
    'kursi/generate/<int:studio_id>/',
    generate_kursi,
    name='generate_kursi'
),

# =====================================================
# JADWAL
# =====================================================

path(
    'jadwal/',
    jadwal_list,
    name='jadwal_list'
),

path(
    'jadwal/tambah/',
    jadwal_create,
    name='jadwal_create'
),

path(
    'jadwal/edit/<int:pk>/',
    jadwal_update,
    name='jadwal_update'
),

path(
    'jadwal/delete/<int:pk>/',
    jadwal_delete,
    name='jadwal_delete'
),

# =====================================================
# RESERVASI
# =====================================================

path(
    'reservasi/',
    reservasi_list,
    name='reservasi_list'
),

path(
    'reservasi/tambah/',
    reservasi_create,
    name='reservasi_create'
),

path(
    'reservasi/saya/',
    reservasi_saya,
    name='reservasi_saya'
),

path(
    'reservasi/status/<int:pk>/',
    reservasi_status,
    name='reservasi_status'
),

# =====================================================
# PEMBAYARAN
# =====================================================

path(
    'pembayaran/',
    pembayaran_list,
    name='pembayaran_list'
),

path(
    'pembayaran/<int:reservasi_id>/',
    pembayaran_create,
    name='pembayaran_create'
),

path(
    'pembayaran/verifikasi/<int:pk>/',
    pembayaran_verifikasi,
    name='pembayaran_verifikasi'
),

# =====================================================
# TIKET
# =====================================================

path(
    'tiket/',
    tiket_saya,
    name='tiket_saya'
),

path(
    'tiket/admin/',
    tiket_list,
    name='tiket_list'
),

path(
'tiket/scan/',
tiket_scan,
name='tiket_scan'
    ),

path(
    'tiket/detail/<int:pk>/',
    tiket_detail,
    name='tiket_detail'
    ),

path(
    'tiket/pdf/<int:pk>/',
    tiket_pdf,
    name='tiket_pdf'
    ),

path(
    'tiket/validasi/<int:pk>/',
    validasi_tiket,
    name='validasi_tiket'
    ),


]