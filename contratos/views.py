from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contrato
from .serializers import ContratoSerializer
from .filters import ContratoFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg, F

class ContratoListCreateView(generics.ListCreateAPIView):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContratoFilter

class ResumoContratosView(APIView):
    def get(self, request, *args, **kwargs):
        contratos = Contrato.objects.all()
        filterset = ContratoFilter(request.GET, queryset=contratos)
        contratos_filtrados = filterset.qs

        total_contratos = contratos_filtrados.count()

        total_desembolsado = contratos_filtrados.aggregate(
            total=Sum('valor_desembolsado')
        )['total'] or 0

        taxa_media = contratos_filtrados.aggregate(
            media=Avg('taxa')
        )['media'] or 0

        total_parcelas = 0
        for contrato in contratos_filtrados:
            total_parcelas += contrato.parcelas.aggregate(
                soma_parcelas=Sum('valor_parcela')
            )['soma_parcelas'] or 0

        data = {
            "valor_total_a_receber": total_parcelas,
            "valor_total_desembolsado": total_desembolsado,
            "numero_total_contratos": total_contratos,
            "taxa_media_contratos": round(taxa_media, 2)
        }

        return Response(data)
