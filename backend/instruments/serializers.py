from rest_framework import serializers
from backend.instruments.models import (
    InstrumentBookings,
    InstrumentBrands,
    InstrumentTypes,
    Instrument
)


class InstrumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentTypes
        fields = '__all__'


class InstrumentBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentBrands
        fields = '__all__'


class InstrumentBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentBookings
        fields = '__all__'


class UserInstrumentSerializer(serializers.ModelSerializer):
    """
    Serializer para a lista de instrumentos do usuário, buscando a primeira
    foto e os nomes dos campos relacionados.
    """
    # Busca o nome do objeto relacionado na tabela InstrumentBrands
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    
    # Busca o nome do objeto relacionado na tabela InstrumentTypes
    type_name = serializers.CharField(source='type.name', read_only=True)
    
    # Campo customizado para buscar a primeira foto do instrumento
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Instrument
        fields = [
            'id',
            'main_image',      # A foto principal do instrumento
            'name',            # O nome (ex: "Violão Aço")
            'brand_name',      # A marca (ex: "Yamaha")
            'type_name',       # O tipo (ex: "Violão")
            'color',           # A cor (ex: "Natural")
        ]

    def get_main_image(self, obj):
        """
        Este método busca a primeira foto associada ao instrumento.
        'obj' é a instância do Instrumento.
        """
        # Acessa a relação reversa 'instrumentpictures_set' e pega o primeiro objeto
        first_picture = obj.instrumentpictures_set.first()
        
        if first_picture:
            # Pega o request do contexto para construir a URL absoluta
            request = self.context.get('request')
            if request:
                # Retorna a URL completa da imagem
                return request.build_absolute_uri(first_picture.picture.url)
            # Se não houver request, retorna apenas a URL relativa
            return first_picture.picture.url
            
        # Retorna nulo se não houver nenhuma foto cadastrada
        return None
