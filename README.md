

# 📬 Classificador Inteligente de E-mails

> Este repositório contém o **back-end e front-end da plataforma de classificação inteligente de e-mails**, desenvolvido em **Django** com integração à **IA generativa do Google Gemini** e uso de **Machine Learning**.

---

## 📌 Sobre o Projeto

Esta aplicação permite que usuários classifiquem e-mails como **"Produtivo"** ou **"Improdutivo"**, com base em um modelo de machine learning previamente treinado. Além disso, utiliza a **IA do Google Gemini** para sugerir uma **resposta automática personalizada**, conforme a categoria e o conteúdo do e-mail.

O objetivo é ajudar empresas a ganharem produtividade ao tratar comunicações relevantes de forma rápida e automatizada.

---

## 🎯 Funcionalidades

- Upload de arquivos `.pdf` e `.txt`, com extração automática de conteúdo.
- Entrada manual de texto do e-mail.
- Classificação automática em "Produtivo" ou "Improdutivo".
- Geração de resposta automática via Google Gemini, com base em diretrizes formais e tom profissional.
- Interface responsiva com suporte a **modo claro/escuro**.
- Testes automatizados cobrindo views e funções utilitárias.

---

## 🖥️ Tecnologias Utilizadas

| Camada | Tecnologias |
|--------|-------------|
| 🔙 Backend | Python, Django, joblib, Google Generative AI (Gemini), scikit-learn |
| 🔮 Machine Learning | Logistic Regression, TF-IDF, NLTK |
| 🔝 Frontend | HTML5, CSS3, JavaScript puro, PDF.js |
| 🧪 Testes | Django TestCase, pytest, unittest.mock |
| 📦 Outros | Render (deploy), SQLite (local), `.env` |

---

## 🌐 Acesse o Projeto Online

🔗 Deploy: [https://classificador-email-0knh.onrender.com/](https://classificador-email-0knh.onrender.com/)

---

## 🧠 Treinamento do Modelo

O modelo foi treinado com base em um dataset rotulado contendo exemplos reais e simulados de e-mails categorizados como produtivos ou improdutivos. O pipeline inclui:

- Pré-processamento com **stopwords + stemming**
- Vetorização com **TF-IDF**
- Classificação com **Regressão Logística**
- Persistência do modelo com `joblib`

---

## ⚙️ Como Executar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/classificador-email.git
cd classificador-email
```

2. Crie um ambiente virtual e ative:

```bash
python -m venv venv
venv\Scripts\activate     
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure suas variaveis de ambiente:

```bash
# exemplo

SECRET_KEY=teste123
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
GOOGLE_API_TOKEN=sua-chave-aqui
```

5. Treine o modelo (se desejar recriar):

```bash
python emails/ml/train_model.py
```

6. Rode o servidor local:

```bash
python manage.py runserver
```

---

## 🧪 Testes Automatizados

O projeto contém cobertura de testes para:

* Views (classify_email, index)
* Utilitários (classify_email, analyze_email_with_ai)
* Mocks da IA para evitar chamadas reais durante testes

Execute com:

```bash
python -m pytest emails/tests/tests_utils.py
python -m pytest emails/tests/tests_views.py
```

---

## 🔑 Como obter a chave da API Gemini (Google AI)

Para utilizar a funcionalidade de resposta automática com IA, você precisa gerar uma chave de API da Google Generative AI (Gemini). Siga os passos abaixo:

1.  Acesse o site oficial:
👉 https://makersuite.google.com/app/apikey
2.  Faça login com sua conta Google (se necessário).
3.  Clique em "Create API key".
4.  Copie a chave gerada e adicione ao seu .env, como no exemplo:

```bash
GOOGLE_API_TOKEN=coloque-sua-chave-aqui
```

> ⚠️ Atenção: essa chave possui limites gratuitos e pode ter custo se exceder. Consulte os termos da API para mais detalhes.

---
