function isAuthenticated() {
    return document.cookie.split(';').some(c => c.trim().startsWith('access_token='));
}

async function apiRequest(url, method = 'GET', body = null) {
    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: body ? JSON.stringify(body) : null
    });

    if (response.status === 401) {
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
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    window.location.href = '/login';
}

document.addEventListener('DOMContentLoaded', function () {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});