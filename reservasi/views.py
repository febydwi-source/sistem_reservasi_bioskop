from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required
from .models import Tiket
from .models import Kursi
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse


from .models import (
    Film,
    Studio,
    JadwalTayang,
    Kursi,
    Reservasi,
    Pembayaran,
    Tiket
)

from .forms import (
    FilmForm,
    StudioForm,
    KursiForm,
    JadwalTayangForm,
    ReservasiForm,
    PembayaranForm
)


# =====================================================
# FILM
# =====================================================

@login_required
def film_list(request):

    films = Film.objects.all()

    return render(
        request,
        'film/film_list.html',
        {
            'films': films
        }
    )


from .models import (
    Film,
    JadwalTayang
)


def film_detail(request, pk):

    film = get_object_or_404(
        Film,
        pk=pk
    )

    jadwal = JadwalTayang.objects.filter(
        film=film
    ).order_by(
        'tanggal',
        'jam_mulai'
    )

    context = {

        'film': film,

        'jadwal': jadwal,

        'jumlah_jadwal':
        jadwal.count()

    }

    return render(
        request,
        'film/film_detail.html',
        context
    )

@admin_required
def film_create(request):

    form = FilmForm()

    if request.method == 'POST':

        form = FilmForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('film_list')

    return render(
        request,
        'film/film_form.html',
        {
            'form': form,
            'title': 'Tambah Film'
        }
    )


@admin_required
def film_update(request, pk):

    film = get_object_or_404(
        Film,
        pk=pk
    )

    form = FilmForm(
        instance=film
    )

    if request.method == 'POST':

        form = FilmForm(
            request.POST,
            request.FILES,
            instance=film
        )

        if form.is_valid():

            form.save()

            return redirect('film_list')

    return render(
        request,
        'film/film_form.html',
        {
            'form': form,
            'title': 'Edit Film'
        }
    )


@admin_required
def film_delete(request, pk):

    film = get_object_or_404(
        Film,
        pk=pk
    )

    if request.method == 'POST':

        film.delete()

        return redirect('film_list')

    return render(
        request,
        'film/film_delete.html',
        {
            'film': film
        }
    )


# =====================================================
# STUDIO
# =====================================================

@admin_required
def studio_list(request):

    studios = Studio.objects.all()

    return render(
        request,
        'studio/studio_list.html',
        {
            'studios': studios
        }
    )


@admin_required
def studio_create(request):

    form = StudioForm()

    if request.method == 'POST':

        form = StudioForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'studio_list'
            )

    return render(
        request,
        'studio/studio_form.html',
        {
            'form': form,
            'title': 'Tambah Studio'
        }
    )


@admin_required
def studio_update(request, pk):

    studio = get_object_or_404(
        Studio,
        pk=pk
    )

    form = StudioForm(
        instance=studio
    )

    if request.method == 'POST':

        form = StudioForm(
            request.POST,
            instance=studio
        )

        if form.is_valid():

            form.save()

            return redirect(
                'studio_list'
            )

    return render(
        request,
        'studio/studio_form.html',
        {
            'form': form,
            'title': 'Edit Studio'
        }
    )


@admin_required
def studio_delete(request, pk):

    studio = get_object_or_404(
        Studio,
        pk=pk
    )

    if request.method == 'POST':

        studio.delete()

        return redirect(
            'studio_list'
        )

    return render(
        request,
        'studio/studio_delete.html',
        {
            'studio': studio
        }
    )

# =====================================================
# KURSI
# =====================================================

@admin_required
def kursi_list(request):

    data = Kursi.objects.select_related(
        'studio'
    )

    return render(
        request,
        'kursi/kursi_list.html',
        {
            'data': data
        }
    )


@admin_required
def kursi_create(request):

    form = KursiForm()

    if request.method == 'POST':

        form = KursiForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'kursi_list'
            )

    return render(
        request,
        'kursi/kursi_form.html',
        {
            'form': form,
            'title': 'Tambah Kursi'
        }
    )


@admin_required
def kursi_update(request, pk):

    kursi = get_object_or_404(
        Kursi,
        pk=pk
    )

    form = KursiForm(
        instance=kursi
    )

    if request.method == 'POST':

        form = KursiForm(
            request.POST,
            instance=kursi
        )

        if form.is_valid():

            form.save()

            return redirect(
                'kursi_list'
            )

    return render(
        request,
        'kursi/kursi_form.html',
        {
            'form': form,
            'title': 'Edit Kursi'
        }
    )


