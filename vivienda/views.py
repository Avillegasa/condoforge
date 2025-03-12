from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Vivienda, Mascota
from .forms import ViviendaForm, MascotaForm

def lista_viviendas(request):
    query = request.GET.get("query", "")
    con_mascotas = request.GET.get("con_mascotas", False)

    viviendas = Vivienda.objects.annotate(
        num_habitantes=Count("habitantes"),
        num_mascotas=Count("mascotas"),
    )

    if query:
        viviendas = viviendas.filter(codigo__icontains=query)  

    if con_mascotas:
        viviendas = viviendas.filter(num_mascotas__gt=0)

    return render(request, "vivienda/lista_viviendas.html", {"viviendas": viviendas})

def detalle_vivienda(request, vivienda_id):
    vivienda = get_object_or_404(Vivienda, id=vivienda_id)
    return render(request, "vivienda/detalle_vivienda.html", {"vivienda": vivienda})

def editar_vivienda(request, vivienda_id):
    vivienda = get_object_or_404(Vivienda, id=vivienda_id)
    if request.method == "POST":
        form = ViviendaForm(request.POST, instance=vivienda)
        if form.is_valid():
            form.save()
            return redirect("lista_viviendas")
    else:
        form = ViviendaForm(instance=vivienda)
    return render(request, "vivienda/editar_vivienda.html", {"form": form})

def agregar_integrante(request, vivienda_id):
    vivienda = get_object_or_404(Vivienda, id=vivienda_id)
    if request.method == "POST":
        usuario_id = request.POST.get("usuario_id")
        vivienda.habitantes.add(usuario_id)
        return redirect("detalle_vivienda", vivienda_id=vivienda.id)
    

def registrar_mascota(request, vivienda_id):
    vivienda = get_object_or_404(Vivienda, id=vivienda_id)

    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.vivienda = vivienda
            mascota.save()

            vivienda.mascotas.add(mascota)

            return redirect("detalle_vivienda", vivienda_id=vivienda.id)
    else:
        form = MascotaForm()
    return render(request, "vivienda/registrar_mascota.html", {"form": form, "vivienda": vivienda})


def crear_vivienda(request):
    if request.method == "POST":
        form = ViviendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_viviendas")
    else:
        form = ViviendaForm()
    return render(request, "vivienda/crear_vivienda.html", {"form": form})

def detalle_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    return render(request, "vivienda/detalle_mascota.html", {"mascota": mascota})
    