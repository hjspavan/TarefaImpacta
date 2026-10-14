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

    // Salva a sessão do usuário
    const userName = email.split('@')[0];
    const formattedName = userName.charAt(0).toUpperCase() + userName.slice(1);
    localStorage.setItem('impacta_user', JSON.stringify({
      email: email,
      name: formattedName
    }));

    showMessage('Login realizado com sucesso! Redirecionando...', 'success');
    
    setTimeout(() => {
      window.location.href = 'dashboard.html';
    }, 800);
  });
}

function showMessage(text, type) {
  if (!message) return;

  message.textContent = text;
  message.className = `message ${type}`;
}
