from django.conf import settings
from rest_framework import serializers
from backend.instruments.models import (
    InstrumentBookings,
    InstrumentBrands,
    InstrumentTypes,
    Instrument,
    InstrumentPictures
)


class InstrumentPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentPictures
        fields = ['id', 'picture']


class InstrumentSerializer(serializers.ModelSerializer):
    # Para ler os nomes, em vez dos IDs
    type_name = serializers.CharField(source='type.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    # Para receber o ID ao criar/atualizar
    type = serializers.PrimaryKeyRelatedField(queryset=InstrumentTypes.objects.all(), write_only=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=InstrumentBrands.objects.all(), write_only=True)

    # Para contar agendamentos (opcional, mas legal para o card)
    bookings_count = serializers.SerializerMethodField()

    provider = serializers.CharField(source='user_id.get_full_name', read_only=True)
    
    # Para lidar com imagens
    images = InstrumentPictureSerializer(source='instrumentpictures_set', many=True, read_only=True)
    main_image = serializers.SerializerMethodField()


    class Meta:
        model = Instrument
        fields = [
            'id', 'name', 'description', 'color', 'color_name', 'status', 'featured', 
            'location', 'type', 'brand', 'type_name', 
            'brand_name', 'bookings_count', 'images', 'main_image', 'availability', 'is_active', 'provider', 'is_loanable'
        ]
        read_only_fields = ['user_id'] # O user será pego do request

    def get_bookings_count(self, obj):
        # obj é a instância do Instrumento
        return obj.instrumentbookings_set.count()

    def get_main_image(self, obj):
        """
        Retorna a URL da primeira foto do instrumento.
        Se não houver fotos, retorna a URL de uma imagem padrão.
        """
        request = self.context.get('request')
        first_picture = obj.instrumentpictures_set.first()

        if first_picture and hasattr(first_picture.picture, 'url'):
            # Se uma foto real existir e tiver uma URL, retorne a URL completa
            return request.build_absolute_uri(first_picture.picture.url)
        else:
            # Caso contrário, construa e retorne a URL da imagem padrão
            default_image_url = f"{settings.MEDIA_URL}instruments_media/pictures/default.png"
            return request.build_absolute_uri(default_image_url)


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
