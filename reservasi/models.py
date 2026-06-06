from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError

import qrcode
from io import BytesIO

from django.core.files import File

# =====================================
# FILM
# =====================================
class Film(models.Model):
    judul = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    durasi = models.PositiveIntegerField(help_text="Durasi dalam menit")
    rating_usia = models.CharField(max_length=10)
    sinopsis = models.TextField()
    poster = models.ImageField(upload_to='poster/', blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)

    tanggal_rilis = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('TAYANG', 'Sedang Tayang'),
            ('COMING_SOON', 'Coming Soon')
        ],
        default='TAYANG'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul


# =====================================
# STUDIO
# =====================================
class Studio(models.Model):
    nama_studio = models.CharField(max_length=50)
    kapasitas = models.PositiveIntegerField()

    def __str__(self):
        return self.nama_studio


# =====================================
# JADWAL TAYANG
# =====================================
class JadwalTayang(models.Model):
    film = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        related_name='jadwal_film'
    )

    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE,
        related_name='jadwal_studio'
    )

    tanggal = models.DateField()
    jam_mulai = models.TimeField()
    harga_tiket = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.film.judul} - {self.tanggal} {self.jam_mulai}"


# =====================================
# KURSI
# =====================================
class Kursi(models.Model):
    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE,
        related_name='kursi_studio'
    )

    nomor_kursi = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.studio.nama_studio} - {self.nomor_kursi}"

    class Meta:
        unique_together = ('studio', 'nomor_kursi')


# =====================================
# RESERVASI
# =====================================

class Reservasi(models.Model):

    STATUS_RESERVASI = [
        ('PENDING', 'Pending'),
        ('LUNAS', 'Lunas'),
        ('BATAL', 'Batal'),
        ('SELESAI', 'Selesai')
    ]

    kode_reservasi = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservasi_user'
    )

    jadwal = models.ForeignKey(
        JadwalTayang,
        on_delete=models.CASCADE
    )

    kursi = models.ForeignKey(
        Kursi,
        on_delete=models.CASCADE
    )

    jumlah_tiket = models.PositiveIntegerField(
        default=1
    )

    total_harga = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_RESERVASI,
        default='PENDING'
    )

    tanggal_pesan = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'jadwal',
            'kursi'
        )

    def clean(self):

        if self.kursi and self.jadwal:

            if self.kursi.studio != self.jadwal.studio:

                raise ValidationError(
                    'Kursi harus berasal dari studio yang sama dengan jadwal.'
                )

            kursi_dipakai = Reservasi.objects.filter(
                jadwal=self.jadwal,
                kursi=self.kursi
            )

            if self.pk:

                kursi_dipakai = kursi_dipakai.exclude(
                    pk=self.pk
                )

            if kursi_dipakai.exists():

                raise ValidationError(
                    'Kursi sudah dipesan.'
                )

    def save(self, *args, **kwargs):

        self.clean()

        if not self.kode_reservasi:

            self.kode_reservasi = (
                "RSV-" +
                uuid.uuid4().hex[:8].upper()
            )

        self.total_harga = (
            self.jadwal.harga_tiket *
            self.jumlah_tiket
        )

        super().save(
            *args,
            **kwargs
        )

    def __str__(self):

        return (
            f"{self.kode_reservasi} - "
            f"{self.user.username}"
        )
# =====================================
# PEMBAYARAN
# =====================================
class Pembayaran(models.Model):

    STATUS_PEMBAYARAN = [
        ('MENUNGGU', 'Menunggu'),
        ('BERHASIL', 'Berhasil'),
        ('DITOLAK', 'Ditolak')
    ]

    reservasi = models.OneToOneField(
        Reservasi,
        on_delete=models.CASCADE
    )

    metode_pembayaran = models.CharField(
        max_length=50,
        choices=[
            ('TRANSFER', 'Transfer Bank'),
            ('QRIS', 'QRIS')
        ]
    )

    bukti_pembayaran = models.ImageField(
        upload_to='bukti_pembayaran/',
        blank=True,
        null=True
    )

    jumlah_bayar = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    tanggal_bayar = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_PEMBAYARAN,
        default='MENUNGGU'
    )

    def __str__(self):
        return f"Pembayaran {self.reservasi.kode_reservasi}"


# =====================================
# TIKET
# =====================================

class Tiket(models.Model):

    reservasi = models.OneToOneField(
        Reservasi,
        on_delete=models.CASCADE
    )

    kode_tiket = models.CharField(
        max_length=30,
        unique=True,
        editable=False
    )

    qr_code = models.ImageField(
        upload_to='qrcode/',
        blank=True,
        null=True
    )

    sudah_digunakan = models.BooleanField(
        default=False
    )

    waktu_scan = models.DateTimeField(
        null=True,
        blank=True
    )

    diterbitkan_pada = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.kode_tiket:

            self.kode_tiket = (
                "TKT-" +
                uuid.uuid4().hex[:10].upper()
            )

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.qr_code:

            self.generate_qr_code()

            super().save(
                update_fields=['qr_code']
            )

    def generate_qr_code(self):

        qr = qrcode.make(
            self.kode_tiket
        )

        buffer = BytesIO()

        qr.save(
            buffer,
            format='PNG'
        )

        filename = (
            f'{self.kode_tiket}.png'
        )

        self.qr_code.save(
            filename,
            File(buffer),
            save=False
        )

    def __str__(self):

        return self.kode_tiket