// Estado da Aplicação
let currentShortUrl = '';

// Troca de Abas
function switchTab(tabName) {
    const tabs = ['encurtar', 'buscar'];
    tabs.forEach(t => {
        const btn = document.getElementById(`tab-${t}`);
        const content = document.getElementById(`content-${t}`);
        if (btn && content) {
            if (t === tabName) {
                btn.classList.add('active');
                btn.setAttribute('aria-selected', 'true');
                content.classList.add('active');
            } else {
                btn.classList.remove('active');
                btn.setAttribute('aria-selected', 'false');
                content.classList.remove('active');
            }
        }
    });
}

// Sistema de Toasts
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = type === 'success' 
        ? '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#10B981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        : '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#EF4444" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';

    toast.innerHTML = `${icon}<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-fadeout');
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// Encurtar URL
async function handleEncurtar(event) {
    event.preventDefault();
    const input = document.getElementById('input-url');
    const submitBtn = document.getElementById('btn-submit-encurtar');
    const url = input.value.trim();

    if (!url) {
        showToast('Por favor, digite uma URL válida.', 'error');
        return;
    }

    const originalBtnHtml = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Encurtando...</span>';

    try {
        const response = await fetch('/api/encurtar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (response.ok && data.sucesso) {
            currentShortUrl = data.url_encurtada;

            // Atualiza Card de Resultado
            const resultCard = document.getElementById('result-card');
            const resultShortUrl = document.getElementById('result-short-url');
            const resultOriginalUrl = document.getElementById('result-original-url');
            const resultCode = document.getElementById('result-code');
            const resultOpenLink = document.getElementById('btn-open-link');
            const resultStatusTitle = document.getElementById('result-status-title');

            resultShortUrl.textContent = data.url_encurtada;
            resultShortUrl.href = data.url_encurtada;
            resultOpenLink.href = data.url_encurtada;
            resultOriginalUrl.textContent = data.url_original;
            resultCode.textContent = `#${data.codigo}`;
            
            resultStatusTitle.textContent = data.ja_existia 
                ? 'Link já existente recuperado!' 
                : 'Link encurtado com sucesso!';

            resultCard.style.display = 'block';

            showToast(data.ja_existia ? 'URL já existia e foi recuperada!' : 'Link encurtado com sucesso!', 'success');

            // Atualiza lista de links da sessão
            carregarHistorico();
        } else {
            showToast(data.mensagem || 'Erro ao encurtar URL.', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Erro de conexão com o servidor.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHtml;
    }
}

// Copiar URL do resultado principal
function copyResultUrl() {
    if (!currentShortUrl) return;
    copyToClipboard(currentShortUrl, 'Link encurtado copiado!');
    
    const copyBtn = document.getElementById('btn-copy');
    const copyText = document.getElementById('copy-btn-text');
    
    if (copyBtn && copyText) {
        copyBtn.classList.add('copied');
        copyText.textContent = 'Copiado!';
        setTimeout(() => {
            copyBtn.classList.remove('copied');
            copyText.textContent = 'Copiar';
        }, 2000);
    }
}

// Copiar texto genérico para o clipboard
function copyToClipboard(text, successMsg = 'Copiado para a área de transferência!') {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showToast(successMsg, 'success');
        }).catch(() => fallbackCopy(text, successMsg));
    } else {
        fallbackCopy(text, successMsg);
    }
}

function fallbackCopy(text, successMsg) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
        showToast(successMsg, 'success');
    } catch (err) {
        showToast('Não foi possível copiar automaticamente.', 'error');
    }
    document.body.removeChild(textArea);
}

// Buscar / Redirecionar
async function handleBuscar(event) {
    event.preventDefault();
    const input = document.getElementById('input-busca');
    const submitBtn = document.getElementById('btn-submit-buscar');
    const termo = input.value.trim();

    if (!termo) {
        showToast('Por favor, informe o código ou a URL encurtada.', 'error');
        return;
    }

    const originalBtnHtml = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Buscando...</span>';

    try {
        const response = await fetch('/api/buscar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ termo })
        });

        const data = await response.json();

        const searchResultCard = document.getElementById('search-result-card');
        const searchResultCode = document.getElementById('search-result-code');
        const searchResultDestino = document.getElementById('search-result-destino');
        const btnSearchRedirect = document.getElementById('btn-search-redirect');

        if (response.ok && data.sucesso) {
            searchResultCode.textContent = `#${data.codigo}`;
            searchResultDestino.textContent = data.destino;
            searchResultDestino.href = data.destino;
            btnSearchRedirect.href = data.destino;

            searchResultCard.style.display = 'block';
            showToast('Destino encontrado com sucesso!', 'success');
        } else {
            searchResultCard.style.display = 'none';
            showToast(data.mensagem || 'Link ou código inexistente!', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Erro de conexão ao buscar.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHtml;
    }
}

// Carregar Histórico da Sessão
async function carregarHistorico() {
    try {
        const response = await fetch('/api/links');
        const data = await response.json();

        const historyList = document.getElementById('history-list');
        const historyCount = document.getElementById('history-count');
        const emptyState = document.getElementById('empty-state');

        if (!historyList || !data.sucesso) return;

        historyCount.textContent = `${data.total} ${data.total === 1 ? 'link' : 'links'}`;

        if (data.total === 0) {
            if (emptyState) emptyState.style.display = 'flex';
            historyList.innerHTML = `
                <div class="empty-state" id="empty-state">
                    <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                        <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                    </svg>
                    <p>Nenhum link encurtado nesta sessão ainda.</p>
                    <span>Encurte seu primeiro link acima para vê-lo aqui!</span>
                </div>
            `;
            return;
        }

        historyList.innerHTML = '';

        data.links.forEach(item => {
            const el = document.createElement('div');
            el.className = 'history-item';
            el.innerHTML = `
                <div class="history-info">
                    <div class="history-short-line">
                        <a href="${item.url_encurtada}" target="_blank" class="history-short-link">${item.url_encurtada}</a>
                        <span class="code-badge">#${item.codigo}</span>
                    </div>
                    <div class="history-orig-link" title="${item.url_original}">
                        ${item.url_original}
                    </div>
                </div>
                <div class="history-actions">
                    <button type="button" class="btn-icon" onclick="copyToClipboard('${item.url_encurtada}', 'Link copiado!')" title="Copiar link encurtado">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                        </svg>
                        <span>Copiar</span>
                    </button>
                    <a href="${item.url_encurtada}" target="_blank" class="btn-icon" title="Abrir link">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                            <polyline points="15 3 21 3 21 9"></polyline>
                            <line x1="10" y1="14" x2="21" y2="3"></line>
                        </svg>
                    </a>
                </div>
            `;
            historyList.appendChild(el);
        });
    } catch (err) {
        console.error('Erro ao carregar histórico:', err);
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    carregarHistorico();
});
