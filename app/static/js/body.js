// Função para mostrar pré-visualização da imagem
function previewImage(event) {
  const preview = document.getElementById('preview');
  const file = event.target.files[0];

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      preview.src = e.target.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

// Função para enviar a imagem e mostrar em uma card
function enviarImagem() {
  const fileInput = document.getElementById('file-upload');
  const cardImage = document.getElementById('card-image');
  const cardText = document.querySelector('.card p');
  const preview = document.getElementById('preview');

  if (fileInput.files.length > 0) {
    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
      cardImage.src = e.target.result;
      cardImage.style.display = 'block';
      cardText.style.display = 'block';
      alert('Imagem enviada com sucesso!');

      // Limpa preview e input
      preview.src = '';
      preview.style.display = 'none';
      fileInput.value = '';

      // Oculta após 10 segundos
      setTimeout(() => {
        cardImage.src = '';
        cardImage.style.display = 'none';
        cardText.style.display = 'none';
      }, 1000);
    };

    reader.readAsDataURL(file);
  } else {
    alert('Por favor, selecione uma imagem antes de enviar.');
  }
}

// Alternar sidebar
function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("collapsed");
}

// Mostrar abas
function showTab(tabId) {
  const tabs = ['dashboard', 'analise', 'config'];
  tabs.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = "none";
  });
  const selected = document.getElementById(tabId);
  if (selected) selected.style.display = "block";
}

// Funções extras
function mudarConta() {
  alert("Função de troca de conta ainda não implementada.");
}

function conectarGoogle() {
  alert("Integração com o Google em desenvolvimento.");
}

// Inicializa carrossel Slick
$(document).ready(function () {
  $('.slider-sobrenos').slick({
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    adaptiveHeight: true,
    autoplay: true,
    autoplaySpeed: 3000
  });

  $('.autoplay').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2000
  });
});
