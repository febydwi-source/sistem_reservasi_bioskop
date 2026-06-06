from django.shortcuts import redirect


def admin_only(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_staff:
            return view_func(
                request,
                *args,
                **kwargs
            )

        return redirect('dashboard')

    return wrapper