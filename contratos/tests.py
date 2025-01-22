from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Contrato, Parcela

class ContratoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_create_url = reverse('contratos-list-create')
        self.resumo_url = reverse('contratos-resumo')
        
        self.contrato_data = {
            "data_emissao": "2025-01-01",
            "data_nascimento_tomador": "1990-05-10",
            "valor_desembolsado": "10000.00",
            "cpf": "12345678900",
            "pais": "Brasil",
            "estado": "SP",
            "cidade": "São Paulo",
            "telefone": "11999999999",
            "taxa": "3.50",
            "parcelas": [
                {
                    "numero_parcela": 1,
                    "valor_parcela": "1000.00",
                    "data_vencimento": "2025-02-01"
                },
                {
                    "numero_parcela": 2,
                    "valor_parcela": "1000.00",
                    "data_vencimento": "2025-03-01"
                }
            ]
        }
    
    def test_criar_contrato(self):
        response = self.client.post(self.list_create_url, self.contrato_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contrato.objects.count(), 1)
        self.assertEqual(Parcela.objects.count(), 2)
        contrato = Contrato.objects.get()
        self.assertEqual(contrato.cpf, "12345678900")
    
    def test_listar_contratos(self):
        self.client.post(self.list_create_url, self.contrato_data, format='json')
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cpf'], "12345678900")
    
    def test_filtrar_contratos_por_cpf(self):
        self.client.post(self.list_create_url, self.contrato_data, format='json')
        response = self.client.get(self.list_create_url, {'cpf': '12345678900'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_obter_resumo_contratos(self):
        self.client.post(self.list_create_url, self.contrato_data, format='json')
        response = self.client.get(self.resumo_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valor_total_a_receber'], 2000.00)
        self.assertEqual(response.data['valor_total_desembolsado'], 10000.00)
        self.assertEqual(response.data['numero_total_contratos'], 1)
        self.assertEqual(response.data['taxa_media_contratos'], 3.5)
