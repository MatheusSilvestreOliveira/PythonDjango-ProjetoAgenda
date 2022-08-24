from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Contato


# Create your views here.
def index(request):
    contatos = get_list_or_404(Contato)
    return render(request, 'contatos/index.html', {'contatos': contatos})


def dados_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    return render(request, 'contatos/dados_contato.html', {'contato': contato})


