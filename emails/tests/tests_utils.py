import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.test import TestCase
from emails.utils import classify_email, analyze_email_with_ai
from unittest.mock import patch

# ======= TESTES DO UTILS =======
class EmailUtilsTest(TestCase):

    # ======= TESTA CLASSIFICACAO LOCAL DO EMAIL COM MODELO =======
    def test_classify_email_returns_valid_category(self):
        texto = "Gostaria de uma reunião para falar sobre a proposta"
        categoria = classify_email(texto)
        self.assertIn(categoria, ['Produtivo', 'Improdutivo', 'Desconhecida'])

    # ======= TESTA ANALISE COMPLETA DE EMAIL USANDO IA (SIMULADA - MOCK) =======
    @patch('emails.utils.generate_automatic_ai_response')
    def test_analyze_email_with_ai_returns_expected_data(self, mock_response):
        mock_response.return_value = "Resposta gerada mockada."
        texto = "Olá, tudo bem? Gostaria de saber mais sobre os planos da empresa."
        categoria, resposta = analyze_email_with_ai(texto)

        self.assertIn(categoria, ['Produtivo', 'Improdutivo', 'Desconhecida', 'ErroClassificacao'])

        self.assertEqual(resposta, "Resposta gerada mockada.")
