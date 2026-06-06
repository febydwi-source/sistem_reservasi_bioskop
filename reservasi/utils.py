from .models import Studio, Kursi

def generate_kursi():

    for studio in Studio.objects.all():

        if Kursi.objects.filter(
            studio=studio
        ).exists():
            continue

        baris = ['A', 'B', 'C', 'D', 'E']

        for b in baris:

            for n in range(1, 11):

                Kursi.objects.create(
                    studio=studio,
                    nomor_kursi=f"{b}{n}"
                )