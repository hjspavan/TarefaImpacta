const form = document.getElementById('loginForm');
const message = document.getElementById('message');

if (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!email || !password) {
      showMessage('Preencha e-mail e senha para continuar.', 'error');
      return;
    }

    const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    if (!isValidEmail) {
      showMessage('Informe um e-mail válido.', 'error');
      return;
    }

    if (password.length < 6) {
      showMessage('A senha deve ter pelo menos 6 caracteres.', 'error');
      return;
    }

    showMessage('Login realizado com sucesso!', 'success');
    form.reset();
  });
}

function showMessage(text, type) {
  if (!message) return;

  message.textContent = text;
  message.className = `message ${type}`;
}
