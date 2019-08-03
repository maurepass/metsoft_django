from django.shortcuts import render, redirect


def base(request):
    return render(request, 'offers/base.html')


def redirect_after_login(request):
    if request.user.username == 'modelarnia':
        return redirect('patterns:patterns')
    else:
        return redirect('offers')
