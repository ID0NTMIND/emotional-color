// static/js/history.js
document.addEventListener('DOMContentLoaded', function () {
    if (!isAuthenticated()) {
        window.location.href = '/login';
    }

    function formatDate(isoString) {
        if (!isoString) return '-';
        const date = new Date(isoString);
        return date.toLocaleString('ru-RU');
    }

    function renderTransactions(transactions) {
        const container = document.getElementById('transactionsContainer');
        if (!transactions.length) {
            container.innerHTML = '<div class="text-muted">История транзакций пуста.</div>';
            return;
        }
        const table = `
            <table class="table table-striped">
                <thead><tr><th>Дата</th><th>Тип</th><th>Сумма</th><th>Задача</th></tr></thead>
                <tbody>
                    ${transactions.map(t => `
                        <tr>
                            <td>${formatDate(t.timestamp)}</td>
                            <td>${t.type === 'credit' ? 'Пополнение' : 'Списание'}</td>
                            <td>${t.amount}</td>
                            <td>${t.task_id || '-'}</td>
                        </tr>`).join('')}
                </tbody>
            </table>`;
        container.innerHTML = table;
    }

    function renderPredictions(predictions) {
        const container = document.getElementById('predictionsContainer');
        if (!predictions.length) {
            container.innerHTML = '<div class="text-muted">История предсказаний пуста.</div>';
            return;
        }
        const table = `
            <table class="table table-striped">
                <thead><tr><th>Дата</th><th>Модель</th><th>Текст</th><th>Статус</th><th>Результат</th></tr></thead>
                <tbody>
                    ${predictions.map(p => `
                        <tr>
                            <td>${formatDate(p.created_at)}</td>
                            <td>${p.model_name}</td>
                            <td>${p.input_data.length > 40 ? p.input_data.slice(0, 40) + '…' : p.input_data}</td>
                            <td>${p.status}</td>
                            <td>${p.label ? `${p.label} (${p.confidence})` : '-'}</td>
                        </tr>`).join('')}
                </tbody>
            </table>`;
        container.innerHTML = table;
    }

    async function loadHistory() {
        try {
            const [transactions, predictions] = await Promise.all([
                apiRequest('/history/transactions?limit=100'),
                apiRequest('/history/predictions?limit=100')
            ]);
            renderTransactions(transactions);
            renderPredictions(predictions);
        } catch (err) {
            document.getElementById('transactionsContainer').innerHTML = `<div class="alert alert-danger">⚠️ ${err.message}</div>`;
            document.getElementById('predictionsContainer').innerHTML = `<div class="alert alert-danger">⚠️ ${err.message}</div>`;
        }
    }

    loadHistory();
});