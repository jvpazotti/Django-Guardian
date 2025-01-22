# contratos/serializers.py
from rest_framework import serializers
from .models import Contrato, Parcela

class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = ['id', 'numero_parcela', 'valor_parcela', 'data_vencimento']

class ContratoSerializer(serializers.ModelSerializer):
    parcelas = ParcelaSerializer(many=True)

    class Meta:
        model = Contrato
        fields = [
            'id',
            'data_emissao',
            'data_nascimento_tomador',
            'valor_desembolsado',
            'cpf',
            'pais',
            'estado',
            'cidade',
            'telefone',
            'taxa',
            'parcelas'
        ]

    def create(self, validated_data):
        
        parcelas_data = validated_data.pop('parcelas', [])
        contrato = Contrato.objects.create(**validated_data)

        for parcela_data in parcelas_data:
            Parcela.objects.create(contrato=contrato, **parcela_data)

        return contrato
