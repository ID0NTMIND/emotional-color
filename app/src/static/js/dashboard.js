// static/js/dashboard.js
document.addEventListener('DOMContentLoaded', function () {
    // Если нет токена, перенаправляем на логин
    if (!isAuthenticated()) {
        window.location.href = '/login';
    }

    async function updateBalance() {
        try {
            const data = await apiRequest('/balance');
            document.getElementById('balance').textContent = data.balance;
        } catch (err) {
            document.getElementById('topupMessage').innerHTML = `<div class="alert alert-danger">⚠️ ${err.message}</div>`;
        }
    }

    function getSentimentInfo(label) {
        const map = {
            positive: { emoji: '😊', text: 'Позитивная', cssClass: 'positive' },
            negative: { emoji: '😠', text: 'Негативная', cssClass: 'negative' },
            neutral: { emoji: '😐', text: 'Нейтральная', cssClass: 'neutral' }
        };
        return map[label] || { emoji: '❓', text: label, cssClass: 'neutral' };
    }

    function showPredictionResult(result) {
        const info = getSentimentInfo(result.label);
        document.getElementById('predictResult').innerHTML = `
            <div class="result-box ${info.cssClass}">
                <div class="emotion">${info.emoji}</div>
                <div class="fw-bold fs-5 mt-2">${info.text}</div>
                <div class="text-muted mt-1">Уверенность: ${result.confidence}</div>
            </div>`;
        updateBalance();
    }

    // Пополнение баланса
    document.getElementById('topupBtn').addEventListener('click', async () => {
        const amount = document.getElementById('topupAmount').value;
        if (!amount || amount <= 0) {
            document.getElementById('topupMessage').innerHTML = '<div class="alert alert-danger">⚠️ Введите положительную сумму</div>';
            return;
        }
        try {
            const data = await apiRequest('/balance/topup', 'POST', { amount: parseFloat(amount) });
            document.getElementById('balance').textContent = data.balance;
            document.getElementById('topupMessage').innerHTML = '<div class="alert alert-success">✅ Баланс успешно пополнен!</div>';
        } catch (err) {
            document.getElementById('topupMessage').innerHTML = `<div class="alert alert-danger">⚠️ ${err.message}</div>`;
        }
    });

    // Отправка предсказания
    document.getElementById('predictBtn').addEventListener('click', async () => {
        const text = document.getElementById('textInput').value.trim();
        if (!text) {
            document.getElementById('predictError').innerHTML = '<div class="alert alert-danger">⚠️ Введите текст для анализа</div>';
            return;
        }
        document.getElementById('predictError').innerHTML = '';
        document.getElementById('predictResult').innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Загрузка...</span></div>';

        try {
            const data = await apiRequest('/predict', 'POST', { text });
            updateBalance(); // баланс списан сразу
            if (data.status === 'completed') {
                showPredictionResult(data);
            } else {
                // Ожидание результата через опрос истории
                setTimeout(async () => {
                    try {
                        const hist = await apiRequest('/history/predictions?limit=1');
                        if (hist.length > 0 && hist[0].id === data.task_id) {
                            showPredictionResult(hist[0]);
                        } else {
                            document.getElementById('predictResult').innerHTML = '<div class="alert alert-info">Задача всё ещё обрабатывается. Обновите страницу.</div>';
                        }
                    } catch (e) {
                        document.getElementById('predictResult').innerHTML = '';
                        document.getElementById('predictError').innerHTML = `<div class="alert alert-danger">⚠️ ${e.message}</div>`;
                    }
                }, 2000);
            }
        } catch (err) {
            document.getElementById('predictResult').innerHTML = '';
            document.getElementById('predictError').innerHTML = `<div class="alert alert-danger">⚠️ ${err.message}</div>`;
        }
    });

    // Инициализация
    updateBalance();
});