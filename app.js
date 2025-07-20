const ThermalScout = (() => {
    const state = {
        apiKey: localStorage.getItem('hf_api_key'),
        models: [],
        filters: {
            thermal: 'all',
            openOnly: true
        }
    };

    const API_BASE = 'https://huggingface.co/api/models';

    const elements = {
        searchForm: null,
        searchInput: null,
        resultsContainer: null,
        resultsCount: null,
        loading: null,
        error: null,
        apiForm: null,
        apiKeyInput: null,
        clearDataBtn: null
    };

    function init() {
        cacheElements();
        bindEvents();
        checkApiKey();
    }

    function cacheElements() {
        elements.searchForm = document.getElementById('search-form');
        elements.searchInput = document.getElementById('search-input');
        elements.resultsContainer = document.getElementById('results-container');
        elements.resultsCount = document.getElementById('results-count');
        elements.loading = document.getElementById('loading');
        elements.error = document.getElementById('error');
        elements.apiForm = document.getElementById('api-form');
        elements.apiKeyInput = document.getElementById('api-key-input');
        elements.clearDataBtn = document.getElementById('clear-data');
    }

    function bindEvents() {
        elements.searchForm.addEventListener('submit', handleSearch);
        elements.apiForm.addEventListener('submit', handleApiKeySave);
        elements.clearDataBtn.addEventListener('click', handleClearData);

        document.querySelectorAll('input[name="thermal"]').forEach(input => {
            input.addEventListener('change', handleFilterChange);
        });

        document.querySelector('input[name="license"]').addEventListener('change', handleFilterChange);
    }

    function checkApiKey() {
        if (!state.apiKey) {
            showMessage('Please add your HuggingFace API key below to search models');
        }
    }

    async function handleSearch(e) {
        e.preventDefault();
        
        if (!state.apiKey) {
            showError('API key required. Please add it below.');
            return;
        }

        const query = elements.searchInput.value.trim();
        if (!query) return;

        showLoading();
        hideError();

        try {
            const models = await searchModels(query);
            displayResults(models);
        } catch (err) {
            showError('Failed to search models. Please try again.');
            console.error('Search error:', err);
        } finally {
            hideLoading();
        }
    }

    async function searchModels(query) {
        const params = new URLSearchParams({
            search: query,
            limit: '30',
            full: 'true'
        });

        if (state.filters.openOnly) {
            params.append('filter', 'license:apache-2.0,license:mit,license:openrail');
        }

        const response = await fetch(`${API_BASE}?${params}`, {
            headers: {
                'Authorization': `Bearer ${state.apiKey}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        return filterByThermal(data);
    }

    function filterByThermal(models) {
        if (state.filters.thermal === 'all') return models;

        return models.filter(model => {
            const params = getModelParameters(model);
            const thermal = getThermalCategory(params);
            return thermal === state.filters.thermal;
        });
    }

    function getModelParameters(model) {
        if (model.safetensors?.parameters?.total) {
            return model.safetensors.parameters.total;
        }
        
        const match = model.modelId?.match(/(\d+)B/i);
        if (match) {
            return parseFloat(match[1]) * 1e9;
        }
        
        return 0;
    }

    function getThermalCategory(parameters) {
        if (parameters < 1e9) return 'cool';
        if (parameters < 3e9) return 'warm';
        if (parameters < 7e9) return 'moderate';
        return 'hot';
    }

    function getThermalIndicator(parameters) {
        if (parameters < 1e9) return '·';
        if (parameters < 3e9) return '🔥';
        if (parameters < 7e9) return '🔥🔥';
        return '🔥🔥🔥';
    }

    function displayResults(models) {
        elements.resultsContainer.innerHTML = '';
        elements.resultsCount.textContent = `Found ${models.length} models`;

        if (models.length === 0) {
            elements.resultsContainer.innerHTML = '<p>No models found. Try different search terms or filters.</p>';
            return;
        }

        models.forEach(model => {
            const card = createModelCard(model);
            elements.resultsContainer.appendChild(card);
        });
    }

    function createModelCard(model) {
        const card = document.createElement('article');
        card.className = 'model-card';

        const params = getModelParameters(model);
        const thermal = getThermalIndicator(params);
        const thermalClass = getThermalClass(params);
        const size = formatSize(params);

        card.innerHTML = `
            <h3>${model.modelId}</h3>
            <p>${model.pipeline_tag || 'Unknown task'}</p>
            <p>
                <span class="thermal-indicator ${thermalClass}">${thermal}</span>
                <span>${size}</span>
            </p>
            <p>
                <a href="https://huggingface.co/${model.modelId}" 
                   target="_blank" 
                   rel="noopener noreferrer">
                    View on HuggingFace →
                </a>
            </p>
        `;

        return card;
    }

    function getThermalClass(parameters) {
        if (parameters < 1e9) return 'thermal-cool';
        if (parameters < 3e9) return 'thermal-warm';
        if (parameters < 7e9) return 'thermal-moderate';
        return 'thermal-hot';
    }

    function formatSize(parameters) {
        if (parameters === 0) return 'Size unknown';
        if (parameters < 1e9) return `${Math.round(parameters / 1e6)}M parameters`;
        return `${(parameters / 1e9).toFixed(1)}B parameters`;
    }

    function handleFilterChange() {
        const thermalFilter = document.querySelector('input[name="thermal"]:checked');
        const licenseFilter = document.querySelector('input[name="license"]');

        state.filters.thermal = thermalFilter.value;
        state.filters.openOnly = licenseFilter.checked;

        if (elements.resultsContainer.children.length > 0) {
            elements.searchForm.dispatchEvent(new Event('submit'));
        }
    }

    function handleApiKeySave(e) {
        e.preventDefault();

        const consent = e.target.consent.checked;
        if (!consent) {
            showError('Consent required to store API key');
            return;
        }

        const apiKey = elements.apiKeyInput.value.trim();
        if (!apiKey.startsWith('hf_')) {
            showError('Invalid API key format');
            return;
        }

        localStorage.setItem('hf_api_key', apiKey);
        state.apiKey = apiKey;
        
        elements.apiKeyInput.value = '';
        e.target.consent.checked = false;
        
        showMessage('API key saved successfully!');
    }

    function handleClearData() {
        if (confirm('Clear all stored data including your API key?')) {
            localStorage.clear();
            state.apiKey = null;
            elements.resultsContainer.innerHTML = '';
            elements.resultsCount.textContent = 'Ready to search';
            showMessage('All data cleared');
        }
    }

    function showLoading() {
        elements.loading.hidden = false;
        elements.resultsContainer.hidden = true;
    }

    function hideLoading() {
        elements.loading.hidden = true;
        elements.resultsContainer.hidden = false;
    }

    function showError(message) {
        elements.error.hidden = false;
        elements.error.querySelector('p').textContent = message;
    }

    function hideError() {
        elements.error.hidden = true;
    }

    function showMessage(message) {
        elements.resultsCount.textContent = message;
    }

    return {
        init
    };
})();

document.addEventListener('DOMContentLoaded', ThermalScout.init);