from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
import pandas as pd
from reportlab.pdfgen import canvas
from .models import CustomUser
from .forms import UserForm

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_list')
        else:
            return render(request, 'users/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_list(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(username__icontains=query)
    return render(request, 'users/user_list.html', {'users': users, 'query': query})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión activa
            return redirect('user_profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})

""" @login_required """
def user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form})

@login_required
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.delete()
    return redirect('user_list')

@login_required
def user_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'users/user_profile.html', {'user': user})


def listado_copropietarios(request):
    query = request.GET.get("q")
    tipo_habitante = request.GET.get("tipo_habitante")

    copropietarios = CustomUser.objects.filter(tipo_habitante__in=["titular", "dueno", "copropietario", "menor"]).select_related("vivienda")

    if query:
        copropietarios = copropietarios.filter(
            Q(first_name__icontains=query) | 
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(vivienda__codigo__icontains=query)
        )

    if tipo_habitante:
        copropietarios = copropietarios.filter(tipo_habitante=tipo_habitante)

    paginator = Paginator(copropietarios, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "users/listado.html", {"page_obj": page_obj})

@login_required
def exportar_copropietarios_excel(request):
    copropietarios = CustomUser.objects.filter(role__in=["titular", "dueno", "copropietario", "menor"]).values(
        "username", "email", "phone", "tipo_habitante", "vivienda__codigo"
    )

    df = pd.DataFrame(list(copropietarios))
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="copropietarios.xlsx"'
    df.to_excel(response, index=False)
    return response

@login_required
def exportar_copropietarios_pdf(request):
    copropietarios = CustomUser.objects.filter(role__in=["titular", "dueno", "copropietario", "menor"])

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="copropietarios.pdf"'
    p = canvas.Canvas(response)

    y = 800  
    for c in copropietarios:
        p.drawString(100, y, f"{c.get_full_name()} - {c.get_tipo_habitante_display()} - {c.email} - {c.phone}")
        y -= 20  

    p.save()
    return response

@login_required
def editar_copropietario(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.tipo_habitante = request.POST.get("tipo_habitante")
        user.save()
        messages.success(request, "Copropietario actualizado correctamente.")
        return redirect("listado_copropietarios")

    return render(request, "users/editar.html", {"user": user})


@login_required
def cambiar_contrasena(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        new_password = request.POST.get("password")
        user.set_password(new_password)
        user.save()
        messages.success(request, "Contraseña actualizada correctamente.")
        return redirect("listado_copropietarios")

    return render(request, "users/cambiar_contrasena.html", {"user": user})

@login_required
def eliminar_copropietario(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.delete()
        messages.success(request, "Copropietario eliminado correctamente.")
        return redirect("listado_copropietarios")

    return render(request, "users/eliminar.html", {"user": user})
