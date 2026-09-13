/* ==========================================================================
   Aetheris Brand Strategist — app.js
   Main application logic (vanilla JS, no dependencies)
   ========================================================================== */

'use strict';

/* --------------------------------------------------------------------------
   1. STATE STORE
   -------------------------------------------------------------------------- */

const AppState = {
    currentPage: 'landing',
    currentDashboardView: 'content-studio',
    onboarding: {
        socialProfiles: [],
        brandLocation: '',
        brandMaturity: '',
        customMaturity: '',
        aestheticDirection: [],
        goal: '',
        customObjective: '',
        philosophyHeritage: 30,
        philosophyBoldness: 75,
        antiPersona: '',
        voiceTaboos: ['affordable', 'cheap', 'fast', 'hack'],
        visualTexture: 'linen',
        niche: '',
        hashtags: [],
        country: 'United States',
        weeks: 2,
        topN: 5,
        scrapeCount: 50,
        hashtagScrapeCount: 50,
    },
    chat: {
        messages: [],
    },
    artifacts: [],
    pipelineResult: null,
    pipelineRunning: false,
};

/* --------------------------------------------------------------------------
   2. ROUTER
   -------------------------------------------------------------------------- */

/**
 * Navigate to a named page. Hides every `.page-section`, reveals the target,
 * applies enter animation, updates the hash, and scrolls to top.
 * @param {string} pageName — e.g. 'landing', 'onboarding-1', 'dashboard'
 */
const navigateTo = (pageName) => {
    const targetId = `page-${pageName}`;
    const target = document.getElementById(targetId);
    if (!target) {
        console.warn(`[Router] Page not found: #${targetId}`);
        return;
    }

    // Hide all pages
    document.querySelectorAll('.page-section').forEach((section) => {
        section.classList.remove('active', 'page-enter');
        section.style.display = 'none';
    });

    // Show target
    target.style.display = '';
    // Force reflow so the enter animation triggers reliably
    void target.offsetWidth;
    target.classList.add('active', 'page-enter');

    // Update hash (no hashchange loop — we guard below)
    const newHash = `#${pageName}`;
    if (window.location.hash !== newHash) {
        history.pushState(null, '', newHash);
    }

    AppState.currentPage = pageName;
    window.scrollTo({ top: 0, behavior: 'smooth' });

    console.log(`[Router] Navigated to "${pageName}"`);

    // Post-navigation hooks
    if (pageName === 'onboarding-4') populateReview();
    if (pageName === 'dashboard') {
        renderArtifacts();
        initSidebarFirstActive();
        switchDashboardView(AppState.currentDashboardView);
        if (AppState.pipelineResult) {
            renderStrategyBoard();
            renderBrandLibrary();
        }
    }

    // Update progress bar for onboarding pages
    const stepMatch = pageName.match(/^onboarding-(\d)$/);
    if (stepMatch) updateProgressBar(parseInt(stepMatch[1], 10));

    // Re-init scroll reveal for newly-visible content
    initScrollReveal();
};

/** Listen for browser back/forward via hashchange */
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.replace('#', '') || 'landing';
    // Avoid double-navigation if we already updated
    if (hash !== AppState.currentPage) navigateTo(hash);
});

/* --------------------------------------------------------------------------
   3. PROGRESS BAR UPDATER
   -------------------------------------------------------------------------- */

/**
 * Marks `.progress-step` elements inside the current visible page as
 * completed, current, or upcoming based on the given step number.
 * @param {number} stepNumber — 1-based step index
 */
const updateProgressBar = (stepNumber) => {
    const currentPage = document.getElementById(`page-onboarding-${stepNumber}`);
    if (!currentPage) return;

    const steps = currentPage.querySelectorAll('.progress-step');
    steps.forEach((step) => {
        const stepIdx = parseInt(step.dataset.step ?? step.getAttribute('data-step'), 10);
        if (isNaN(stepIdx)) return;

        step.classList.remove('completed', 'current', 'upcoming');
        if (stepIdx < stepNumber) {
            step.classList.add('completed');
        } else if (stepIdx === stepNumber) {
            step.classList.add('current');
        } else {
            step.classList.add('upcoming');
        }
    });
};

/* --------------------------------------------------------------------------
   4. ONBOARDING STEP 1 — Social Profiles, Maturity, Aesthetics
   -------------------------------------------------------------------------- */

let socialRowCounter = 0; // unique key for each row

/**
 * Append a new social-profile input row to the container.
 */
const addSocialProfileRow = () => {
    const container = document.getElementById('social-profiles-container');
    if (!container) return;

    socialRowCounter += 1;
    const row = document.createElement('div');
    row.className = 'social-profile-row flex items-center gap-2 mt-2';
    row.dataset.rowId = socialRowCounter;
    row.innerHTML = `
        <input type="text"
               class="social-profile-input flex-1 bg-transparent border-0 border-b border-outline-variant focus:border-primary focus:ring-0 pl-8 pb-2 text-body-lg font-body text-on-surface transition-colors duration-300 placeholder:text-surface-dim"
               placeholder="https://twitter.com/yourbrand" />
        <button type="button"
                class="btn-remove-profile text-outline hover:text-error transition p-1"
                aria-label="Remove profile"
                data-remove-row="${socialRowCounter}">
            <span class="material-symbols-outlined text-[18px]">close</span>
        </button>
    `;
    container.appendChild(row);
};

/**
 * Remove a social-profile row by its data-row-id.
 */
const removeSocialProfileRow = (rowId) => {
    const row = document.querySelector(`.social-profile-row[data-row-id="${rowId}"]`);
    if (row) row.remove();
};

/**
 * Collect all social profile URLs from the container into AppState.
 */
const collectSocialProfiles = () => {
    const inputs = document.querySelectorAll('#social-profiles-container .social-profile-input');
    AppState.onboarding.socialProfiles = Array.from(inputs)
        .map((el) => el.value.trim())
        .filter(Boolean);
};

/**
 * Handle brand-maturity card selection.
 */
const selectMaturityCard = (card) => {
    document.querySelectorAll('.maturity-card').forEach((c) => c.classList.remove('selected'));
    card.classList.add('selected');

    const value = card.dataset.value;
    AppState.onboarding.brandMaturity = value;

    // Show/hide custom textarea
    const customInput = document.getElementById('custom-maturity-input');
    if (customInput) {
        if (value === 'custom') {
            customInput.classList.remove('hidden');
        } else {
            customInput.classList.add('hidden');
            customInput.value = '';
            AppState.onboarding.customMaturity = '';
        }
    }

    console.log(`[Step1] Brand maturity set to "${value}"`);
};

/** Maximum number of selectable aesthetic chips */
const MAX_AESTHETICS = 3;

/**
 * Toggle an aesthetic chip. Enforces a max of 3 selections.
 */
const toggleAestheticChip = (chip) => {
    const container = chip.closest('.aesthetic-chips-container') || chip.parentElement;
    const value = chip.dataset.value;

    // Handle '+ Custom' chip specially — open inline input
    if (value === 'custom') {
        const customInput = chip.querySelector('.custom-aesthetic-input') || createInlineCustomAesthetic(chip);
        customInput.focus();
        return;
    }

    if (chip.classList.contains('selected')) {
        // Deselect
        chip.classList.remove('selected');
        AppState.onboarding.aestheticDirection = AppState.onboarding.aestheticDirection.filter((v) => v !== value);
    } else {
        // Check max
        if (AppState.onboarding.aestheticDirection.length >= MAX_AESTHETICS) {
            // Shake animation feedback
            if (container) {
                container.classList.add('shake');
                setTimeout(() => container.classList.remove('shake'), 500);
            }
            return;
        }
        chip.classList.add('selected');
        AppState.onboarding.aestheticDirection.push(value);
    }

    console.log('[Step1] Aesthetic direction:', AppState.onboarding.aestheticDirection);
};

