from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.db.models import Sum

from .forms import RegisterForm


# =====================================================
# LOGIN
# =====================================================

def login_view(request):

    if request.user.is_authenticated:

        if request.user.is_staff:
            return redirect('dashboard_admin')

        return redirect('dashboard_user')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_staff:
                return redirect('dashboard_admin')

            return redirect('dashboard_user')

        return render(
            request,
            'login.html',
            {
                'error': 'Username atau Password salah'
            }
        )

    return render(
        request,
        'login.html'
    )


# =====================================================
# REGISTER
# =====================================================

def register_view(request):

    form = RegisterForm()

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect(
                'dashboard_user'
            )

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


# =====================================================
# LOGOUT
# =====================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect('login')


# =====================================================
# DASHBOARD ADMIN
# =====================================================

@login_required
def dashboard_admin(request):

    if not request.user.is_staff:
        return redirect('dashboard_user')

    from reservasi.models import (
        Film,
        Studio,
        Kursi,
        JadwalTayang,
        Reservasi,
        Pembayaran,
        Tiket
    )

    total_pendapatan = Pembayaran.objects.filter(
        status='BERHASIL'
    ).aggregate(
        total=Sum('jumlah_bayar')
    )['total'] or 0

    context = {

        'total_film':
        Film.objects.count(),

        'total_studio':
        Studio.objects.count(),

        'total_kursi':
        Kursi.objects.count(),

        'total_jadwal':
        JadwalTayang.objects.count(),

        'total_reservasi':
        Reservasi.objects.count(),

        'total_pembayaran':
        Pembayaran.objects.count(),

        'total_tiket':
        Tiket.objects.count(),

        'total_pendapatan':
        total_pendapatan,

    }

    return render(
        request,
        'admin/dashboard_admin.html',
        context
    )


# =====================================================
# DASHBOARD USER
# =====================================================

@login_required
def dashboard_user(request):

    from reservasi.models import (
        Reservasi,
        Pembayaran,
        Tiket
    )

    reservasi_user = Reservasi.objects.filter(
        user=request.user
    ).order_by(
        '-tanggal_pesan'
    )

    pembayaran_user = Pembayaran.objects.filter(
        reservasi__user=request.user
    )

    tiket_user = Tiket.objects.filter(
        reservasi__user=request.user
    )

    context = {

        'reservasi_user':
        reservasi_user,

        'total_reservasi':
        reservasi_user.count(),

        'total_pembayaran':
        pembayaran_user.count(),

        'total_tiket':
        tiket_user.count(),

    }

    return render(
        request,
        'user/dashboard_user.html',
        context
    )