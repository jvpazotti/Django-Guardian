from django.db import models

class Contrato(models.Model):
    
    data_emissao = models.DateField()
    data_nascimento_tomador = models.DateField()
    valor_desembolsado = models.DecimalField(max_digits=10, decimal_places=2)
    cpf = models.CharField(max_length=14)
    pais = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    taxa = models.DecimalField(max_digits=5, decimal_places=2)  # 3.50 => 3,5%

    def __str__(self):
        return f"Contrato {self.id} - CPF: {self.cpf}"

class Parcela(models.Model):
    
    contrato = models.ForeignKey(Contrato, related_name='parcelas', on_delete=models.CASCADE)
    numero_parcela = models.PositiveIntegerField()
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()

    def __str__(self):
        return f"Parcela {self.numero_parcela} - Contrato {self.contrato_id}"