/**
 * Create a small inline text input inside the custom aesthetic chip.
 */
const createInlineCustomAesthetic = (chip) => {
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'custom-aesthetic-input bg-transparent border-b border-outline-variant text-on-surface text-sm ml-1 w-24 focus:outline-none focus:border-primary';
    input.placeholder = 'Type…';
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const val = input.value.trim();
            if (val && AppState.onboarding.aestheticDirection.length < MAX_AESTHETICS) {
                AppState.onboarding.aestheticDirection.push(val);
                chip.classList.add('selected');
                chip.dataset.value = val;
                // Replace input with text
                input.replaceWith(document.createTextNode(val));
                console.log('[Step1] Custom aesthetic added:', val);
            }
        }
    });
    // Prevent chip toggle from firing when clicking inside input
    input.addEventListener('click', (e) => e.stopPropagation());
    chip.appendChild(input);
    return input;
};

/**
 * Collect Step 1 data into AppState (called on forward navigation).
 */
const collectStep1 = () => {
    const handleInput = document.getElementById('instagram-handle');
    if (handleInput) AppState.onboarding.socialProfiles.unshift(handleInput.value.trim());

    const locationInput = document.getElementById('brand-location');
    if (locationInput) AppState.onboarding.brandLocation = locationInput.value.trim();

    const nicheInput = document.getElementById('content-niche');
    if (nicheInput) AppState.onboarding.niche = nicheInput.value.trim();

    const hashtagsInput = document.getElementById('content-hashtags');
    if (hashtagsInput && window.AetherisAPI) {
        AppState.onboarding.hashtags = AetherisAPI.parseHashtags(hashtagsInput.value);
    }

    const countrySelect = document.getElementById('content-country');
    if (countrySelect) AppState.onboarding.country = countrySelect.value;

    collectSocialProfiles();

    const customMaturityEl = document.getElementById('custom-maturity-input');
    if (customMaturityEl) AppState.onboarding.customMaturity = customMaturityEl.value.trim();

    // De-duplicate social profiles
    AppState.onboarding.socialProfiles = [...new Set(AppState.onboarding.socialProfiles.filter(Boolean))];

    console.log('[Step1] Collected:', {
        socialProfiles: AppState.onboarding.socialProfiles,
        brandLocation: AppState.onboarding.brandLocation,
        brandMaturity: AppState.onboarding.brandMaturity,
        aestheticDirection: AppState.onboarding.aestheticDirection,
    });
};

/* --------------------------------------------------------------------------
   5. ONBOARDING STEP 2 — Goal / Objective
   -------------------------------------------------------------------------- */

/**
 * Handle goal radio change. Shows/hides the custom textarea.
 */
const handleGoalChange = (value) => {
    AppState.onboarding.goal = value;

    const customTextarea = document.getElementById('custom-objective-textarea');
    if (customTextarea) {
        const shouldShow = value === 'custom';
        customTextarea.style.opacity = shouldShow ? '1' : '0.5';
        customTextarea.style.pointerEvents = shouldShow ? 'auto' : 'none';
        customTextarea.disabled = !shouldShow;
        if (!shouldShow) {
            customTextarea.value = '';
            AppState.onboarding.customObjective = '';
        }
    }

    console.log(`[Step2] Goal set to "${value}"`);
};

/**
 * Collect Step 2 data into AppState.
 */
const collectStep2 = () => {
    const checked = document.querySelector('input[name="goal"]:checked');
    if (checked) AppState.onboarding.goal = checked.value;

    const customTextarea = document.getElementById('custom-objective-textarea');
    if (customTextarea) AppState.onboarding.customObjective = customTextarea.value.trim();

    console.log('[Step2] Collected:', {
        goal: AppState.onboarding.goal,
        customObjective: AppState.onboarding.customObjective,
    });
};

/* --------------------------------------------------------------------------
   6. ONBOARDING STEP 3 — Philosophy, Taboos, Texture
   -------------------------------------------------------------------------- */

/**
 * Handle range-slider input events (heritage / boldness).
 */
const handleSliderInput = (sliderId, value) => {
    if (sliderId === 'slider-heritage') {
        AppState.onboarding.philosophyHeritage = parseInt(value, 10);
    } else if (sliderId === 'slider-boldness') {
        AppState.onboarding.philosophyBoldness = parseInt(value, 10);
    }
};

/**
 * Add a taboo chip to the DOM and AppState.
 * @param {string} word
 * @param {boolean} isDefault — if true, skip dupe-check against defaults
 */
const addTabooChip = (word, isDefault = false) => {
    const trimmed = word.trim().toLowerCase();
    if (!trimmed) return;

    // Prevent duplicates
    if (AppState.onboarding.voiceTaboos.includes(trimmed) && !isDefault) return;

    if (!isDefault) AppState.onboarding.voiceTaboos.push(trimmed);

    const container = document.getElementById('taboo-chips');
    if (!container) return;

    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.dataset.word = trimmed;
    chip.innerHTML = `
        ${escapeHtml(trimmed)}
        <span class="material-symbols-outlined chip-remove" style="font-size:16px;">close</span>
    `;
    container.appendChild(chip);
};

/**
 * Remove a taboo chip from the DOM and AppState.
 */
const removeTabooChip = (chipEl) => {
    const word = chipEl.dataset.word;
    AppState.onboarding.voiceTaboos = AppState.onboarding.voiceTaboos.filter((w) => w !== word);
    chipEl.remove();
    console.log('[Step3] Taboo removed:', word, '| Remaining:', AppState.onboarding.voiceTaboos);
};

/**
 * Render the default taboo chips into the DOM.
 */
const initDefaultTabooChips = () => {
    const container = document.getElementById('taboo-chips');
    if (!container) return;
    // Clear existing chips first
    container.innerHTML = '';
    AppState.onboarding.voiceTaboos.forEach((word) => addTabooChip(word, true));
};

/**
 * Handle texture radio selection.
 */
const handleTextureChange = (value) => {
    AppState.onboarding.visualTexture = value;
    console.log(`[Step3] Visual texture set to "${value}"`);
};

/**
 * Collect Step 3 data into AppState.
 */
const collectStep3 = () => {
    const heritage = document.getElementById('slider-heritage');
    if (heritage) AppState.onboarding.philosophyHeritage = parseInt(heritage.value, 10);

    const boldness = document.getElementById('slider-boldness');
    if (boldness) AppState.onboarding.philosophyBoldness = parseInt(boldness.value, 10);

    const antiPersona = document.getElementById('anti-persona');
    if (antiPersona) AppState.onboarding.antiPersona = antiPersona.value.trim();

    const textureChecked = document.querySelector('input[name="texture"]:checked');
    if (textureChecked) AppState.onboarding.visualTexture = textureChecked.value;

    console.log('[Step3] Collected:', {
        heritage: AppState.onboarding.philosophyHeritage,
        boldness: AppState.onboarding.philosophyBoldness,
        antiPersona: AppState.onboarding.antiPersona,
        voiceTaboos: AppState.onboarding.voiceTaboos,
        visualTexture: AppState.onboarding.visualTexture,
    });
};

/* --------------------------------------------------------------------------
   7. ONBOARDING STEP 4 — Review & Launch
   -------------------------------------------------------------------------- */

