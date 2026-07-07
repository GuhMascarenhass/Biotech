from rest_framework import serializers
from .models import Analise

class AnaliseSerializer(serializers.ModelSerializer):
    nome_paciente = serializers.SerializerMethodField()
    id_amostra = serializers.SerializerMethodField()

    class Meta:
        model = Analise
        fields = [
            'id',
            'lamina',
            'id_amostra',
            'nome_paciente',
            'status',
            'imagem',
            'parasita_detectado',
            'confianca',
            'data_analise',
        ]

    def get_nome_paciente(self, obj):
        try:
            return obj.lamina.Paciente.paciente
        except AttributeError:
            return 'Não Identificado'

    def get_id_amostra(self, obj):
        try:
            return obj.lamina.id
        except AttributeError:
            return None