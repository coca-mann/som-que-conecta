import os
import uuid
from django.utils.deconstruct import deconstructible

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        # Pega a extensão do arquivo original
        ext = filename.split('.')[-1]
        
        # Gera um nome de arquivo aleatório e seguro usando UUID4
        filename = f'{uuid.uuid4().hex}.{ext}'
        
        # Retorna o caminho completo do arquivo (ex: 'articles/covers/2b1f8b2d-1a41-4c6e-8d8a-0b2a2d7f8d3d.jpg')
        return os.path.join(self.path, filename)

# Criamos uma instância da classe para usar nos modelos
rename_and_upload_path = PathAndRename
