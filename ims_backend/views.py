from django.shortcuts import render


def render_custom_404(request):
    return render(request, '404.html', status=404)
