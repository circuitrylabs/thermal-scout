const ThermalScout = (() => {
    const state = {
        models: []
    };

    const API_BASE = 'https://huggingface.co/api/models';

    const elements = {
        searchForm: null,
        searchInput: null,
        resultsContainer: null,
        resultsCount: null,
        loading: null,
        error: null
    };

    function init() {
        cacheElements();
        bindEvents();
    }

    function cacheElements() {
        elements.searchForm = document.getElementById('search-form');
        elements.searchInput = document.getElementById('search-input');
        elements.resultsContainer = document.getElementById('results-container');
        elements.resultsCount = document.getElementById('results-count');
        elements.loading = document.getElementById('loading');
        elements.error = document.getElementById('error');
    }

    function bindEvents() {
        elements.searchForm.addEventListener('submit', handleSearch);
    }


    async function handleSearch(e) {
        e.preventDefault();
        

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


        const response = await fetch(`${API_BASE}?${params}`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        return data;
    }


    function getModelParameters(model) {
        // Try to get parameters from various sources
        if (model.safetensors?.parameters?.total) {
            return model.safetensors.parameters.total;
        }
        
        // Try to extract from model ID (e.g., "7B" in name)
        const match = model.id?.match(/(\d+\.?\d*)B/i) || model.modelId?.match(/(\d+\.?\d*)B/i);
        if (match) {
            return parseFloat(match[1]) * 1e9;
        }
        
        // Default to unknown
        return 0;
    }


    function getThermalIndicator(parameters) {
        if (parameters < 1e9) return 'Cool';
        if (parameters < 3e9) return 'Warm';
        if (parameters < 7e9) return 'Moderate';
        return 'Hot';
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

        const modelId = model.id || model.modelId;
        const downloads = model.downloads || 0;
        const likes = model.likes || 0;
        
        card.innerHTML = `
            <a href="https://huggingface.co/${modelId}" 
               target="_blank" 
               rel="noopener noreferrer"
               class="model-name-link">
                <h3 class="model-name">${modelId}</h3>
            </a>
            <p class="model-task">${model.pipeline_tag || 'General'}</p>
            <div class="model-stats">
                <span class="thermal-indicator ${thermalClass}">${thermal} ${size}</span>
                <span class="model-popularity">↓ ${formatNumber(downloads)} · ♥ ${likes}</span>
            </div>
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
        if (parameters === 0) return '';
        if (parameters < 1e9) return `(${Math.round(parameters / 1e6)}M)`;
        return `(${(parameters / 1e9).toFixed(1)}B)`;
    }
    
    function formatNumber(num) {
        if (num >= 1e6) return `${(num / 1e6).toFixed(1)}M`;
        if (num >= 1e3) return `${(num / 1e3).toFixed(1)}K`;
        return num.toString();
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



    return {
        init
    };
})();

document.addEventListener('DOMContentLoaded', ThermalScout.init);