import os
import joblib
import traceback
from django.conf import settings
import google.generativeai as genai


# ======= CARREGAMENTO DO MODELO E VETORIZADOR =======
model_path = os.path.join(settings.BASE_DIR, 'emails', 'models', 'email_classifier.joblib')
vectorizer_path = os.path.join(settings.BASE_DIR, 'emails', 'models', 'vectorizer.joblib')

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("✅ Modelo e vetorizador locais carregados com sucesso.")
except Exception as e:
    print(f"❌ Erro ao carregar modelo ou vetor: {e}")
    model = None
    vectorizer = None

# ======= CONFIGURACAO DA API GOOGLE GEMINI =======
if not hasattr(settings, 'GOOGLE_API_TOKEN') or not settings.GOOGLE_API_TOKEN:
    print("❌ ERRO: GOOGLE_API_TOKEN não está configurado em settings.py. Por favor, adicione sua chave do Gemini.")
    genai_config_ok = False
else:
    genai.configure(api_key=settings.GOOGLE_API_TOKEN)
    genai_config_ok = True
    print("✅ Google Gemini API configurada.")

try:
    gemini_model = genai.GenerativeModel('models/gemini-2.0-flash')
    print("✅ Modelo models/gemini-2.0-flash inicializado.")
except Exception as e:
    print(f"❌ Erro ao inicializar modelo Gemini: {e}")
    traceback.print_exc()
    gemini_model = None

# ======== FUNCAO DE CLASSIFICAÇÃO DE EMAIL =======
def classify_email(text):
    if not model or not vectorizer:
        print("❌ Modelo ou vetorizador não disponíveis.")
        return "Desconhecida"
    try:
        text_tfidf = vectorizer.transform([text])
        prediction = model.predict(text_tfidf)
        return prediction[0]
    except Exception as e:
        print(f"❌ Erro ao classificar o e-mail: {e}")
        return "ErroClassificacao"

# ======= FUNCAO PARA GERAR RESPOSTA AUTOMATICA USANDO IA =======
def generate_automatic_ai_response(email_text, category):
    """
    Usa a API do Google Gemini para gerar resposta automática em formato de e-mail,
    condizente com o desafio da AutoU para uma empresa financeira.
    """

    if not genai_config_ok or gemini_model is None:
        print("❌ Erro: Gemini API não configurada ou modelo não inicializado. Não é possível gerar resposta com IA.")
        return "Obrigado pela sua mensagem! Em breve entraremos em contato."

    prompt = f"""
Sua função é atuar como um assistente de inteligência artificial para o setor de atendimento ao cliente de uma grande empresa do setor financeiro.

Com base no "E-mail Original do Cliente" e na "Categoria Identificada", elabore uma resposta por e-mail para o remetente.

**Diretrizes para a Resposta:**
1.  **Formato:** A resposta deve ser integralmente em formato de e-mail, começando com "Assunto:", seguido por uma saudação, o corpo da mensagem e uma despedida.
2.  **Linguagem:** Utilize Português do Brasil, com tom formal, profissional e educado.
3.  **Clareza e Objetividade:** A mensagem deve ser concisa, clara e ir direto ao ponto, abordando a questão principal do e-mail do remetente.
4.  **Conteúdo por Categoria:**
    * **Se a Categoria for "Produtivo":**
        * **Para solicitações ou dúvidas de clientes (internos ou externos) DA EMPRESA FINANCEIRA:** Reconheça o contato, forneça a informação solicitada, ou oriente os próximos passos, ou confirme o recebimento e o que será feito a seguir. Indique um prazo ou o que o cliente pode esperar. Ofereça-se para futuras dúvidas.
        * **Para comunicações externas (ex: ofertas, marketing, notificações de terceiros como LinkedIn, parcerias) recebidas PELA EMPRESA FINANCEIRA:** Agradeça o contato e o conteúdo do e-mail. **Informe que a mensagem será encaminhada internamente para o setor responsável para avaliação.** Deixe claro que a empresa está processando a informação. **Não tente resolver ou interagir diretamente com o conteúdo do e-mail original se ele não for uma solicitação direta de um cliente desta empresa.** Ofereça-se para contato futuro, se necessário.
    * **Se a Categoria for "Improdutivo":**
        * Agradeça a mensagem (ex: felicitações, agradecimentos).
        * Deixe claro que nenhuma ação imediata é necessária por parte do remetente ou da equipe, de forma educada.
        * Mantenha a resposta breve e cordial.
5.  **Assunto do E-mail:** Crie um assunto conciso e relevante. **Use "Re: [Assunto Original do E-mail]" se houver um assunto claro no e-mail original. Caso contrário, crie um assunto que resuma bem a mensagem e comece com "Re:".**

---

**Dados para a Resposta:**

**Categoria Identificada:** {category}

**E-mail Original do Cliente:**
\"\"\"
{email_text}
\"\"\"

---

**Inicie a resposta com:**

Assunto: Re: [Assunto Original do E-mail, ou um resumo relevante se não houver assunto claro]

Prezado(a) [Se o remetente do E-mail Original do Cliente for uma entidade (ex: LinkedIn, Cyfrin, UniFECAF), use o nome da entidade (ex: "Equipe LinkedIn", "UniFECAF"). Se o remetente for uma pessoa física (ex: "Marcus Santana") e o email for uma solicitação ou dúvida PARA A EMPRESA FINANCEIRA, use o nome da pessoa. Caso contrário, use "Prezados(as)"],

[Corpo da resposta conforme as diretrizes acima]

Atenciosamente,
Equipe de Atendimento
"""

    try:
        gemini_response = gemini_model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=350,
                temperature=0.7,
                top_p=0.9,
            )
        )

        generated_text = ""
        if gemini_response.parts:
            for part in gemini_response.parts:
                if hasattr(part, 'text'):
                    generated_text += part.text
            generated_text = generated_text.strip()
        else:
            print(f"⚠️ Aviso: Nenhuma resposta gerada pelo modelo. Feedback da API: {gemini_response.prompt_feedback}")
            if gemini_response.candidates and gemini_response.candidates[0].finish_reason:
                print(f"⚠️ Aviso: Finish Reason: {gemini_response.candidates[0].finish_reason}")

        if not generated_text or len(generated_text) < 80:
            print("❌ Aviso: Resposta gerada pela IA é muito curta ou vazia. Retornando mensagem padrão.")
            return "Obrigado pela sua mensagem! Em breve entraremos em contato."

        return generated_text

    except Exception as e:
        print(f"❌ Erro REAL ao gerar resposta com Gemini: {type(e).__name__}")
        print(f"Detalhes do Erro: {e}")
        traceback.print_exc()
        return "Obrigado pela sua mensagem! Em breve entraremos em contato."

# ======= FUNCAO PRINCIPAL PARA ANALISAR EMAIL E GERAR RESPOSTA =======
def analyze_email_with_ai(email_text):
    category = classify_email(email_text)
    response = generate_automatic_ai_response(email_text, category)
    return category, response
