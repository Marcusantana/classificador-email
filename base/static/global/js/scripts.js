/* ======= ELEMENTOS DA INTERFACE ======= */
const dropArea = document.querySelector('.file_box');
const fileInput = document.getElementById('email_file');
const emailTextArea = document.getElementById('email_text');
const submitButton = document.querySelector('.submit_button button');
const themeSwitch = document.getElementById('theme_switch');

/* ======= FUNCAO PARA OBTER O CSRF TOKEN ======= */
const getCsrfToken = () => {
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta && csrfMeta.content) {
        return csrfMeta.content;
    }

    const cookies = document.cookie.split(';').map(c => c.trim());
    for (const cookie of cookies) {
        if (cookie.startsWith('csrftoken=')) {
            return decodeURIComponent(cookie.slice('csrftoken'.length + 1));
        }
    }
    
    return null;
};

/* ======= EXTRAÇÃO DE TEXTO DE ARQUIVO PDF ======= */
const extractTextFromPDF = async (file) => {
    if (!pdfjsLib) return alert('PDF.js não carregado');
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise; 
    let fullText = '';
    for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const content = await page.getTextContent();
        fullText += content.items.map(item => item.str).join(' ') + '\n';
    }

    emailTextArea.value = fullText.trim();
};

/* ======== TRATAMENTO DE ARQUIVOS ENVIADOS ======= */
const handleFile = file => {
    if (file.type === 'application/pdf') extractTextFromPDF(file);
    else if (file.type === 'text/plain') {
        const reader = new FileReader();
        reader.onload = e => (emailTextArea.value = e.target.result);
        reader.readAsText(file);
    } 
  
  else alert('Envie apenas arquivos PDF ou TXT.');
};

/* ======= LOGICA PARA ARRASTAR E SOLTAR ARQUIVO ======= */
dropArea.addEventListener('dragenter', e => { e.preventDefault(); dropArea.classList.add('dragover'); });
dropArea.addEventListener('dragover', e => e.preventDefault());
dropArea.addEventListener('dragleave', e => { e.preventDefault(); dropArea.classList.remove('dragover'); });
dropArea.addEventListener('drop', e => { e.preventDefault(); dropArea.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});

document.getElementById('upload_button').addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', e => {
    if (e.target.files.length) handleFile(e.target.files[0]);
});

/* ======= ENVIO DO TEXTO DO E-MAIL PARA CLASSIFICACAO ======= */
submitButton.addEventListener('click', async () => {
    const text = emailTextArea.value.trim();
    if (!text) return alert('Por favor, insira o texto do e-mail ou envie um arquivo.');

    submitButton.textContent = 'Enviando...';
    submitButton.disabled = true;

    try {
        const res = await fetch('/classify_email/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({ email_text: text }),
        });

        const data = await res.json();
        if (data.error) return alert('Erro: ' + data.error);

        const resultContainer = document.getElementById('result_container');
        resultContainer.style.display = 'block';
        document.getElementById('result_categoria').textContent = data.categoria;
        document.getElementById('result_resposta').textContent = data.resposta;
    } 
    
    catch {
        alert('Erro ao comunicar com o servidor.');
    } 
  
    finally {
        submitButton.textContent = 'Enviar';
        submitButton.disabled = false;
    }
});

/* ======= TROCA DE TEMA =======*/
if (localStorage.getItem('darkmode') === 'active') document.body.classList.add('darkmode');
themeSwitch.addEventListener('click', () => {
    document.body.classList.toggle('darkmode');
    localStorage.setItem('darkmode', document.body.classList.contains('darkmode') ? 'active' : 'null');
});