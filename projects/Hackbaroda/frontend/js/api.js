/**
 * ============================================================================
 * Aetheris API Client
 * ============================================================================
 * Connects the frontend onboarding flow to the backend pipeline at
 * POST http://localhost:8000/pipeline
 * ============================================================================
 */

'use strict';

const API_BASE = 'https://hackbaroda.onrender.com';

const PIPELINE_STAGES = [
    { id: 'scrape', label: 'Scraping Instagram', icon: 'travel_explore' },
    { id: 'rank', label: 'Ranking viral content', icon: 'trending_up' },
    { id: 'analyze', label: 'AI post analysis', icon: 'psychology' },
    { id: 'strategy', label: 'Building strategy', icon: 'architecture' },
    { id: 'save', label: 'Saving results', icon: 'save' },
    { id: 'done', label: 'Complete', icon: 'check_circle' },
];

const DEFAULT_COUNTRIES = [
    'United States', 'Canada', 'United Kingdom', 'Australia',
    'Germany', 'France', 'Italy', 'Spain', 'Netherlands',
    'Brazil', 'Mexico', 'Japan', 'South Korea', 'India',
    'Indonesia', 'United Arab Emirates', 'Turkey',
];

/**
 * Build a rich niche string from brand onboarding + user niche input.
 * Backend accepts niche as a free-form string used in strategy prompts.
 */
const buildNicheContext = (onboarding) => {
    const parts = [onboarding.niche];

    if (onboarding.aestheticDirection?.length) {
        parts.push(`aesthetics: ${onboarding.aestheticDirection.join(', ')}`);
    }
    if (onboarding.brandMaturity) {
        const maturity = onboarding.brandMaturity === 'custom'
            ? onboarding.customMaturity
            : onboarding.brandMaturity;
        if (maturity) parts.push(`maturity: ${maturity}`);
    }
    if (onboarding.goal) {
        const goal = onboarding.goal === 'custom'
            ? onboarding.customObjective
            : onboarding.goal;
        if (goal) parts.push(`goal: ${goal}`);
    }
    if (onboarding.antiPersona) parts.push(`anti-persona: ${onboarding.antiPersona}`);
    if (onboarding.voiceTaboos?.length) {
        parts.push(`taboos: ${onboarding.voiceTaboos.join(', ')}`);
    }
    if (onboarding.visualTexture) parts.push(`visual: ${onboarding.visualTexture}`);

    return parts.filter(Boolean).join(' | ');
};

/**
 * Parse comma/space-separated hashtag input into a clean array.
 */
const parseHashtags = (raw) => {
    if (!raw) return [];
    return [...new Set(
        raw.split(/[,\s#]+/)
            .map((t) => t.trim().toLowerCase())
            .filter(Boolean)
    )];
};

/**
 * Map frontend onboarding state to backend PipelineRequest shape.
 */
const mapOnboardingToPipeline = (onboarding) => ({
    niche: buildNicheContext(onboarding),
    country: onboarding.country || 'United States',
    hashtags: onboarding.hashtags || [],
    scrape_count: onboarding.scrapeCount || 50,
    hashtag_scrape_count: onboarding.hashtagScrapeCount || 50,
    top_n: onboarding.topN || 5,
    weeks: onboarding.weeks || 2,
    use_vision: true,
    save_outputs: true,
});

/**
 * Fetch supported countries from backend (falls back to defaults).
 */
const fetchCountries = async () => {
    try {
        const res = await fetch(`${API_BASE}/countries`);
        if (!res.ok) throw new Error('Failed to fetch countries');
        const data = await res.json();
        return data.countries || DEFAULT_COUNTRIES;
    } catch {
        return DEFAULT_COUNTRIES;
    }
};

/**
 * Health check — verify backend is reachable.
 */
const checkBackendHealth = async () => {
    try {
        const res = await fetch(`${API_BASE}/health`);
        return res.ok;
    } catch {
        return false;
    }
};

/**
 * Run the full pipeline. Returns PipelineResult from backend.
 */
const runPipeline = async (onboarding) => {
    const payload = mapOnboardingToPipeline(onboarding);

    const res = await fetch(`${API_BASE}/pipeline`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
        const detail = data.detail || `Pipeline failed (${res.status})`;
        throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
    }

    return data;
};

window.AetherisAPI = {
    API_BASE,
    PIPELINE_STAGES,
    DEFAULT_COUNTRIES,
    buildNicheContext,
    parseHashtags,
    mapOnboardingToPipeline,
    fetchCountries,
    checkBackendHealth,
    runPipeline,
};