/**
 * Populate every #review-* element with human-readable summaries from AppState.
 */
const populateReview = () => {
    const ob = AppState.onboarding;

    // Collect latest data from all steps before rendering
    collectStep1();
    collectStep2();
    collectStep3();

    const set = (id, content) => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = content;
    };

    // Social profiles
    const socials = ob.socialProfiles.length
        ? ob.socialProfiles.map((p) => `<span class="block font-body text-body-sm text-on-surface">• ${escapeHtml(p)}</span>`).join('')
        : '<span class="font-body text-body-sm text-secondary italic">No profiles added</span>';
    set('review-social', socials);

    // Location
    set('review-location', ob.brandLocation
        ? escapeHtml(ob.brandLocation)
        : '<span class="text-secondary italic">Not specified</span>');

    // Brand maturity
    const maturityLabel = ob.brandMaturity === 'custom'
        ? `Custom: ${escapeHtml(ob.customMaturity) || '—'}`
        : capitalize(ob.brandMaturity || '—');
    set('review-maturity', maturityLabel);

    // Aesthetics
    const aesthetics = ob.aestheticDirection.length
        ? ob.aestheticDirection.map((a) => `<span class="inline-block bg-primary-fixed text-on-primary-fixed text-body-sm px-3 py-1 rounded-full mr-1 mb-1">${escapeHtml(a)}</span>`).join('')
        : '<span class="text-secondary italic">None selected</span>';
    set('review-aesthetics', aesthetics);

    // Goal
    const goalLabels = { engagement: 'Deep Engagement', followers: 'Audience Expansion', sales: 'Commercial Conversion' };
    const goalLabel = ob.goal === 'custom'
        ? `Custom: ${escapeHtml(ob.customObjective) || '—'}`
        : goalLabels[ob.goal] || capitalize(ob.goal || '—');
    set('review-goal', goalLabel);

    // Philosophy sliders
    set('review-philosophy', `
        <span class="block font-body text-body-sm text-on-surface">Heritage ←→ Futurism: ${ob.philosophyHeritage}%</span>
        <span class="block font-body text-body-sm text-on-surface">Restraint ←→ Boldness: ${ob.philosophyBoldness}%</span>
    `);

    // Anti-persona
    set('review-anti-persona', ob.antiPersona
        ? `"${escapeHtml(ob.antiPersona)}"`
        : '<span class="text-secondary italic">Not defined</span>');

    // Taboos
    const taboos = ob.voiceTaboos.length
        ? ob.voiceTaboos.map((t) => `<span class="inline-block bg-error-container text-on-error-container text-body-sm px-3 py-1 rounded-full mr-1 mb-1">${escapeHtml(t)}</span>`).join('')
        : '<span class="text-secondary italic">None</span>';
    set('review-taboos', taboos);

    // Texture
    set('review-texture', capitalize(ob.visualTexture || '—'));

    // Pipeline settings
    set('review-niche', ob.niche
        ? escapeHtml(ob.niche)
        : '<span class="text-secondary italic">Not specified</span>');
    set('review-country', escapeHtml(ob.country || 'United States'));
    const hashtagTags = ob.hashtags?.length
        ? ob.hashtags.map((h) => `<span class="inline-block bg-primary-fixed text-on-primary-fixed text-body-sm px-3 py-1 rounded-full mr-1 mb-1">#${escapeHtml(h)}</span>`).join('')
        : '<span class="text-secondary italic">None added</span>';
    set('review-hashtags', hashtagTags);

    const weeksEl = document.getElementById('pipeline-weeks');
    const topNEl = document.getElementById('pipeline-top-n');
    const scrapeEl = document.getElementById('pipeline-scrape-count');
    if (weeksEl) ob.weeks = parseInt(weeksEl.value, 10);
    if (topNEl) ob.topN = parseInt(topNEl.value, 10);
    if (scrapeEl) {
        ob.scrapeCount = parseInt(scrapeEl.value, 10);
        ob.hashtagScrapeCount = parseInt(scrapeEl.value, 10);
    }

    console.log('[Step4] Review populated');
};

/**
 * Validate required pipeline inputs before launch.
 */
const validatePipelineInputs = () => {
    collectStep1();
    collectStep2();
    collectStep3();

    const weeksEl = document.getElementById('pipeline-weeks');
    const topNEl = document.getElementById('pipeline-top-n');
    const scrapeEl = document.getElementById('pipeline-scrape-count');
    if (weeksEl) AppState.onboarding.weeks = parseInt(weeksEl.value, 10);
    if (topNEl) AppState.onboarding.topN = parseInt(topNEl.value, 10);
    if (scrapeEl) {
        AppState.onboarding.scrapeCount = parseInt(scrapeEl.value, 10);
        AppState.onboarding.hashtagScrapeCount = parseInt(scrapeEl.value, 10);
    }

    const errors = [];
    if (!AppState.onboarding.niche) errors.push('Content niche is required');
    if (!AppState.onboarding.hashtags?.length) errors.push('At least one hashtag is required');
    return errors;
};

/**
 * Show the pipeline loading overlay with stage indicators.
 */
const showPipelineOverlay = () => {
    const overlay = document.getElementById('pipeline-overlay');
    const stagesEl = document.getElementById('pipeline-stages');
    if (!overlay || !stagesEl) return;

    stagesEl.innerHTML = (AetherisAPI?.PIPELINE_STAGES || []).map((stage) => `
        <div class="pipeline-stage" data-stage="${stage.id}">
            <span class="material-symbols-outlined pipeline-stage-icon">${stage.icon}</span>
            <span class="pipeline-stage-label">${stage.label}</span>
            <span class="pipeline-stage-status"></span>
        </div>
    `).join('');

    updatePipelineStatus('Connecting to backend…');
    overlay.classList.remove('hidden');
};

const hidePipelineOverlay = () => {
    const overlay = document.getElementById('pipeline-overlay');
    if (overlay) overlay.classList.add('hidden');
};

const updatePipelineStage = (stageId) => {
    const stages = document.querySelectorAll('.pipeline-stage');
    const stageOrder = (AetherisAPI?.PIPELINE_STAGES || []).map((s) => s.id);
    const currentIdx = stageOrder.indexOf(stageId);

    stages.forEach((el) => {
        const id = el.dataset.stage;
        const idx = stageOrder.indexOf(id);
        el.classList.remove('active', 'completed');
        if (idx < currentIdx) el.classList.add('completed');
        else if (idx === currentIdx) el.classList.add('active');
    });
};

const updatePipelineStatus = (text) => {
    const el = document.getElementById('pipeline-status');
    if (el) el.textContent = text;
};

const startPipelineTimer = () => {
    const start = Date.now();
    const elapsedEl = document.getElementById('pipeline-elapsed');
    const interval = setInterval(() => {
        if (!AppState.pipelineRunning) {
            clearInterval(interval);
            return;
        }
        const secs = Math.floor((Date.now() - start) / 1000);
        if (elapsedEl) elapsedEl.textContent = `${secs}s elapsed`;
    }, 1000);
    return interval;
};

/**
 * Simulate stage progress while waiting for the long-running API call.
 */
const simulatePipelineProgress = () => {
    const stages = ['scrape', 'rank', 'analyze', 'strategy', 'save'];
    let idx = 0;
    updatePipelineStage(stages[0]);
    updatePipelineStatus('Scraping Instagram trending & hashtag posts…');

    const interval = setInterval(() => {
        if (!AppState.pipelineRunning) {
            clearInterval(interval);
            return;
        }
        idx = Math.min(idx + 1, stages.length - 1);
        updatePipelineStage(stages[idx]);
        const messages = {
            scrape: 'Scraping Instagram trending & hashtag posts…',
            rank: 'Ranking content by viral score…',
            analyze: 'Deep-analyzing top posts with AI…',
            strategy: 'Generating your content strategy…',
            save: 'Saving results…',
        };
        updatePipelineStatus(messages[stages[idx]] || 'Processing…');
    }, 12000);

    return interval;
};

