from django.urls import path
from .views import ContratoListCreateView, ResumoContratosView

urlpatterns = [
    path('contratos/', ContratoListCreateView.as_view(), name='contratos-list-create'),
    path('contratos/resumo/', ResumoContratosView.as_view(), name='contratos-resumo'),
]
