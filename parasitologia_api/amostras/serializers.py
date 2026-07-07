from rest_framework import serializers
from .models import Paciente
from .models import Amostras

class AmostraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amostras
        fields = ['id', 'Paciente', 'imagem']