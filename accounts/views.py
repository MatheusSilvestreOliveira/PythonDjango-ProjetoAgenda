from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User


# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'Todos os campos devem ser preenchidos.')
        return render(request, 'accounts/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido.')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 8:
        messages.error(request, 'Senha muito curta, é necessário 8 (oito) caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')

    if senha2 != senha:
        messages.error(request, 'As senhas devem ser iguais.')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 8:
        messages.error(request, 'Usuário muito curto, é necessário 8 (oito) caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário existente.')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail existente.')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'Cadastrado com sucesso!')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
