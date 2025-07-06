import os
import sys
import pandas as pd
import re
import string
import unicodedata
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from django.conf import settings

# ======= CONFIGURACOES PARA DJANGO/NLTK/PRE-PROCESSAMENTO =======
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
nltk.download('stopwords')
nltk.download('rslp')
stopwords_pt = set(stopwords.words('portuguese'))
stemmer = RSLPStemmer()

# ======= FUNCAO PARA PRE-PROCESSAR O TEXTO =======
def preprocessar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    texto = re.sub(r'\d+', '', texto)
    tokens = texto.split()
    tokens = [stemmer.stem(t) for t in tokens if t not in stopwords_pt]
    return ' '.join(tokens)

# ======= LEITURA DO DATASET =======
df = pd.read_excel(os.path.join(settings.BASE_DIR, 'emails', 'datasets', 'emails_dataset.xlsx'))
print(f"✅ Total de registros no dataset: {len(df)}")

# ======= PRE-PROCESSAMENTO DOS TEXTOS =======
df['texto'] = df['texto'].apply(preprocessar_texto)

# ======= DIVISAO DOS DADOS(80% treino, 20% teste) =======
X_train, X_test, y_train, y_test = train_test_split(df['texto'], df['categoria'], test_size=0.2, random_state=42)

# ====== VETORIZACAO COM TF-ID (TEXTO PARA NUMMERO)
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# ====== TREINAMENTO E PRECISAO DO MODELO ======
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)
accuracy = model.score(X_test_tfidf, y_test)
print(f"✅ Treinamento concluído com acurácia: {accuracy:.2%}")

# ======= SALVANDO MODELO E VETORIZADOR =======
model_dir = os.path.join(settings.BASE_DIR, 'emails', 'models')
os.makedirs(model_dir, exist_ok=True)
joblib.dump(model, os.path.join(model_dir, 'email_classifier.joblib'))
joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer.joblib'))
print("✅ Modelo e vetorizador salvos com sucesso.")