@admin_required
def kursi_delete(request, pk):

    kursi = get_object_or_404(
        Kursi,
        pk=pk
    )

    if request.method == 'POST':

        kursi.delete()

        return redirect(
            'kursi_list'
        )

    return render(
        request,
        'kursi/kursi_delete.html',
        {
            'kursi': kursi
        }
    )
    
@admin_required
def generate_kursi(
    request,
    studio_id
):

    studio = get_object_or_404(
        Studio,
        pk=studio_id
    )

    jumlah = studio.kapasitas

    for nomor in range(
        1,
        jumlah + 1
    ):

        Kursi.objects.get_or_create(
            studio=studio,
            nomor_kursi=f"K{nomor}"
        )

    return redirect(
        'kursi_list'
    )
# =====================================================
# JADWAL
# =====================================================

@login_required
def jadwal_list(request):

    jadwals = JadwalTayang.objects.select_related(
        'film',
        'studio'
    )

    return render(
        request,
        'jadwal/jadwal_list.html',
        {
            'jadwals': jadwals
        }
    )


@admin_required
def jadwal_create(request):

    form = JadwalTayangForm()

    if request.method == 'POST':

        form = JadwalTayangForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect('jadwal_list')

    return render(
        request,
        'jadwal/jadwal_form.html',
        {
            'form': form,
            'title': 'Tambah Jadwal'
        }
    )


@admin_required
def jadwal_update(request, pk):

    jadwal = get_object_or_404(
        JadwalTayang,
        pk=pk
    )

    form = JadwalTayangForm(
        instance=jadwal
    )

    if request.method == 'POST':

        form = JadwalTayangForm(
            request.POST,
            instance=jadwal
        )

        if form.is_valid():

            form.save()

            return redirect('jadwal_list')

    return render(
        request,
        'jadwal/jadwal_form.html',
        {
            'form': form,
            'title': 'Edit Jadwal'
        }
    )


@admin_required
def jadwal_delete(request, pk):

    jadwal = get_object_or_404(
        JadwalTayang,
        pk=pk
    )

    if request.method == 'POST':

        jadwal.delete()

        return redirect('jadwal_list')

    return render(
        request,
        'jadwal/jadwal_delete.html',
        {
            'jadwal': jadwal
        }
    )


# =====================================================
# RESERVASI USER
# =====================================================

@login_required
def reservasi_create(request):

    jadwals = JadwalTayang.objects.all()

    selected_jadwal = None
    kursi_list = []

    jadwal_id = request.GET.get('jadwal')

    if jadwal_id:

        selected_jadwal = get_object_or_404(
            JadwalTayang,
            pk=jadwal_id
        )

        kursi_list = Kursi.objects.filter(
            studio=selected_jadwal.studio
        )

        kursi_terisi = Reservasi.objects.filter(
            jadwal=selected_jadwal
        ).values_list(
            'kursi_id',
            flat=True
        )

    else:

        kursi_terisi = []

    if request.method == 'POST':

        jadwal = JadwalTayang.objects.get(
            pk=request.POST['jadwal']
        )

        kursi = Kursi.objects.get(
            pk=request.POST['kursi']
        )

        reservasi = Reservasi(
            user=request.user,
            jadwal=jadwal,
            kursi=kursi,
            jumlah_tiket=1
        )

        reservasi.save()

        return redirect(
            'reservasi_saya'
        )

    return render(
        request,
        'reservasi/reservasi_form.html',
        {
            'jadwals': jadwals,
            'selected_jadwal': selected_jadwal,
            'kursi_list': kursi_list,
            'kursi_terisi': kursi_terisi,
        }
    )

@login_required
def reservasi_saya(request):

    data = Reservasi.objects.filter(
        user=request.user
    ).select_related(
        'jadwal',
        'kursi'
    ).order_by(
        '-tanggal_pesan'
    )

    return render(
        request,
        'reservasi/reservasi_saya.html',
        {
            'data': data
        }
    )

# =====================================================
# RESERVASI ADMIN
# =====================================================

@admin_required
def reservasi_list(request):

    data = Reservasi.objects.all()

    return render(
        request,
        'reservasi/reservasi_list.html',
        {
            'data': data
        }
    )


@admin_required
def reservasi_status(request, pk):

    reservasi = get_object_or_404(
        Reservasi,
        pk=pk
    )

    status_baru = request.GET.get(
        'status'
    )

    status_valid = [
        'PENDING',
        'LUNAS',
        'BATAL',
        'SELESAI'
    ]

    if status_baru in status_valid:

        reservasi.status = status_baru

        reservasi.save()

    return redirect(
        'reservasi_list'
    )


