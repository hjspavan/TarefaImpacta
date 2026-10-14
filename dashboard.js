document.addEventListener('DOMContentLoaded', () => {
  // 1. Gerenciamento do Perfil do Usuário
  initUserProfile();

  // 2. Data de Hoje
  initCurrentDate();

  // 3. Gerenciamento de Tarefas
  initTaskManager();

  // 4. Botão de Logout
  initLogout();
});

/* ==========================================================
   1. PERFIL DO USUÁRIO & SESSÃO
   ========================================================== */
function initUserProfile() {
  const displayUserName = document.getElementById('displayUserName');
  const displayUserEmail = document.getElementById('displayUserEmail');
  const welcomeUserName = document.getElementById('welcomeUserName');
  const userAvatar = document.getElementById('userAvatar');

  // Recupera usuário salvo no login
  const storedUserRaw = localStorage.getItem('impacta_user');
  let user = {
    name: 'Estudante Impacta',
    email: 'aluno@impacta.edu.br'
  };

  if (storedUserRaw) {
    try {
      const parsed = JSON.parse(storedUserRaw);
      if (parsed && parsed.email) {
        user = parsed;
      }
    } catch (e) {
      console.error('Erro ao ler usuário salvo:', e);
    }
  }

  if (displayUserName) displayUserName.textContent = user.name || 'Estudante';
  if (displayUserEmail) displayUserEmail.textContent = user.email || 'aluno@impacta.edu.br';
  if (welcomeUserName) welcomeUserName.textContent = user.name || 'Estudante';
  if (userAvatar) {
    const initial = (user.name || user.email || 'A').charAt(0).toUpperCase();
    userAvatar.textContent = initial;
  }
}

/* ==========================================================
   2. DATA ATUAL
   ========================================================== */
function initCurrentDate() {
  const dateEl = document.getElementById('currentDateStr');
  if (!dateEl) return;

  const now = new Date();
  const options = { day: '2-digit', month: 'short', year: 'numeric' };
  const formatted = now.toLocaleDateString('pt-BR', options).replace('.', '');
  dateEl.textContent = formatted.charAt(0).toUpperCase() + formatted.slice(1);
}

/* ==========================================================
   3. GESTOR DE TAREFAS (CRUD & LOCALSTORAGE)
   ========================================================== */
