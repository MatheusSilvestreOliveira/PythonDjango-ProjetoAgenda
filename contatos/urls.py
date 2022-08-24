from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:contato_id>', views.dados_contato, name='dados_contato'),
]