/**
 * Build artifacts list from pipeline strategy report.
 */
const buildArtifactsFromResult = (result) => {
    const report = result?.strategy_report;
    if (!report) return [];

    const artifacts = [
        { id: 'summary', title: 'Executive Summary', subtitle: report.niche_detected || 'Strategy', time: 'JUST NOW', icon: 'summarize', section: 'summary' },
        { id: 'weekly', title: 'Weekly Content Plan', subtitle: `${report.weekly_plan?.length || 0} days planned`, time: 'JUST NOW', icon: 'calendar_month', section: 'weekly_plan' },
        { id: 'hooks', title: 'Winning Hooks', subtitle: `${report.winning_hooks?.length || 0} patterns identified`, time: 'JUST NOW', icon: 'bolt', section: 'winning_hooks' },
        { id: 'pillars', title: 'Content Pillars', subtitle: `${report.content_pillars?.length || 0} pillars`, time: 'JUST NOW', icon: 'account_tree', section: 'content_pillars' },
        { id: 'posting', title: 'Posting Strategy', subtitle: report.posting_strategy?.frequency || 'Schedule', time: 'JUST NOW', icon: 'schedule', section: 'posting_strategy' },
        { id: 'analyses', title: 'Post Analyses', subtitle: `${report.per_post_analyses?.length || 0} deep dives`, time: 'JUST NOW', icon: 'analytics', section: 'per_post_analyses' },
        { id: 'hashtags', title: 'Hashtag Strategy', subtitle: `${report.hashtag_strategy?.length || 0} recommendations`, time: 'JUST NOW', icon: 'tag', section: 'hashtag_strategy' },
        { id: 'dos-donts', title: 'Do\'s & Don\'ts', subtitle: 'Content guidelines', time: 'JUST NOW', icon: 'rule', section: 'dos_donts' },
    ];

    if (result.suggestions?.length) {
        artifacts.push({
            id: 'trending',
            title: 'Trending Content',
            subtitle: `${result.scraped_count || 0} posts scraped, top ${result.suggestions.length} ranked`,
            time: 'JUST NOW',
            icon: 'trending_up',
            section: 'suggestions',
        });
    }

    return artifacts;
};

/**
 * Render the initial chat welcome with executive summary after pipeline completes.
 */
const renderPipelineChatWelcome = (result) => {
    const container = document.getElementById('chat-messages');
    if (!container) return;
    container.innerHTML = '';

    const report = result?.strategy_report;
    if (!report) {
        appendChatBubble('ai', 'Pipeline completed but no strategy report was returned. Please check backend logs.');
        return;
    }

    const elapsed = result.elapsed_seconds ? ` in ${Math.round(result.elapsed_seconds)}s` : '';
    appendChatBubble('ai', `Your content strategy is ready${elapsed}. I analyzed ${result.scraped_count || 0} Instagram posts and deep-dived into the top performers in the ${report.niche_detected} niche.`);

    let summaryText = report.executive_summary + '\n\n';

    if (report.content_pillars?.length) {
        summaryText += 'Content Pillars:\n';
        report.content_pillars.forEach((pillar) => {
            summaryText += `• ${pillar}\n`;
        });
    }

    appendChatBubble('ai', summaryText.trim());
};

/**
 * Render the full strategy board from pipeline results.
 */
const renderStrategyBoard = () => {
    const container = document.getElementById('strategy-board-content');
    const result = AppState.pipelineResult;
    if (!container) return;

    const report = result?.strategy_report;
    if (!report) {
        container.innerHTML = `<div class="text-center py-16">
            <span class="material-symbols-outlined text-outline text-[48px] mb-4">architecture</span>
            <p class="font-body text-body-lg text-secondary">Launch your strategy to see the full content plan here.</p>
        </div>`;
        return;
    }

    const listItems = (items) => items?.length
        ? `<ul class="strategy-list">${items.map((i) => `<li>${escapeHtml(typeof i === 'string' ? i : i.pattern || JSON.stringify(i))}</li>`).join('')}</ul>`
        : '<p class="text-secondary italic">None</p>';

    const weeklyPlan = report.weekly_plan?.map((day) => `
        <div class="strategy-day-card">
            <div class="strategy-day-header">
                <span class="font-headline text-headline-md text-primary">${escapeHtml(day.day)}</span>
                <span class="strategy-badge">${escapeHtml(day.content_type)}</span>
            </div>
            <p class="font-body text-body-md text-on-surface font-medium mt-2">${escapeHtml(day.topic)}</p>
            <p class="font-body text-body-sm text-secondary mt-1"><strong>Hook:</strong> ${escapeHtml(day.hook)}</p>
            <p class="font-body text-body-sm text-on-surface-variant mt-2">${escapeHtml(day.script_outline)}</p>
            <p class="font-body text-body-sm text-on-surface-variant mt-2"><strong>Caption:</strong> ${escapeHtml(day.caption_framework)}</p>
            ${day.hashtags?.length ? `<div class="flex flex-wrap gap-1 mt-2">${day.hashtags.map((h) => `<span class="strategy-tag">#${escapeHtml(h.replace('#', ''))}</span>`).join('')}</div>` : ''}
            <p class="font-label text-label-caps text-secondary uppercase tracking-widest mt-3">Post at ${escapeHtml(day.best_posting_time)}</p>
        </div>
    `).join('') || '';

    const postAnalyses = report.per_post_analyses?.map((post) => `
        <div class="strategy-day-card">
            <div class="strategy-day-header">
                <span class="font-headline text-body-md text-primary">#${post.rank} @${escapeHtml(post.username)}</span>
                <span class="strategy-badge">${escapeHtml(post.format_label || post.content_type)}</span>
            </div>
            <p class="font-body text-body-sm text-secondary mt-1">${escapeHtml(post.hook_analysis)}</p>
            <p class="font-body text-body-sm text-on-surface-variant mt-2">${escapeHtml(post.why_viral?.join('. ') || '')}</p>
            ${post.url ? `<a href="${escapeHtml(post.url)}" target="_blank" rel="noopener" class="font-body text-body-sm text-primary hover:underline mt-2 inline-block">View original post →</a>` : ''}
        </div>
    `).join('') || '';

    container.innerHTML = `
        <header class="strategy-board-header">
            <h2 class="font-display text-headline-lg text-primary">Content Strategy</h2>
            <p class="font-body text-body-md text-secondary">${escapeHtml(report.niche_detected)} · ${report.weekly_plan?.length || 0}-day plan</p>
        </header>

        <section class="strategy-section">
            <h3 class="font-headline text-headline-md text-primary">Executive Summary</h3>
            <p class="font-body text-body-md text-on-surface mt-3">${escapeHtml(report.executive_summary)}</p>
        </section>

        <section class="strategy-section">
            <h3 class="font-headline text-headline-md text-primary">Weekly Content Plan</h3>
            <div class="flex flex-col gap-4 mt-4">${weeklyPlan}</div>
        </section>

        <section class="strategy-section">
            <h3 class="font-headline text-headline-md text-primary">Winning Hooks</h3>
            <div class="flex flex-col gap-4 mt-4">
                ${(report.winning_hooks || []).map((hook) => `
                    <div class="strategy-day-card">
                        <p class="font-body text-body-md text-on-surface font-medium">${escapeHtml(hook.pattern)}</p>
                        <p class="font-body text-body-sm text-secondary mt-1">Example: "${escapeHtml(hook.example_from_scrape)}"</p>
                        <p class="font-body text-body-sm text-on-surface-variant mt-1">${escapeHtml(hook.why_it_works)}</p>
                        <p class="font-body text-body-sm text-primary mt-2">${escapeHtml(hook.how_to_use)}</p>
                    </div>
                `).join('')}
            </div>
        </section>

        <section class="strategy-section">
            <h3 class="font-headline text-headline-md text-primary">Posting Strategy</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div class="strategy-day-card">
                    <p class="font-label text-label-caps text-secondary uppercase tracking-widest">Frequency</p>
                    <p class="font-body text-body-md text-on-surface mt-1">${escapeHtml(report.posting_strategy?.frequency || '—')}</p>
                </div>
                <div class="strategy-day-card">
                    <p class="font-label text-label-caps text-secondary uppercase tracking-widest">Format Mix</p>
                    <p class="font-body text-body-md text-on-surface mt-1">${escapeHtml(report.posting_strategy?.format_mix || '—')}</p>
                </div>
            </div>
            ${report.posting_strategy?.best_times?.length ? `<p class="font-body text-body-sm text-on-surface-variant mt-3">Best times: ${report.posting_strategy.best_times.map(escapeHtml).join(', ')}</p>` : ''}
        </section>

        <section class="strategy-section">
            <h3 class="font-headline text-headline-md text-primary">Post Deep Analyses</h3>
            <div class="flex flex-col gap-4 mt-4">${postAnalyses}</div>
        </section>

        <section class="strategy-section grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <h3 class="font-headline text-headline-md text-primary">Do's</h3>
                ${listItems(report.content_dos)}
            </div>
            <div>
                <h3 class="font-headline text-headline-md text-primary">Don'ts</h3>
                ${listItems(report.content_donts)}
            </div>
        </section>
    `;
};

