const dropArea = document.querySelector('.file_box');
const fileInput = document.getElementById('email_file');
const uploadStatus = document.getElementById('upload_status');
const fileName = document.getElementById('file_name');
const progressBar = document.getElementById('progress_bar');
const progressText = document.getElementById('progress_text');
const successIcon = document.querySelector('.success_icon');

function simulateUpload(file) {
  fileName.textContent = file.name;
  progressBar.style.width = '0%';
  progressText.textContent = '0%';
  uploadStatus.style.display = 'flex';
  document.getElementById('progress_container').style.display = 'block';
  successIcon.style.display = 'none';

  let percent = 0;
  const interval = setInterval(() => {
    percent += 10;
    progressBar.style.width = `${percent}%`;
    progressText.textContent = `${percent}%`;

    if (percent >= 100) {
      clearInterval(interval);
      setTimeout(() => {
        document.getElementById('progress_container').style.display = 'none';
        successIcon.style.display = 'block';
      }, 300);
    }
  }, 200);
}

['dragenter', 'dragover'].forEach(event => {
  dropArea.addEventListener(event, e => {
    e.preventDefault();
    dropArea.classList.add('dragover');
  });
});

['dragleave', 'drop'].forEach(event => {
  dropArea.addEventListener(event, e => {
    e.preventDefault();
    dropArea.classList.remove('dragover');
  });
});

dropArea.addEventListener('drop', e => {
  const file = e.dataTransfer.files[0];
  if (!file) return;

  const isPDF = file.type === 'application/pdf';
  const isTXT = file.type === 'text/plain';

  if (isPDF || isTXT) {
    simulateUpload(file);
  } else {
    alert('Por favor, envie um arquivo PDF ou .txt válido.');
  }
});

document.getElementById('upload_button').addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;

  const isPDF = file.type === 'application/pdf';
  const isTXT = file.type === 'text/plain';

  if (isPDF || isTXT) {
    simulateUpload(file);
  } else {
    alert('Por favor, envie um arquivo PDF ou .txt válido.');
  }
});

let darkmode = localStorage.getItem("darkmode");
const themeSwitch = document.getElementById("theme_switch");

const enableDarkmode = () => {
  document.body.classList.add("darkmode");
  localStorage.setItem("darkmode", "active");
};

const disableDarkmode = () => {
  document.body.classList.remove("darkmode");
  localStorage.setItem("darkmode", null);
};

if (darkmode === "active") enableDarkmode();

themeSwitch.addEventListener("click", () => {
  darkmode = localStorage.getItem("darkmode");
  darkmode !== "active" ? enableDarkmode() : disableDarkmode();
});