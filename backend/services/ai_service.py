import os
from typing import Dict, Any
import google.generativeai as genai
from django.conf import settings

class AIService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.api_key = None
            self.model = None

    def _initialize(self):
        """
        Inicializa o serviço de IA apenas quando necessário
        """
        if self.model is None:
            # Tenta obter a API key das configurações do Django primeiro
            self.api_key = getattr(settings, 'GOOGLE_API_KEY', None)
            
            # Se não encontrar nas configurações, tenta obter da variável de ambiente
            if not self.api_key:
                self.api_key = os.getenv('GOOGLE_API_KEY')
                
            if not self.api_key:
                raise ValueError(
                    "API key do Google Gemini não encontrada. "
                    "Configure a variável de ambiente GOOGLE_API_KEY ou "
                    "adicione GOOGLE_API_KEY nas configurações do Django."
                )
                
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

    def analyze_text(self, text: str, prompt: str) -> Dict[str, Any]:
        """
        Analisa um texto usando o Google Gemini com um prompt específico
        
        Args:
            text (str): O texto a ser analisado
            prompt (str): O prompt específico para a análise
            
        Returns:
            Dict[str, Any]: Resultado da análise
        """
        try:
            self._initialize()
            full_prompt = f"{prompt}\n\nTexto para análise:\n{text}"
            response = self.model.generate_content(full_prompt)
            
            return {
                'success': True,
                'response': response.text,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'response': None,
                'error': str(e)
            }

# Instância global do serviço
ai_service = AIService() 