/**
 * Render brand library from onboarding data.
 */
const renderBrandLibrary = () => {
    const container = document.getElementById('brand-library-content');
    if (!container) return;

    const ob = AppState.onboarding;
    container.innerHTML = `
        <h2 class="font-display text-headline-lg text-primary">Brand Library</h2>
        <p class="font-body text-body-md text-secondary">Your brand foundation used to shape the content strategy.</p>
        <div class="bg-surface-container-lowest rounded-lg border border-surface-variant p-6 mt-4 flex flex-col gap-4">
            <div><span class="font-label text-label-caps text-secondary uppercase tracking-widest">Niche</span><p class="font-body text-body-md mt-1">${escapeHtml(ob.niche || '—')}</p></div>
            <div><span class="font-label text-label-caps text-secondary uppercase tracking-widest">Location</span><p class="font-body text-body-md mt-1">${escapeHtml(ob.brandLocation || '—')}</p></div>
            <div><span class="font-label text-label-caps text-secondary uppercase tracking-widest">Maturity</span><p class="font-body text-body-md mt-1 capitalize">${escapeHtml(ob.brandMaturity === 'custom' ? ob.customMaturity : ob.brandMaturity || '—')}</p></div>
            <div><span class="font-label text-label-caps text-secondary uppercase tracking-widest">Aesthetics</span><p class="font-body text-body-md mt-1">${ob.aestheticDirection?.map(escapeHtml).join(', ') || '—'}</p></div>
            <div><span class="font-label text-label-caps text-secondary uppercase tracking-widest">Anti-Persona</span><p class="font-body text-body-md mt-1 italic">${escapeHtml(ob.antiPersona || '—')}</p></div>
            <div><span class="font-label text-label-caps text-secondary uppercase tracking-widest">Voice Taboos</span><p class="font-body text-body-md mt-1">${ob.voiceTaboos?.map(escapeHtml).join(', ') || '—'}</p></div>
        </div>
    `;
};

/**
 * Render artifact detail in main view.
 */
const renderArtifactDetail = (artifact) => {
    const container = document.getElementById('artifacts-detail-content');
    const result = AppState.pipelineResult;
    const report = result?.strategy_report;
    if (!container || !report) return;

    let content = '';

    switch (artifact.section) {
        case 'summary':
            content = `<h2 class="font-display text-headline-lg text-primary">Executive Summary</h2>
                <p class="font-body text-body-lg text-on-surface mt-4">${escapeHtml(report.executive_summary)}</p>`;
            break;
        case 'weekly_plan':
            content = `<h2 class="font-display text-headline-lg text-primary">Weekly Plan</h2>
                <div class="flex flex-col gap-4 mt-6">${(report.weekly_plan || []).map((day) => `
                    <div class="strategy-day-card">
                        <strong>${escapeHtml(day.day)}</strong> — ${escapeHtml(day.topic)}
                        <p class="font-body text-body-sm text-secondary mt-1">${escapeHtml(day.hook)}</p>
                    </div>`).join('')}</div>`;
            break;
        case 'winning_hooks':
            content = `<h2 class="font-display text-headline-lg text-primary">Winning Hooks</h2>
                ${(report.winning_hooks || []).map((h) => `<div class="strategy-day-card mt-4"><p class="font-medium">${escapeHtml(h.pattern)}</p><p class="text-sm text-secondary mt-1">${escapeHtml(h.how_to_use)}</p></div>`).join('')}`;
            break;
        case 'per_post_analyses':
            content = `<h2 class="font-display text-headline-lg text-primary">Post Analyses</h2>
                ${(report.per_post_analyses || []).map((p) => `<div class="strategy-day-card mt-4"><strong>#${p.rank} @${escapeHtml(p.username)}</strong><p class="text-sm mt-2">${escapeHtml(p.hook_analysis)}</p><p class="text-sm text-secondary mt-1">${escapeHtml(p.visual_style)}</p></div>`).join('')}`;
            break;
        case 'suggestions':
            content = `<h2 class="font-display text-headline-lg text-primary">Top Trending Content</h2>
                ${(result.suggestions || []).map((s) => `<div class="strategy-day-card mt-4"><strong>#${s.rank}</strong> @${escapeHtml(s.item?.username || '')}<p class="text-sm mt-1">${escapeHtml(s.why_trending)}</p></div>`).join('')}`;
            break;
        default:
            content = `<h2 class="font-display text-headline-lg text-primary">${escapeHtml(artifact.title)}</h2>
                <p class="font-body text-body-md text-secondary mt-4">${escapeHtml(artifact.subtitle)}</p>
                <p class="font-body text-body-sm text-on-surface-variant mt-4">Open Strategy Board for the full view.</p>`;
    }

    container.innerHTML = content;
};

/**
 * Switch between dashboard views (content-studio, strategy-board, etc.)
 */
const switchDashboardView = (viewName) => {
    AppState.currentDashboardView = viewName;

    document.querySelectorAll('.dashboard-view').forEach((el) => el.classList.add('hidden'));
    const viewMap = {
        'content-studio': 'view-content-studio',
        'artifacts': 'view-artifacts',
        'strategy-board': 'view-strategy-board',
        'brand-library': 'view-brand-library',
    };
    const targetId = viewMap[viewName];
    const target = document.getElementById(targetId);
    if (target) target.classList.remove('hidden');

    const mobileHeader = document.querySelector('.chat-main .md\\:hidden span.font-headline');
    const titles = {
        'content-studio': 'Content Studio',
        'artifacts': 'Artifacts',
        'strategy-board': 'Strategy Board',
        'brand-library': 'Brand Library',
    };
    if (mobileHeader) mobileHeader.textContent = titles[viewName] || 'Dashboard';
};

