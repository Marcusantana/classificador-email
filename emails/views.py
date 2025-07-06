import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import analyze_email_with_ai  

# ======= RENDERIZA O INDEX =======
def index(request):
    print("DEBUG: View index foi acessada!") # Adicione esta linha
    return render(request, "index.html")

# ======= FUNCAO PARA RECEBER E CLASSIFICAR EMAIL VIA POST =======
def classify_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email_text = data.get('email_text', '').strip()
            if not email_text:
                return JsonResponse({'error': 'Texto do email não enviado'}, status=400)
            
            categoria, resposta = analyze_email_with_ai(email_text) 
            
            return JsonResponse({'categoria': categoria, 'resposta': resposta})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)
