from django.db import models
from amostras.models import Amostras


class Analise(models.Model):
    STATUS = [('PEND','Pendente'),('CONCL','Concluida'),('CANC','Cancelada')]
    status = models.CharField(max_length=5,choices=STATUS,default='PEND')
    inicializada_em =models.DateTimeField(null=True, blank= True)
    finalizada_em = models.DateTimeField(null=True,blank=True)
    lamina = models.OneToOneField(Amostras, on_delete=models.SET_NULL, null=True, blank=True, related_name='analise')
    imagem = models.ImageField(upload_to='analise', null= True, blank= True)
    parasita_detectado = models.CharField(max_length=100, null= True, blank= True)
    confianca = models.FloatField(null= True, blank= True)
    data_analise = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Status: {self.status}'
