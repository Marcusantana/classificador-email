import json
from django.test import TestCase, Client
from django.urls import reverse

# ======= TESTES DAS VIEWS =======
class EmailViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    # ======= TESTA SE O INDEX CARREGA CORRETAMENTE =======
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # ======= TESTA CLASSIFICACAO DE EMAIL VIA POST =======
    def test_classify_email_valid_post(self):
        data = {'email_text': 'Gostaria de saber mais sobre o plano empresarial.'}
        response = self.client.post(reverse('classify_email'), 
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('categoria', response.json())
        self.assertIn('resposta', response.json())

    # ======= TESTA CLASSIFICACAO COM JSON SEM CAMPO =======
    def test_classify_email_missing_text(self):
        response = self.client.post(reverse('classify_email'), 
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Texto do email não enviado')

    # ======= TESTA CLASSSIFICACAO COM METODO INVALIDO =======
    def test_classify_email_wrong_method(self):
        response = self.client.get(reverse('classify_email'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['error'], 'Método não permitido')