/**
 * Launch the strategy — call backend pipeline and navigate to dashboard.
 */
const launchStrategy = async () => {
    const errors = validatePipelineInputs();
    if (errors.length) {
        alert('Please complete required fields:\n\n• ' + errors.join('\n• '));
        return;
    }

    if (!window.AetherisAPI) {
        alert('API client not loaded. Make sure api.js is included.');
        return;
    }

    const healthy = await AetherisAPI.checkBackendHealth();
    if (!healthy) {
        alert('Backend is not running.\n\nStart it with:\ncd backend\nuvicorn api:app --reload');
        return;
    }

    console.log('[Launch] Starting pipeline with:', JSON.stringify(AppState.onboarding, null, 2));

    AppState.pipelineRunning = true;
    showPipelineOverlay();
    const progressInterval = simulatePipelineProgress();
    const timerInterval = startPipelineTimer();

    try {
        const result = await AetherisAPI.runPipeline(AppState.onboarding);
        AppState.pipelineResult = result;
        AppState.artifacts = buildArtifactsFromResult(result);

        updatePipelineStage('done');
        updatePipelineStatus(`Complete! Analyzed ${result.scraped_count || 0} posts in ${Math.round(result.elapsed_seconds || 0)}s`);

        await new Promise((r) => setTimeout(r, 800));
        hidePipelineOverlay();

        navigateTo('dashboard');
        renderPipelineChatWelcome(result);
        renderArtifacts();
        renderStrategyBoard();
        renderBrandLibrary();
    } catch (err) {
        console.error('[Launch] Pipeline failed:', err);
        updatePipelineStatus(`Error: ${err.message}`);
        await new Promise((r) => setTimeout(r, 2000));
        hidePipelineOverlay();
        alert(`Pipeline failed:\n\n${err.message}\n\nMake sure backend is running and .env has APIFY_API_TOKEN and OPENAI_API_KEY.`);
    } finally {
        AppState.pipelineRunning = false;
        clearInterval(progressInterval);
        clearInterval(timerInterval);
    }
};

/* --------------------------------------------------------------------------
   8. DASHBOARD LOGIC — Sidebar, Chat, Artifacts
   -------------------------------------------------------------------------- */

// ---- 8a. Sidebar (mobile) ------------------------------------------------

const openSidebar = () => {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    if (sidebar) sidebar.classList.add('open');
    if (overlay) overlay.classList.add('active');
};

const closeSidebar = () => {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
};

/**
 * Mark the first sidebar nav item as active on initial dashboard load.
 */
const initSidebarFirstActive = () => {
    const items = document.querySelectorAll('.sidebar-nav-item');
    if (items.length && !document.querySelector('.sidebar-nav-item.active')) {
        items[0].classList.add('active');
    }
};

/**
 * Handle sidebar navigation item clicks.
 */
const selectSidebarItem = (item) => {
    document.querySelectorAll('.sidebar-nav-item').forEach((el) => el.classList.remove('active'));
    item.classList.add('active');
    const section = item.dataset.section;
    switchDashboardView(section);
    console.log(`[Dashboard] Sidebar section selected: "${section}"`);
    closeSidebar();
};

// ---- 8b. Chat -------------------------------------------------------------

/**
 * Load chat history from localStorage.
 */
const loadChatHistory = () => {
    try {
        const history = localStorage.getItem('aetheris_chat_history');
        if (history) {
            const messages = JSON.parse(history);
            AppState.chat.messages = [];
            const container = document.getElementById('chat-messages');
            if (container) container.innerHTML = '';
            messages.forEach(m => appendChatBubble(m.role, m.text, m.htmlContent, true));
        }
    } catch (e) {
        console.error('Failed to load chat history', e);
    }
};

/**
 * Generate a unique message ID.
 */
let msgIdCounter = 0;
const nextMsgId = () => `msg-${++msgIdCounter}`;

/**
 * Append a message bubble to #chat-messages.
 * @param {'user'|'ai'} role
 * @param {string} text
 * @param {string} htmlContent
 * @param {boolean} isLoadingHistory
 */
const appendChatBubble = (role, text, htmlContent = null, isLoadingHistory = false) => {
    const container = document.getElementById('chat-messages');
    if (!container) return;

    const id = nextMsgId();
    const isUser = role === 'user';

    const wrapper = document.createElement('div');
    wrapper.id = id;
    wrapper.className = `chat-message flex items-start gap-4 p-6 border-b border-outline-variant/20 w-full`;

    const iconWrap = document.createElement('div');
    iconWrap.className = `w-10 h-10 rounded-sm flex items-center justify-center shrink-0 mt-1 ${isUser ? 'bg-primary text-on-primary' : 'bg-surface-container-high text-primary'}`;
    iconWrap.innerHTML = isUser ? '<span class="material-symbols-outlined text-[18px]">person</span>' : '<span class="material-symbols-outlined text-[18px]" style="font-variation-settings: \'FILL\' 1;">auto_awesome</span>';
    
    wrapper.appendChild(iconWrap);

    const bubble = document.createElement('div');
    bubble.className = 'flex-1 min-w-0';
    
    const roleLabel = document.createElement('p');
    roleLabel.className = 'font-label text-label-caps text-secondary uppercase tracking-widest mb-2';
    roleLabel.textContent = isUser ? 'You' : 'Aetheris AI';
    bubble.appendChild(roleLabel);

    if (htmlContent) {
        const htmlWrap = document.createElement('div');
        htmlWrap.innerHTML = htmlContent;
        bubble.appendChild(htmlWrap);
    } else {
        const textWrap = document.createElement('div');
        textWrap.className = 'font-body text-body-md text-on-surface whitespace-pre-wrap leading-relaxed';
        textWrap.innerHTML = escapeHtml(text);
        bubble.appendChild(textWrap);
    }

    wrapper.appendChild(bubble);
    container.appendChild(wrapper);
    scrollChatToBottom();

    if (!isLoadingHistory) {
        AppState.chat.messages.push({ id, role, text, htmlContent, timestamp: Date.now() });
        localStorage.setItem('aetheris_chat_history', JSON.stringify(AppState.chat.messages));
    }

    return id;
};

/**
 * Show a typing indicator (three animated dots).
 * @returns {HTMLElement} the indicator element (so it can be removed later)
 */
const showTypingIndicator = () => {
    const container = document.getElementById('chat-messages');
    if (!container) return null;

    const wrapper = document.createElement('div');
    wrapper.id = 'typing-indicator';
    wrapper.className = 'chat-message flex items-start gap-4 p-6 border-b border-outline-variant/20 w-full';

    wrapper.innerHTML = `
        <div class="w-10 h-10 rounded-sm bg-surface-container-high text-primary flex items-center justify-center shrink-0 mt-1">
            <span class="material-symbols-outlined text-[18px]" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
        </div>
        <div class="flex-1 min-w-0">
            <p class="font-label text-label-caps text-secondary uppercase tracking-widest mb-2">Aetheris AI</p>
            <div class="flex items-center gap-2 mt-2">
                <span class="typing-dot w-2 h-2 bg-outline rounded-full inline-block animate-bounce" style="animation-delay:0ms"></span>
                <span class="typing-dot w-2 h-2 bg-outline rounded-full inline-block animate-bounce" style="animation-delay:150ms"></span>
                <span class="typing-dot w-2 h-2 bg-outline rounded-full inline-block animate-bounce" style="animation-delay:300ms"></span>
            </div>
        </div>
    `;
    container.appendChild(wrapper);
    scrollChatToBottom();
    return wrapper;
};

