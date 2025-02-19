from django.shortcuts import render


def handler404(request, exception):
    return render(request, 'err/404.html', status=404)

