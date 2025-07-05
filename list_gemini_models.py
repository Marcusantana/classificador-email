import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis do .env (certifique-se de que GOOGLE_API_TOKEN está lá)
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_TOKEN")

if not API_KEY:
    print("Erro: GOOGLE_API_TOKEN não está definida no seu arquivo .env.")
else:
    try:
        genai.configure(api_key=API_KEY)
        print("Modelos disponíveis para geração de conteúdo (generateContent):")
        found_pro_model = False
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                print(f"  - Nome: {m.name} | Display Name: {m.display_name}")
                if m.name == "models/gemini-1.0-pro" or m.display_name == "Gemini 1.0 Pro":
                    found_pro_model = True

        if not found_pro_model:
            print("\n⚠️ Aviso: 'gemini-1.0-pro' não foi encontrado na lista de modelos suportados para generateContent.")
            print("Por favor, verifique se a Generative Language API está completamente ativada em seu projeto Google Cloud.")
            print("Se o problema persistir, pode ser necessário tentar outro modelo listado acima (ex: text-bison-001) ou entrar em contato com o suporte do Google Cloud.")

    except Exception as e:
        print(f"Erro ao listar modelos: {e}")
        import traceback
        traceback.print_exc()