from django.shortcuts import render
from .models import Alarma

def panel_principal(request):
    ultimas_alarmas = Alarma.objects.order_by('-fecha_creacion')[:5]  # Últimas 5 alarmas
    return render(request, 'home/panel.html', {'ultimas_alarmas': ultimas_alarmas})