from typing import Dict, Any
from ..services.ai_service import ai_service

class ArticleValidationService:
    @staticmethod
    def validate_article(article_content: str) -> Dict[str, Any]:
        """
        Valida um artigo usando IA
        
        Args:
            article_content (str): Conteúdo do artigo a ser validado
            
        Returns:
            Dict[str, Any]: Resultado da validação
        """
        prompt = """
        Analise o artigo e retorne APENAS um objeto JSON com dois campos:
        {
            "aprovado": true/false,
            "motivo": "explicação do motivo da aprovação ou rejeição"
        }

        Rejeite o artigo se:
        1. Contiver conteúdo impróprio ou ofensivo
        2. Não tiver coesão com o assunto
        3. For uma sequência aleatória de caracteres

        Retorne APENAS o objeto JSON, sem nenhum texto adicional.
        """
        
        result = ai_service.analyze_text(article_content, prompt)
        
        if result['success']:
            try:
                import json
                response_text = result['response'].strip()
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                
                if start >= 0 and end > start:
                    json_str = response_text[start:end]
                    feedback_dict = json.loads(json_str)
                    
                    return {
                        'is_valid': True,
                        'is_approved': feedback_dict.get('aprovado', False),
                        'feedback': feedback_dict.get('motivo', ''),
                        'error': None
                    }
                else:
                    return {
                        'is_valid': False,
                        'is_approved': False,
                        'feedback': 'Resposta da IA não contém JSON válido',
                        'error': 'Formato de resposta inválido'
                    }
            except json.JSONDecodeError as e:
                return {
                    'is_valid': False,
                    'is_approved': False,
                    'feedback': 'Erro ao processar resposta da IA',
                    'error': f'Erro ao decodificar JSON: {str(e)}'
                }
        else:
            return {
                'is_valid': False,
                'is_approved': False,
                'feedback': None,
                'error': result['error']
            }

# Instância global do serviço
article_validation_service = ArticleValidationService() 