function initTaskManager() {
  const tasksListEl = document.getElementById('tasksList');
  const emptyStateEl = document.getElementById('emptyTasksState');
  const addTaskForm = document.getElementById('addTaskForm');
  const filterBtns = document.querySelectorAll('.filter-btn');

  // Métricas
  const statPending = document.getElementById('statPending');
  const statCompleted = document.getElementById('statCompleted');
  const countAll = document.getElementById('countAll');
  const countPending = document.getElementById('countPending');
  const countCompleted = document.getElementById('countCompleted');

  let currentFilter = 'all';

  // Tarefas padrão iniciais se for o primeiro acesso
  const defaultTasks = [
    {
      id: 'task-1',
      title: 'Finalizar atividade prática de Git & GitHub',
      category: 'Git e GitHub',
      priority: 'alta',
      dueDate: getRelativeDateString(1),
      completed: false
    },
    {
      id: 'task-2',
      title: 'Praticar comandos de branch e resolução de conflitos',
      category: 'Git e GitHub',
      priority: 'alta',
      dueDate: getRelativeDateString(3),
      completed: false
    },
    {
      id: 'task-3',
      title: 'Estudar modelagem de dados e consultas SQL',
      category: 'Banco de Dados',
      priority: 'media',
      dueDate: getRelativeDateString(5),
      completed: false
    },
    {
      id: 'task-4',
      title: 'Construir layout responsivo em CSS Grid e Flexbox',
      category: 'Desenvolvimento Web',
      priority: 'baixa',
      dueDate: getRelativeDateString(-1),
      completed: true
    }
  ];

  let tasks = loadTasks();
  if (!tasks || tasks.length === 0) {
    tasks = defaultTasks;
    saveTasks(tasks);
  }

  // Renderização inicial
  renderTasks();

  // Evento de submissão do formulário
  if (addTaskForm) {
    addTaskForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const titleInput = document.getElementById('taskTitle');
      const categorySelect = document.getElementById('taskCategory');
      const prioritySelect = document.getElementById('taskPriority');
      const dueDateInput = document.getElementById('taskDueDate');

      const title = titleInput.value.trim();
      const category = categorySelect.value || 'Geral';
      const priority = prioritySelect.value || 'media';
      const dueDate = dueDateInput.value || '';

      if (!title) return;

      const newTask = {
        id: 'task-' + Date.now(),
        title,
        category,
        priority,
        dueDate: dueDate ? formatDate(dueDate) : 'Sem prazo',
        completed: false
      };

      tasks.unshift(newTask);
      saveTasks(tasks);
      renderTasks();

      // Reset
      addTaskForm.reset();
      categorySelect.selectedIndex = 0;
      prioritySelect.value = 'media';
    });
  }

  // Filtros
  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      filterBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.getAttribute('data-filter');
      renderTasks();
    });
  });

  // Funções internas do gestor
  function loadTasks() {
    try {
      const data = localStorage.getItem('impacta_tasks');
      return data ? JSON.parse(data) : null;
    } catch (e) {
      console.error('Erro ao ler tarefas:', e);
      return null;
    }
  }

  function saveTasks(newTasks) {
    try {
      localStorage.setItem('impacta_tasks', JSON.stringify(newTasks));
    } catch (e) {
      console.error('Erro ao salvar tarefas:', e);
    }
  }

  function updateMetrics() {
    const total = tasks.length;
    const completed = tasks.filter((t) => t.completed).length;
    const pending = total - completed;

    if (statPending) statPending.textContent = pending;
    if (statCompleted) statCompleted.textContent = completed;
    if (countAll) countAll.textContent = total;
    if (countPending) countPending.textContent = pending;
    if (countCompleted) countCompleted.textContent = completed;
  }

  function renderTasks() {
    updateMetrics();

    let filtered = tasks;
    if (currentFilter === 'pending') {
      filtered = tasks.filter((t) => !t.completed);
    } else if (currentFilter === 'completed') {
      filtered = tasks.filter((t) => t.completed);
    }

    if (filtered.length === 0) {
      tasksListEl.innerHTML = '';
      if (emptyStateEl) emptyStateEl.style.display = 'block';
      return;
    }

    if (emptyStateEl) emptyStateEl.style.display = 'none';

    tasksListEl.innerHTML = filtered
      .map((task) => {
        const priorityLabels = {
          alta: 'Alta',
          media: 'Média',
          baixa: 'Baixa'
        };

        return `
        <li class="task-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
          <div class="task-left">
            <input
              type="checkbox"
              class="task-checkbox-custom"
              ${task.completed ? 'checked' : ''}
              data-action="toggle"
              data-id="${task.id}"
              aria-label="Marcar como concluída"
            />
            <div class="task-info-block">
              <span class="task-name">${escapeHtml(task.title)}</span>
              <div class="task-meta-tags">
                <span class="tag-discipline">${escapeHtml(task.category)}</span>
                <span class="tag-priority priority-${task.priority}">
                  ${priorityLabels[task.priority] || 'Média'}
                </span>
                ${
                  task.dueDate
                    ? `<span class="tag-date">📅 ${escapeHtml(task.dueDate)}</span>`
                    : ''
                }
              </div>
            </div>
          </div>
          <button
            class="delete-task-btn"
            data-action="delete"
            data-id="${task.id}"
            title="Excluir tarefa"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
            </svg>
          </button>
        </li>
      `;
      })
      .join('');

    // Eventos de checkbox e exclusão
    tasksListEl.querySelectorAll('[data-action="toggle"]').forEach((checkbox) => {
      checkbox.addEventListener('change', (e) => {
        const id = e.target.getAttribute('data-id');
        const targetTask = tasks.find((t) => t.id === id);
        if (targetTask) {
          targetTask.completed = e.target.checked;
          saveTasks(tasks);
          renderTasks();
        }
      });
    });

    tasksListEl.querySelectorAll('[data-action="delete"]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const id = btn.getAttribute('data-id');
        tasks = tasks.filter((t) => t.id !== id);
        saveTasks(tasks);
        renderTasks();
      });
    });
  }

  function getRelativeDateString(daysOffset) {
    const d = new Date();
    d.setDate(d.getDate() + daysOffset);
    return d.toLocaleDateString('pt-BR');
  }

  function formatDate(dateStr) {
    if (!dateStr) return '';
    const parts = dateStr.split('-');
    if (parts.length === 3) {
      return `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
    return dateStr;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
}

/* ==========================================================
   4. LOGOUT
   ========================================================== */
function initLogout() {
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('impacta_user');
      window.location.href = 'login.html';
    });
  }
}