/**
 * Remove the typing indicator if present.
 */
const removeTypingIndicator = () => {
    const ind = document.getElementById('typing-indicator');
    if (ind) ind.remove();
};

/**
 * Scroll the chat container to the bottom smoothly.
 */
const scrollChatToBottom = () => {
    const container = document.getElementById('chat-messages');
    if (container) {
        container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
    }
};

/**
 * Generate AI post and image.
 */
const generateAIPost = async () => {
    try {
        const report = AppState.pipelineResult?.strategy_report;
        if (!report) {
            appendChatBubble('ai', "I need a completed strategy before I can generate a post. Please launch the strategy pipeline first.");
            return;
        }

        appendChatBubble('ai', "Generating abstract, highly detailed passage and accompanying image. Please wait...");
        
        const payload = {
            niche: report.niche_detected || AppState.onboarding.niche,
            topic: report.executive_summary || "Brand Strategy",
            brand_context: AppState.onboarding.antiPersona + " " + (AppState.onboarding.voiceTaboos || []).join(", ")
        };

        const res = await fetch(`${AetherisAPI.API_BASE}/generate-post`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!res.ok) throw new Error("Failed to generate post.");
        const data = await res.json();
        
        let html = `<div class="ai-post-result flex flex-col gap-6 mt-4">`;
        if (data.image_b64) {
            html += `<img src="data:image/png;base64,${data.image_b64}" class="w-full max-w-lg rounded-xl shadow-lg border border-outline-variant/20" alt="AI Generated Post Image" />`;
        }
        html += `<div class="font-body text-body-lg leading-relaxed text-on-surface whitespace-pre-wrap">${escapeHtml(data.passage)}</div></div>`;
        
        appendChatBubble('ai', "[Generated Post & Image]", html);
    } catch (e) {
        console.error(e);
        appendChatBubble('ai', "Error generating post: " + e.message);
    }
};

/**
 * Handle chat send action.
 */
const sendChatMessage = () => {
    const input = document.getElementById('chat-input');
    if (!input) return;

    const message = input.value.trim();
    if (!message) return;

    // Render user bubble & clear input
    appendChatBubble('user', message);
    input.value = '';

    const indicator = showTypingIndicator();

    if (message.toLowerCase() === '/generate post') {
        generateAIPost().then(() => removeTypingIndicator());
        return;
    }

    setTimeout(() => {
        removeTypingIndicator();
        const report = AppState.pipelineResult?.strategy_report;
        let response;

        if (!report) {
            response = "Launch your strategy first to get AI-powered insights. Complete onboarding and click Launch Strategy.";
        } else if (/weekly|plan|schedule|day/i.test(message)) {
            const days = (report.weekly_plan || []).map((d) => `${d.day}: ${d.topic} (${d.content_type})`).join('\n');
            response = `Here's your weekly plan:\n\n${days}`;
        } else if (/hook/i.test(message)) {
            response = (report.winning_hooks || []).map((h) => `• ${h.pattern}\n  ${h.how_to_use}`).join('\n\n') || 'No hooks found.';
        } else if (/hashtag/i.test(message)) {
            response = `Recommended hashtags:\n${(report.hashtag_strategy || []).join(', ')}`;
        } else if (/post|analy/i.test(message)) {
            response = (report.per_post_analyses || []).map((p) => `@${p.username}: ${p.hook_analysis}`).join('\n\n') || 'No analyses yet.';
        } else if (/pillar/i.test(message)) {
            response = `Content pillars:\n${(report.content_pillars || []).map((p) => `• ${p}`).join('\n')}`;
        } else if (/do|don't|dont/i.test(message)) {
            response = `Do's:\n${(report.content_dos || []).map((d) => `• ${d}`).join('\n')}\n\nDon'ts:\n${(report.content_donts || []).map((d) => `• ${d}`).join('\n')}`;
        } else {
            response = `${report.executive_summary}\n\nTry asking about: weekly plan, hooks, hashtags, post analyses, or content pillars.`;
        }

        appendChatBubble('ai', response);
    }, 1200);

    console.log('[Chat] User sent:', message);
};

// ---- 8c. Artifacts --------------------------------------------------------

/**
 * Render the artifacts list from AppState into #artifacts-panel.
 */
const renderArtifacts = () => {
    const list = document.getElementById('artifacts-list');
    if (!list) return;

    if (!AppState.artifacts.length) {
        list.innerHTML = `<p class="font-body text-body-sm text-secondary text-center py-8 italic">Artifacts will appear after your strategy is generated.</p>`;
        return;
    }

    list.innerHTML = AppState.artifacts
        .map(
            (a) => `
        <div class="artifact-card flex items-start gap-3 p-4 rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors duration-200" data-artifact-id="${a.id}">
            <div class="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-primary text-[20px]">${a.icon}</span>
            </div>
            <div class="flex-1 min-w-0">
                <p class="font-body text-body-md text-on-surface font-medium truncate">${escapeHtml(a.title)}</p>
                <p class="font-body text-body-sm text-secondary truncate">${escapeHtml(a.subtitle)}</p>
                <span class="font-label text-label-caps text-secondary uppercase tracking-widest">${a.time}</span>
            </div>
        </div>
    `
        )
        .join('');

    console.log(`[Dashboard] Rendered ${AppState.artifacts.length} artifacts`);
};

/* --------------------------------------------------------------------------
   9. SCROLL REVEAL (IntersectionObserver)
   -------------------------------------------------------------------------- */

let revealObserver = null;

/**
 * (Re-)initialize the IntersectionObserver for `.reveal-item` elements.
 */
const initScrollReveal = () => {
    // Disconnect previous observer
    if (revealObserver) revealObserver.disconnect();

    const items = document.querySelectorAll('.reveal-item');
    if (!items.length) return;

    revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    revealObserver.unobserve(entry.target); // only once
                }
            });
        },
        { threshold: 0.15 }
    );

    items.forEach((item) => {
        // Reset visibility for fresh pages so the animation replays
        if (!item.classList.contains('is-visible')) {
            revealObserver.observe(item);
        }
    });
};

/* --------------------------------------------------------------------------
   10. UTILITIES
   -------------------------------------------------------------------------- */

/**
 * Minimal HTML-escape to prevent XSS when injecting user input.
 */
const escapeHtml = (str) => {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
};

/**
 * Capitalize first letter.
 */
const capitalize = (s) => (s ? s.charAt(0).toUpperCase() + s.slice(1) : '');

/* --------------------------------------------------------------------------
   11. EVENT DELEGATION & INITIALIZATION
   -------------------------------------------------------------------------- */

/**
 * Central delegated click handler on document.body.
 */
