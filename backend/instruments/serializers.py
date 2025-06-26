from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
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


# Crie um serializer simples para o instrumento, para usar de forma aninhada
class BookingInstrumentSerializer(serializers.ModelSerializer):
    # Campos que já tínhamos
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    
    # NOVO CAMPO para a imagem do instrumento
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Instrument
        # Adicione 'main_image' à lista de campos
        fields = ['id', 'name', 'brand_name', 'type_name', 'main_image']

    # NOVO MÉTODO para construir a URL da imagem
    def get_main_image(self, obj):
        request = self.context.get('request')
        first_picture = obj.instrumentpictures_set.first()

        if first_picture and hasattr(first_picture.picture, 'url'):
            return request.build_absolute_uri(first_picture.picture.url)
        else:
            # Fallback para uma imagem padrão, se desejar
            default_image_url = f"{settings.MEDIA_URL}instruments_media/pictures/default.png"
            return request.build_absolute_uri(default_image_url) if request else default_image_url

# Crie um serializer simples para o cliente (usuário)
class BookingClientSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    get_full_name = serializers.SerializerMethodField()

    class Meta:
        # CORREÇÃO: Use get_user_model() para obter a classe de modelo real
        model = get_user_model() 
        
        # Use os campos que realmente existem no seu modelo de usuário.
        # Estes são campos padrão do Django. Adapte se o seu for diferente.
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_picture', 'get_full_name']

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            return request.build_absolute_uri(obj.profile_picture.url)
        # Retorna null ou uma URL de avatar padrão se não houver imagem
        return None

    def get_get_full_name(self, obj):
        # Usa o método do modelo se existir, senão concatena
        if hasattr(obj, 'get_full_name'):
            return obj.get_full_name()
        return f"{obj.first_name} {obj.last_name}".strip()

# --- Serializer para LEITURA (GET) ---
# Mostra todos os dados, incluindo informações aninhadas do instrumento e do usuário.
class InstrumentBookingDetailSerializer(serializers.ModelSerializer):
    # Use os serializers aninhados para obter objetos em vez de apenas strings
    instrument = BookingInstrumentSerializer(source='instrument_id', read_only=True)
    client = BookingClientSerializer(source='user_id', read_only=True)

    class Meta:
        model = InstrumentBookings
        fields = [
            'id',
            'instrument', # Agora é um objeto
            'client',     # Agora é um objeto
            'reservation_date',
            'reservation_starttime',
            'reservation_endtime',
            'status',
            'reservation_refusal_reason',
            # 'notes', # Adicione se tiver este campo no modelo
            'created_at',
        ]


# --- Serializer para CRIAÇÃO (POST) ---
class InstrumentBookingCreateSerializer(serializers.ModelSerializer):
    # Pega o usuário logado automaticamente. Este campo não aparecerá no formulário da API.
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    instrument_id = serializers.PrimaryKeyRelatedField(
        queryset=Instrument.objects.filter(is_active=True),
        label="Instrumento"
    )

    class Meta:
        model = InstrumentBookings
        fields = [
            'instrument_id',
            'user_id',
            'reservation_date',
            'reservation_starttime',
            'reservation_endtime',
        ]
    
    def validate(self, data):
        """ Executa a validação de conflito definida no modelo. """
        # Cria uma instância temporária para chamar o método clean() do modelo
        instance = InstrumentBookings(**data)
        instance.clean()
        return data


# --- Serializer para ATUALIZAÇÃO (PATCH) ---
# Permite alterar SOMENTE o status e, opcionalmente, o motivo da recusa.
class InstrumentBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentBookings
        fields = ['status', 'reservation_refusal_reason']

    def validate_status(self, value):
        """ Garante que o status seja uma escolha válida. """
        valid_statuses = [status[0] for status in InstrumentBookings._meta.get_field('status').choices]
        if value not in valid_statuses:
            raise serializers.ValidationError("Status inválido.")
        return value


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
