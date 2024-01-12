from django.shortcuts import redirect


def redirect_to_profile(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_absolute_url())
    return redirect("account_login")