# =====================================================
# PEMBAYARAN USER
# =====================================================

@login_required
def pembayaran_create(
    request,
    reservasi_id
):

    reservasi = get_object_or_404(
        Reservasi,
        id=reservasi_id,
        user=request.user
    )

    if Pembayaran.objects.filter(
        reservasi=reservasi
    ).exists():

        return redirect(
            'reservasi_saya'
        )

    form = PembayaranForm()

    if request.method == 'POST':

        form = PembayaranForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            pembayaran = form.save(
                commit=False
            )

            pembayaran.reservasi = reservasi

            pembayaran.jumlah_bayar = (
                reservasi.total_harga
            )

            pembayaran.save()

            return redirect(
                'reservasi_saya'
            )

    return render(
        request,
        'pembayaran/pembayaran_form.html',
        {
            'form': form,
            'reservasi': reservasi
        }
    )

# =====================================================
# PEMBAYARAN ADMIN
# =====================================================

@admin_required
def pembayaran_list(request):

    data = Pembayaran.objects.all()

    return render(
        request,
        'pembayaran/pembayaran_list.html',
        {
            'data': data
        }
    )


@admin_required
def pembayaran_verifikasi(
    request,
    pk
):

    pembayaran = get_object_or_404(
        Pembayaran,
        pk=pk
    )

    aksi = request.GET.get(
        'aksi'
    )

    if aksi == 'terima':

        pembayaran.status = 'BERHASIL'

        reservasi = pembayaran.reservasi

        reservasi.status = 'LUNAS'

        reservasi.save()

        # Buat tiket otomatis
        if not Tiket.objects.filter(
            reservasi=reservasi
        ).exists():

            Tiket.objects.create(
                reservasi=reservasi
            )

    elif aksi == 'tolak':

        pembayaran.status = 'DITOLAK'

    pembayaran.save()

    return redirect(
        'pembayaran_list'
    )
    
    # =====================================================
# TIKET USER
# =====================================================

@login_required
def tiket_saya(request):

    data = Tiket.objects.filter(
        reservasi__user=request.user
    ).select_related(
        'reservasi',
        'reservasi__jadwal',
        'reservasi__jadwal__film'
    )

    return render(
        request,
        'tiket/tiket_saya.html',
        {
            'data': data
        }
    )
    

@admin_required
def tiket_list(request):

    data = Tiket.objects.select_related(
        'reservasi',
        'reservasi__jadwal',
        'reservasi__jadwal__film'
    )

    return render(
        request,
        'tiket/tiket_list.html',
        {
            'data': data
        }
    )
    
@admin_required
def tiket_scan(request):

    tiket = None
    pesan = None

    if request.method == 'POST':

        kode = request.POST.get(
            'kode_tiket'
        )

        try:

            tiket = Tiket.objects.select_related(
                'reservasi',
                'reservasi__user',
                'reservasi__jadwal',
                'reservasi__jadwal__film'
            ).get(
                kode_tiket=kode
            )

            if tiket.sudah_digunakan:

                pesan = (
                    "❌ Tiket sudah digunakan pada "
                    + tiket.waktu_scan.strftime(
                        "%d-%m-%Y %H:%M"
                    )
                )

            else:

                tiket.sudah_digunakan = True

                tiket.waktu_scan = timezone.now()

                tiket.save()

                pesan = (
                    "✅ Tiket valid dan berhasil digunakan"
                )

        except Tiket.DoesNotExist:

            pesan = (
                "❌ Kode tiket tidak ditemukan"
            )

    return render(
        request,
        'tiket/tiket_scan.html',
        {
            'tiket': tiket,
            'pesan': pesan
        }
    )
    
@login_required
def tiket_detail(request, pk):

    tiket = get_object_or_404(
        Tiket,
        pk=pk
    )

    return render(
        request,
        'tiket/tiket_detail.html',
        {
            'tiket': tiket
        }
    )


@login_required
def tiket_pdf(request, pk):

    tiket = get_object_or_404(
        Tiket,
        pk=pk
    )

    return HttpResponse(
        f"PDF Tiket {tiket.kode_tiket}"
    )


@admin_required
def validasi_tiket(request, pk):

    tiket = get_object_or_404(
        Tiket,
        pk=pk
    )

    tiket.sudah_digunakan = True
    tiket.waktu_scan = timezone.now()

    tiket.save()

    return redirect(
        'tiket_list'
    )