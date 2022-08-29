from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login realizado!')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


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


@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
