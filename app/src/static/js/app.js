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
        let detail = 'Ошибка запроса';
        try {
            const err = await response.json();
            if (typeof err.detail === 'string') {
                detail = err.detail;
            } else if (Array.isArray(err.detail) && err.detail.length > 0) {
                // Извлекаем сообщения из ошибок Pydantic (422)
                detail = err.detail.map(e => e.msg || e).join(', ');
            } else if (typeof err.detail === 'object' && err.detail !== null) {
                detail = JSON.stringify(err.detail);
            }
        } catch (e) {
            // Если ответ не JSON, оставляем дефолтное сообщение
        }
        throw new Error(detail);
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