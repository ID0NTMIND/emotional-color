// static/js/auth.js

document.addEventListener('DOMContentLoaded', function () {
    // Если пользователь уже авторизован, перенаправляем в кабинет
    if (isAuthenticated()) {
        window.location.href = '/dashboard';
    }

    // Активируем вкладку регистрации, если URL содержит ?tab=register
    const params = new URLSearchParams(window.location.search);
    if (params.get('tab') === 'register') {
        const registerTab = document.getElementById('register-tab');
        const loginTab = document.getElementById('login-tab');
        if (registerTab && loginTab) {
            registerTab.classList.add('active');
            loginTab.classList.remove('active');
            document.getElementById('register').classList.add('show', 'active');
            document.getElementById('login').classList.remove('show', 'active');
        }
    }

    // Прямой fetch для авторизации (без apiRequest, чтобы корректно обработать 401)
    async function authFetch(url, body) {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Ошибка авторизации');
        }
        return data;
    }

    // Обработка входа
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        try {
            const data = await authFetch('/auth/login', { username, password });
            localStorage.setItem('access_token', data.access_token);
            document.cookie = `access_token=${data.access_token}; path=/; SameSite=Strict`;
            window.location.href = '/dashboard';
        } catch (err) {
            document.getElementById('authMessage').innerHTML = `<div class="alert alert-danger">⚠️ ${err.message}</div>`;
        }
    });

    // Обработка регистрации
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('regUsername').value;
        const password = document.getElementById('regPassword').value;
        try {
            const data = await authFetch('/auth/register', { username, password });
            localStorage.setItem('access_token', data.access_token);
            document.cookie = `access_token=${data.access_token}; path=/; SameSite=Strict`;
            window.location.href = '/dashboard';
        } catch (err) {
            document.getElementById('authMessage').innerHTML = `<div class="alert alert-danger">⚠️ ${err.message}</div>`;
        }
    });
});