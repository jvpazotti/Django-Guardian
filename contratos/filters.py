import django_filters
from .models import Contrato

class ContratoFilter(django_filters.FilterSet):
    cpf = django_filters.CharFilter(field_name='cpf', lookup_expr='exact')
    estado = django_filters.CharFilter(field_name='estado', lookup_expr='icontains')
    data_emissao = django_filters.DateFilter(field_name='data_emissao', lookup_expr='exact')
    ano_emissao = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='year')
    mes_emissao = django_filters.NumberFilter(field_name='data_emissao', lookup_expr='month')

    class Meta:
        model = Contrato
        fields = ['cpf', 'estado', 'data_emissao', 'ano_emissao', 'mes_emissao']