const handleBodyClick = (e) => {
    const target = e.target;

    // ---- Navigation links [data-navigate] ----
    const navEl = target.closest('[data-navigate]');
    if (navEl) {
        e.preventDefault();
        const dest = navEl.dataset.navigate;

        // Collect current step data before navigating forward
        if (AppState.currentPage === 'onboarding-1') collectStep1();
        if (AppState.currentPage === 'onboarding-2') collectStep2();
        if (AppState.currentPage === 'onboarding-3') collectStep3();

        navigateTo(dest);
        return;
    }

    // ---- Mobile nav toggle ----
    if (target.closest('#mobile-menu-btn')) {
        const mobileNav = document.getElementById('mobile-nav');
        if (mobileNav) mobileNav.classList.toggle('hidden');
        return;
    }

    // ---- Custom aesthetic input toggle ----
    if (target.closest('.aesthetic-chip[data-value="custom"]')) {
        const customInput = document.getElementById('custom-aesthetic-input');
        if (customInput) {
            customInput.classList.toggle('hidden');
            if (!customInput.classList.contains('hidden')) customInput.focus();
        }
        return;
    }

    // ---- Add social profile ----
    if (target.closest('#btn-add-profile')) {
        addSocialProfileRow();
        return;
    }

    // ---- Remove social profile row ----
    const removeBtn = target.closest('[data-remove-row]');
    if (removeBtn) {
        removeSocialProfileRow(removeBtn.dataset.removeRow);
        return;
    }

    // ---- Maturity card ----
    const maturityCard = target.closest('.maturity-card');
    if (maturityCard) {
        selectMaturityCard(maturityCard);
        return;
    }

    // ---- Aesthetic chip ----
    const aestheticChip = target.closest('.aesthetic-chip');
    if (aestheticChip) {
        toggleAestheticChip(aestheticChip);
        return;
    }

    // ---- Taboo chip remove ----
    const chipRemove = target.closest('.chip-remove');
    if (chipRemove) {
        const chip = chipRemove.closest('.chip');
        if (chip) removeTabooChip(chip);
        return;
    }

    // ---- Goal option label ----
    const goalOption = target.closest('.goal-option');
    if (goalOption) {
        const radio = goalOption.querySelector('input[name="goal"]') || goalOption.previousElementSibling;
        if (radio && radio.type === 'radio') {
            radio.checked = true;
            handleGoalChange(radio.value);
        }
        return;
    }

    // ---- Launch button ----
    if (target.closest('#btn-launch')) {
        launchStrategy();
        return;
    }

    // ---- Sidebar toggle (mobile) ----
    if (target.closest('#sidebar-toggle')) {
        openSidebar();
        return;
    }
    if (target.closest('#sidebar-close') || target.closest('#sidebar-overlay')) {
        closeSidebar();
        return;
    }

    // ---- Sidebar nav item ----
    const sidebarItem = target.closest('.sidebar-nav-item');
    if (sidebarItem) {
        selectSidebarItem(sidebarItem);
        return;
    }

    // ---- Chat send ----
    if (target.closest('#btn-send-chat')) {
        sendChatMessage();
        return;
    }

    // ---- Attachment button (placeholder) ----
    if (target.closest('#btn-attachment')) {
        console.log('[Chat] Attachment button clicked (not yet implemented)');
        return;
    }

    // ---- Artifact card click ----
    const artifactCard = target.closest('.artifact-card');
    if (artifactCard) {
        const id = artifactCard.dataset.artifactId;
        const artifact = AppState.artifacts.find((a) => String(a.id) === String(id));
        if (artifact) {
            renderArtifactDetail(artifact);
            switchDashboardView('artifacts');
            document.querySelectorAll('.sidebar-nav-item').forEach((el) => el.classList.remove('active'));
            const artifactsNav = document.querySelector('.sidebar-nav-item[data-section="artifacts"]');
            if (artifactsNav) artifactsNav.classList.add('active');
        }
        return;
    }

    // ---- View all artifacts ----
    if (target.closest('#btn-view-artifacts')) {
        switchDashboardView('strategy-board');
        document.querySelectorAll('.sidebar-nav-item').forEach((el) => el.classList.remove('active'));
        const boardNav = document.querySelector('.sidebar-nav-item[data-section="strategy-board"]');
        if (boardNav) boardNav.classList.add('active');
        return;
    }

    // ---- Sign out ----
    if (target.closest('#btn-sign-out')) {
        console.log('[Auth] Signing out');
        navigateTo('landing');
        return;
    }

    // ---- Upgrade ----
    if (target.closest('#btn-upgrade')) {
        console.log('[Billing] Upgrade to Pro clicked');
        return;
    }
};

/**
 * Central delegated change handler for radios & selects.
 */
const handleBodyChange = (e) => {
    const target = e.target;

    // Goal radios
    if (target.name === 'goal' && target.type === 'radio') {
        handleGoalChange(target.value);
        return;
    }

    // Texture radios
    if (target.name === 'texture' && target.type === 'radio') {
        handleTextureChange(target.value);
        return;
    }
};

/**
 * Central delegated input handler for sliders & textareas.
 */
const handleBodyInput = (e) => {
    const target = e.target;

    // Range sliders
    if (target.id === 'slider-heritage' || target.id === 'slider-boldness') {
        handleSliderInput(target.id, target.value);
        return;
    }

    // Anti-persona textarea
    if (target.id === 'anti-persona') {
        AppState.onboarding.antiPersona = target.value.trim();
        return;
    }

    // Custom maturity textarea
    if (target.id === 'custom-maturity-input') {
        AppState.onboarding.customMaturity = target.value.trim();
        return;
    }

    // Custom objective textarea
    if (target.id === 'custom-objective-textarea') {
        AppState.onboarding.customObjective = target.value.trim();
        return;
    }
};

/**
 * Keydown delegation — chat enter, taboo enter.
 */
const handleBodyKeydown = (e) => {
    const target = e.target;

    // Chat input — Enter to send
    if (target.id === 'chat-input' && e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendChatMessage();
        return;
    }

    // Taboo input — Enter to add chip
    if (target.id === 'taboo-input' && e.key === 'Enter') {
        e.preventDefault();
        addTabooChip(target.value);
        target.value = '';
        return;
    }

    // Custom aesthetic input — Enter to add as a chip
    if (target.id === 'custom-aesthetic-input' && e.key === 'Enter') {
        e.preventDefault();
        const val = target.value.trim();
        if (val && AppState.onboarding.aestheticDirection.length < MAX_AESTHETICS) {
            AppState.onboarding.aestheticDirection.push(val);
            // Create a visual selected chip in the container
            const container = document.getElementById('aesthetic-chips-container');
            if (container) {
                const newChip = document.createElement('button');
                newChip.className = 'aesthetic-chip selected px-5 py-2 rounded-full border border-primary bg-primary text-on-primary font-body text-body-sm transition-colors';
                newChip.type = 'button';
                newChip.dataset.value = val;
                newChip.textContent = val;
                container.insertBefore(newChip, container.lastElementChild);
            }
            target.value = '';
            target.classList.add('hidden');
            console.log('[Step1] Custom aesthetic added:', val);
        }
        return;
    }
};

/**
 * Master initializer — called once on DOMContentLoaded.
 */
/**
 * Populate the country dropdown from backend /countries endpoint.
 */
const initCountryDropdown = async () => {
    const select = document.getElementById('content-country');
    if (!select || !window.AetherisAPI) return;

    const countries = await AetherisAPI.fetchCountries();
    select.innerHTML = countries.map((c) =>
        `<option value="${escapeHtml(c)}"${c === 'United States' ? ' selected' : ''}>${escapeHtml(c)}</option>`
    ).join('');
};

const init = () => {
    console.log('[Aetheris] Initializing application…');

    document.body.addEventListener('click', handleBodyClick);
    document.body.addEventListener('change', handleBodyChange);
    document.body.addEventListener('input', handleBodyInput);
    document.body.addEventListener('keydown', handleBodyKeydown);

    initDefaultTabooChips();
    initCountryDropdown();
    
    loadChatHistory();

    const hash = window.location.hash.replace('#', '') || 'landing';
    navigateTo(hash);

    initScrollReveal();

    console.log('[Aetheris] Application ready ✓');
};

document.addEventListener('DOMContentLoaded', init);
