// static/js/app.js

function getToken() {
    return localStorage.getItem('access_token');
}

function isAuthenticated() {
    return !!getToken();
}

async function apiRequest(url, method = 'GET', body = null) {
    const headers = {
        'Authorization': 'Bearer ' + getToken(),
        'Content-Type': 'application/json'
    };
    const response = await fetch(url, {
        method: method,
        headers: headers,
        body: body ? JSON.stringify(body) : null
    });
    if (response.status === 401) {
        localStorage.removeItem('access_token');
        document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
        window.location.href = '/login';
        throw new Error('Требуется авторизация');
    }
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Ошибка запроса');
    }
    return response.json();
}

function logout() {
    localStorage.removeItem('access_token');
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    window.location.href = '/login';
}

// Глобальный обработчик кнопки выхода
document.addEventListener('DOMContentLoaded', function () {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});