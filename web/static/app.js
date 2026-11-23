/**
 * STRATIFY SaaS Dashboard Interactive Engine
 */

let currentReport = null;
let currentDepth = "standard";

// Security utility: escape HTML entities to prevent DOM XSS
function escapeHtml(str) {
  if (typeof str !== 'string') return str === undefined || str === null ? '' : String(str);
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
}

document.addEventListener("DOMContentLoaded", () => {
  // Initialize Lucide icons
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Setup event listeners
  setupThemeToggle();
  setupTabs();
  setupForm();
  setupQuickPills();
  setupDepthPicker();
  setupProspectSearch();
  setupExport();
  setupModals();

  // Load initial research report for Healthcare Philippines by default
  executeStratifyCommand("/stratify Healthcare --location Philippines --depth standard");
});

// Theme Management
function setupThemeToggle() {
  const themeBtn = document.getElementById("themeToggleBtn");
  const sunIcon = document.getElementById("sunIcon");
  const moonIcon = document.getElementById("moonIcon");

  // Check saved theme or system preference
  const isDark = localStorage.getItem("stratify_theme") !== "light";
  applyTheme(isDark);

  themeBtn.addEventListener("click", () => {
    const currentlyDark = document.documentElement.classList.contains("dark");
    applyTheme(!currentlyDark);
  });

  function applyTheme(dark) {
    if (dark) {
      document.documentElement.classList.add("dark");
      sunIcon.classList.remove("hidden");
      moonIcon.classList.add("hidden");
      localStorage.setItem("stratify_theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      sunIcon.classList.add("hidden");
      moonIcon.classList.remove("hidden");
      localStorage.setItem("stratify_theme", "light");
    }
  }
}

// Tab Switching
function setupTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => {
        t.classList.remove("active", "border-indigo-600", "text-indigo-600", "dark:text-indigo-400", "font-semibold");
        t.classList.add("text-gray-500", "dark:text-gray-400");
      });
      tab.classList.add("active", "border-indigo-600", "text-indigo-600", "dark:text-indigo-400", "font-semibold");
      tab.classList.remove("text-gray-500", "dark:text-gray-400");

      const targetId = tab.getAttribute("data-tab");
      document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.add("hidden"));
      const targetPane = document.getElementById(targetId);
      if (targetPane) {
        targetPane.classList.remove("hidden");
      }
    });
  });
}

// Command Form Submission
function setupForm() {
  const form = document.getElementById("stratifyForm");
  const input = document.getElementById("commandInput");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const cmd = input.value.trim();
    if (!cmd) return;
    executeStratifyCommand(cmd);
  });
}

// Quick Industry Pills
function setupQuickPills() {
  const pills = document.querySelectorAll(".industry-pill");
  const input = document.getElementById("commandInput");

  pills.forEach(pill => {
    pill.addEventListener("click", () => {
      const ind = pill.getAttribute("data-ind");
      input.value = `${ind} --depth ${currentDepth}`;
      executeStratifyCommand(input.value);
    });
  });
}

// Depth Picker
function setupDepthPicker() {
  const depthBtns = document.querySelectorAll(".depth-btn");
  const input = document.getElementById("commandInput");

  depthBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      depthBtns.forEach(b => {
        b.classList.remove("bg-white", "dark:bg-darkbg-600", "font-semibold", "text-indigo-600", "dark:text-indigo-300", "shadow-sm");
        b.classList.add("text-gray-600", "dark:text-gray-300");
      });
      btn.classList.add("bg-white", "dark:bg-darkbg-600", "font-semibold", "text-indigo-600", "dark:text-indigo-300", "shadow-sm");
      btn.classList.remove("text-gray-600", "dark:text-gray-300");

      currentDepth = btn.getAttribute("data-depth");
      let val = input.value;
      if (val.includes("--depth")) {
        val = val.replace(/--depth\s+(quick|standard|deep)/i, `--depth ${currentDepth}`);
      } else {
        val = `${val.trim()} --depth ${currentDepth}`;
      }
      input.value = val;
    });
  });
}

// High-Value Prospect Search
function setupProspectSearch() {
  const searchInput = document.getElementById("prospectSearchInput");
  searchInput.addEventListener("input", (e) => {
    const q = e.target.value.toLowerCase().trim();
    const rows = document.querySelectorAll("#prospectsTableBody tr");
    rows.forEach(r => {
      const text = r.textContent.toLowerCase();
      r.style.display = text.includes(q) ? "" : "none";
    });
  });
}

// Export Dropdown
function setupExport() {
  const btn = document.getElementById("exportDropdownBtn");
  const menu = document.getElementById("exportMenu");

  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    menu.classList.toggle("hidden");
  });

  document.addEventListener("click", () => {
    menu.classList.add("hidden");
  });

  document.getElementById("exportMdBtn").addEventListener("click", (e) => {
    e.preventDefault();
    if (!currentReport) return;
    window.location.href = `/api/stratify/export/${currentReport.report_id}?format=markdown`;
  });

  document.getElementById("exportJsonBtn").addEventListener("click", (e) => {
    e.preventDefault();
    if (!currentReport) return;
    window.location.href = `/api/stratify/export/${currentReport.report_id}?format=json`;
  });
}

// Modals Setup (Opportunities, History, Comparison)
function setupModals() {
  // Opportunity deep-dive modal
  const oppModal = document.getElementById("oppModal");
  document.getElementById("closeOppModalBtn").addEventListener("click", () => {
    oppModal.classList.add("hidden");
  });

  // History modal
  const histModal = document.getElementById("historyModal");
  document.getElementById("historyBtn").addEventListener("click", () => {
    loadHistoryList();
    histModal.classList.remove("hidden");
  });
  document.getElementById("closeHistoryModalBtn").addEventListener("click", () => {
    histModal.classList.add("hidden");
  });

  // Compare modal
  const compModal = document.getElementById("compareModal");
  document.getElementById("openCompareModalBtn").addEventListener("click", () => {
    compModal.classList.remove("hidden");
  });
  document.getElementById("closeCompareModalBtn").addEventListener("click", () => {
    compModal.classList.add("hidden");
  });

  // Compare Form Submission
  document.getElementById("compareForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const ind1 = document.getElementById("compInd1").value.trim();
    const ind2 = document.getElementById("compInd2").value.trim();
    const loc = document.getElementById("compLoc").value.trim();
    compModal.classList.add("hidden");

    let cmd = `compare ${ind1} vs ${ind2}`;
    if (loc) cmd += ` --location ${loc}`;
    executeStratifyCommand(cmd);
  });
}

// Main Execution Call to Backend API
async function executeStratifyCommand(cmdStr) {
  const statusBox = document.getElementById("orchestratorStatus");
  const runBtn = document.getElementById("runBtn");
  const timerSpan = document.getElementById("statusTimer");
  const statusHeading = document.getElementById("statusHeading");
  const statusSubheading = document.getElementById("statusSubheading");

  // Show live progress UI
  statusBox.classList.remove("hidden");
  runBtn.disabled = true;

  let startTime = Date.now();
  let timerInterval = setInterval(() => {
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    timerSpan.textContent = `${elapsed}s`;
  }, 100);

  // Animate steps
  setTimeout(() => {
    statusHeading.textContent = "Step 2: Activating Dynamic Skill Router";
    statusSubheading.textContent = "Selecting high-affinity marketing skills and pruning unneeded instructions...";
  }, 300);

  try {
    const response = await fetch("/api/stratify/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: cmdStr })
    });

    const data = await response.json();
    clearInterval(timerInterval);
    statusBox.classList.add("hidden");
    runBtn.disabled = false;

    if (!data.success || !data.report) {
      alert("Error generating research: " + (data.detail || "Unknown error"));
      return;
    }

    currentReport = data.report;
    renderDashboardReport(currentReport);
  } catch (err) {
    clearInterval(timerInterval);
    statusBox.classList.add("hidden");
    runBtn.disabled = false;
    console.error("STRATIFY run error:", err);
    alert("Connection error executing STRATIFY command.");
  }
}

// Render Dashboard Data
function renderDashboardReport(rep) {
  // Check if comparison report
  if (rep.comparison_id) {
    renderComparisonView(rep);
    return;
  }

  // Header Title & Badges
  document.getElementById("reportIndustryTitle").textContent = rep.industry;
  document.getElementById("reportLocationBadge").textContent = rep.location;
  document.getElementById("reportDepthBadge").textContent = rep.depth;
  document.getElementById("reportDuration").textContent = `${rep.execution_duration_sec}s`;
  document.getElementById("reportSkillCount").textContent = `${rep.skill_routing.selected_count}/${rep.skill_routing.total_skills_available}`;
  document.getElementById("reportTotalTokens").textContent = rep.token_metrics.total_tokens.toLocaleString();

  // Top Score
  document.getElementById("topOppScoreNumber").textContent = rep.top_opportunity_score;
  document.getElementById("topOppNameSummary").textContent = rep.top_ranked_opportunity || "Scored Strategy";

  // Navigation Pill
  document.getElementById("tokenCountNav").textContent = rep.token_metrics.total_tokens.toLocaleString();
  document.getElementById("efficiencyNav").textContent = `${rep.skill_routing.efficiency_percentage}% Saved`;

  // SECTION A: Market Overview
  const mkt = rep.market_overview;
  document.getElementById("tamValue").textContent = mkt.tam;
  document.getElementById("samValue").textContent = mkt.sam;
  document.getElementById("somValue").textContent = mkt.som;
  document.getElementById("cagrValue").textContent = mkt.cagr;
  document.getElementById("maturityValue").textContent = mkt.market_maturity;
  document.getElementById("marketOverviewText").textContent = mkt.market_overview;

  // Key Trends
  const trendsList = document.getElementById("marketTrendsList");
  trendsList.innerHTML = mkt.key_trends.map(t => `
    <li class="flex items-start space-x-2 text-gray-700 dark:text-gray-300">
      <span class="text-indigo-500 font-bold">✓</span>
      <span>${t}</span>
    </li>
  `).join("");

  // Regulatory Tags
  const regTags = document.getElementById("regulatoryTags");
  regTags.innerHTML = mkt.regulatory_frameworks.map(r => `
    <span class="px-2.5 py-1 text-xs rounded-md bg-gray-100 dark:bg-darkbg-700 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-darkbg-600 font-medium">
      ${r}
    </span>
  `).join("");

  // Industry Risks
  const risksList = document.getElementById("industryRisksList");
  risksList.innerHTML = mkt.industry_risks.map(risk => `
    <li class="flex items-start space-x-1.5">
      <span class="text-amber-500 font-bold">•</span>
      <span>${risk}</span>
    </li>
  `).join("");

  // Citations
  const citationsGrid = document.getElementById("citationsGrid");
  citationsGrid.innerHTML = rep.citations.map(c => `
    <div class="p-3 rounded-xl bg-gray-50 dark:bg-darkbg-700/60 border border-gray-200 dark:border-darkbg-600 flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-1">
          <span class="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded ${c.classification === 'VERIFIED_FACT' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300'}">
            ${c.classification}
          </span>
          <span class="text-[11px] text-gray-400 font-mono">${c.publication_year || '2024'}</span>
        </div>
        <p class="text-xs font-semibold text-gray-800 dark:text-gray-200 mb-1">${c.source_name}</p>
        <p class="text-[11px] text-gray-500 line-clamp-1">${c.claim}</p>
      </div>
      <a href="${c.source_url}" target="_blank" rel="noopener noreferrer" class="mt-2 text-[11px] text-indigo-500 hover:text-indigo-400 font-medium flex items-center space-x-1">
        <span>Verify Source</span>
        <i data-lucide="external-link" class="w-3 h-3"></i>
      </a>
    </div>
  `).join("");

  // SECTION B: Opportunities
  document.getElementById("oppTabCount").textContent = rep.opportunities.length;
  document.getElementById("oppTotalCountText").textContent = rep.opportunities.length;
  renderOpportunities(rep.opportunities);

  // SECTION C: Customer Intelligence
  renderCustomerIntelligence(rep.customer_intelligence);

  // SECTION D: High-Value Targets
  document.getElementById("prospectTabCount").textContent = rep.prospects.length;
  renderProspectsTable(rep.prospects);

  // SECTION E: Competitors
  renderCompetitors(rep.competitor_intelligence);

  // SECTION F: Marketing Strategy
  renderMarketingStrategy(rep.marketing_strategy);

  // SECTION G: 90-Day Action Roadmap
  renderActionPlan(rep.business_strategy);

  // SECTION H: Telemetry & Token Accounting
  renderTelemetry(rep.token_metrics, rep.skill_routing);

  // Re-initialize Lucide Icons on dynamic DOM elements
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// Render Opportunities
function renderOpportunities(opps) {
  const container = document.getElementById("opportunitiesContainer");
  container.innerHTML = opps.map((opp, idx) => `
    <div class="bg-white dark:bg-darkbg-800 rounded-2xl p-6 border border-gray-200 dark:border-darkbg-700 hover:border-indigo-400 dark:hover:border-indigo-600 transition shadow-sm">
      <div class="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-4">
        <div>
          <div class="flex items-center space-x-2 mb-1.5">
            <span class="text-xs font-bold text-gray-400 font-mono">#${idx+1}</span>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white">${opp.name}</h3>
            <span class="px-2.5 py-0.5 text-xs font-semibold rounded-full ${opp.execution_difficulty.includes('Low') ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : (opp.execution_difficulty.includes('Medium') ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300')}">
              ${opp.execution_difficulty}
            </span>
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">${opp.concept}</p>
        </div>

        <!-- Score Badge & Deep Dive Button -->
        <div class="flex md:flex-col items-end justify-between shrink-0">
          <div class="text-right">
            <span class="text-2xl font-black text-indigo-600 dark:text-indigo-400">${opp.overall_score}</span>
            <span class="text-xs text-gray-400">/ 100</span>
          </div>
          <button class="mt-2 text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center space-x-1" onclick="openOppDeepDive(${idx})">
            <span>Score Breakdown</span>
            <i data-lucide="chevron-right" class="w-3.5 h-3.5"></i>
          </button>
        </div>
      </div>

      <!-- Opportunity Spec Details Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-3 border-t border-gray-100 dark:border-darkbg-700 text-xs">
        <div>
          <span class="text-gray-400 font-semibold block mb-0.5">Target Buyer:</span>
          <span class="text-gray-800 dark:text-gray-200">${opp.target_audience}</span>
        </div>
        <div>
          <span class="text-gray-400 font-semibold block mb-0.5">Monetization Model:</span>
          <span class="text-gray-800 dark:text-gray-200">${opp.revenue_model}</span>
        </div>
        <div>
          <span class="text-gray-400 font-semibold block mb-0.5">Defensive Moat:</span>
          <span class="text-gray-800 dark:text-gray-200">${opp.competitive_advantage}</span>
        </div>
      </div>
    </div>
  `).join("");
}

// Open Opportunity Deep-Dive Modal
window.openOppDeepDive = function(idx) {
  if (!currentReport || !currentReport.opportunities[idx]) return;
  const opp = currentReport.opportunities[idx];

  document.getElementById("modalOppTitle").textContent = opp.name;
  document.getElementById("modalOppScore").textContent = opp.overall_score;
  document.getElementById("modalConfidence").textContent = opp.confidence_level;

  const dimsList = document.getElementById("modalDimensionsList");
  dimsList.innerHTML = opp.dimensions.map(dim => `
    <div class="p-4 rounded-xl bg-gray-50 dark:bg-darkbg-700 border border-gray-200 dark:border-darkbg-600 space-y-1.5">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold text-gray-900 dark:text-white">${dim.name} (${(dim.weight*100).toFixed(0)}% Weight)</span>
        <span class="text-xs font-mono font-bold text-indigo-500">${dim.score} / 100</span>
      </div>
      <div class="w-full h-1.5 bg-gray-200 dark:bg-darkbg-800 rounded-full overflow-hidden">
        <div class="h-full bg-indigo-500 rounded-full" style="width: ${dim.score}%"></div>
      </div>
      <p class="text-xs text-gray-600 dark:text-gray-300 pt-1">${dim.evidence}</p>
      <span class="text-[11px] text-gray-400 block italic">Assumption: ${dim.assumptions}</span>
    </div>
  `).join("");

  document.getElementById("oppModal").classList.remove("hidden");
  if (window.lucide) window.lucide.createIcons();
};

// Render Customer Intelligence
function renderCustomerIntelligence(cust) {
  const segContainer = document.getElementById("customerSegmentsContainer");
  segContainer.innerHTML = cust.customer_segments.map(seg => `
    <div class="bg-white dark:bg-darkbg-800 p-5 rounded-2xl border border-gray-200 dark:border-darkbg-700 space-y-3">
      <div class="flex items-center justify-between">
        <h4 class="text-sm font-bold text-gray-900 dark:text-white">${seg.name}</h4>
        <span class="text-[11px] px-2 py-0.5 rounded font-mono bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 font-semibold">${seg.share_of_market}</span>
      </div>
      <div>
        <span class="text-xs font-semibold text-gray-400 block mb-0.5">Purchasing Power</span>
        <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400">${seg.purchasing_power}</span>
      </div>
      <div>
        <span class="text-xs font-semibold text-gray-400 block mb-1">Key Pain Points</span>
        <ul class="space-y-1 text-xs text-gray-600 dark:text-gray-300">
          ${seg.pain_points.map(p => `<li>• ${p}</li>`).join("")}
        </ul>
      </div>
    </div>
  `).join("");

  const personaContainer = document.getElementById("buyerPersonasContainer");
  personaContainer.innerHTML = cust.buyer_personas.map(p => `
    <div class="bg-white dark:bg-darkbg-800 p-5 rounded-2xl border border-gray-200 dark:border-darkbg-700 space-y-2.5">
      <div class="flex items-center justify-between">
        <h4 class="text-sm font-bold text-gray-900 dark:text-white">${p.title}</h4>
        <span class="text-[10px] uppercase font-bold text-indigo-500">${p.decision_authority}</span>
      </div>
      <p class="text-xs text-gray-400">${p.demographics}</p>
      <div class="pt-2 border-t border-gray-100 dark:border-darkbg-700 text-xs space-y-1">
        <p><strong class="text-gray-400">Primary KPI:</strong> <span class="text-gray-800 dark:text-gray-200">${p.primary_kpi}</span></p>
        <p><strong class="text-gray-400">Core Pain:</strong> <span class="text-gray-800 dark:text-gray-200">${p.core_pain}</span></p>
        <p><strong class="text-gray-400">Major Objection:</strong> <span class="text-rose-500">${p.major_objection}</span></p>
      </div>
    </div>
  `).join("");
}

// Render Prospects Table
function renderProspectsTable(prospects) {
  const tbody = document.getElementById("prospectsTableBody");
  tbody.innerHTML = prospects.map(p => `
    <tr class="hover:bg-gray-50 dark:hover:bg-darkbg-700/40 transition">
      <td class="px-5 py-4">
        <div class="font-bold text-gray-900 dark:text-white text-xs">${p.company_name}</div>
        <a href="${p.website}" target="_blank" rel="noopener noreferrer" class="text-indigo-500 hover:underline text-[11px] flex items-center space-x-1 mt-0.5">
          <span>${p.website.replace('https://', '').replace('www.', '')}</span>
          <i data-lucide="external-link" class="w-3 h-3"></i>
        </a>
      </td>
      <td class="px-5 py-4">
        <span class="text-gray-800 dark:text-gray-200 block">${p.location}</span>
        <span class="text-gray-400 text-[11px]">${p.industry}</span>
      </td>
      <td class="px-5 py-4">
        <div class="flex items-center space-x-2">
          <span class="font-bold text-indigo-600 dark:text-indigo-400 font-mono">${p.fit_score}</span>
          <div class="w-12 h-1.5 bg-gray-200 dark:bg-darkbg-600 rounded-full overflow-hidden">
            <div class="h-full bg-indigo-500 rounded-full" style="width: ${p.fit_score}%"></div>
          </div>
        </div>
      </td>
      <td class="px-5 py-4 text-gray-700 dark:text-gray-300 max-w-xs">
        ${p.public_buying_signals}
      </td>
      <td class="px-5 py-4 text-gray-700 dark:text-gray-300 max-w-xs">
        <span class="p-1 rounded bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-300 font-medium block">
          ${p.recommended_outreach}
        </span>
      </td>
    </tr>
  `).join("");
}

// Render Competitors
function renderCompetitors(comp) {
  const container = document.getElementById("competitorsContainer");
  container.innerHTML = comp.competitors.map(c => `
    <div class="bg-white dark:bg-darkbg-800 p-5 rounded-2xl border border-gray-200 dark:border-darkbg-700 space-y-3">
      <div class="flex items-center justify-between">
        <div>
          <h4 class="text-sm font-bold text-gray-900 dark:text-white">${c.name}</h4>
          <span class="text-xs text-gray-400">${c.positioning}</span>
        </div>
        <a href="${c.website}" target="_blank" rel="noopener noreferrer" class="text-indigo-500 hover:text-indigo-400">
          <i data-lucide="external-link" class="w-4 h-4"></i>
        </a>
      </div>
      <div class="text-xs space-y-1.5 pt-2 border-t border-gray-100 dark:border-darkbg-700">
        <p><strong class="text-gray-400">Pricing Model:</strong> <span class="font-mono text-emerald-500">${c.pricing}</span></p>
        <p><strong class="text-gray-400">Strengths:</strong> <span class="text-gray-700 dark:text-gray-300">${c.strengths}</span></p>
        <p><strong class="text-gray-400">Weaknesses:</strong> <span class="text-rose-500">${c.weaknesses}</span></p>
        <p><strong class="text-indigo-500">Market White Space Gap:</strong> <span class="text-indigo-600 dark:text-indigo-300 font-medium">${c.market_gap}</span></p>
      </div>
    </div>
  `).join("");

  const wsList = document.getElementById("whiteSpaceList");
  wsList.innerHTML = comp.white_space_opportunities.map(w => `
    <li class="flex items-start space-x-2">
      <span class="text-indigo-500 font-bold">✓</span>
      <span>${w}</span>
    </li>
  `).join("");
}

// Render Marketing Strategy
function renderMarketingStrategy(mkt) {
  document.getElementById("mktPositioningText").textContent = mkt.positioning_statement;

  const channelsContainer = document.getElementById("marketingChannelsContainer");
  channelsContainer.innerHTML = mkt.recommended_channels.map(ch => `
    <div class="p-4 rounded-xl bg-white dark:bg-darkbg-800 border border-gray-200 dark:border-darkbg-700 space-y-1.5">
      <div class="flex items-center justify-between">
        <h4 class="text-xs font-bold text-gray-900 dark:text-white">${ch.channel}</h4>
        <span class="text-[10px] px-2 py-0.5 rounded bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 font-semibold">${ch.priority}</span>
      </div>
      <p class="text-xs text-gray-600 dark:text-gray-300">${ch.rationale}</p>
    </div>
  `).join("");

  const kwBody = document.getElementById("keywordsTableBody");
  kwBody.innerHTML = mkt.high_intent_keywords.map(k => `
    <tr>
      <td class="px-4 py-2.5 font-mono text-gray-800 dark:text-gray-200">${k.keyword}</td>
      <td class="px-4 py-2.5 text-gray-600 dark:text-gray-400">${k.intent}</td>
      <td class="px-4 py-2.5 text-gray-600 dark:text-gray-400">${k.volume}</td>
      <td class="px-4 py-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300">${k.priority}</span></td>
    </tr>
  `).join("");

  // Funnel & Campaign
  document.getElementById("funnelTofuText").textContent = mkt.acquisition_funnel.tofu;
  document.getElementById("funnelMofuText").textContent = mkt.acquisition_funnel.mofu;
  document.getElementById("funnelBofuText").textContent = mkt.acquisition_funnel.bofu;

  document.getElementById("campaignNameText").textContent = mkt.flagship_campaign.name;
  document.getElementById("campaignMessageText").textContent = mkt.flagship_campaign.core_message;
  document.getElementById("campaignHookText").textContent = `"${mkt.flagship_campaign.hook}"`;
}

// Render Action Plan
function renderActionPlan(strat) {
  document.getElementById("marketEntryWedgeText").textContent = strat.market_entry_strategy;

  const plan = strat.strategic_action_plan;
  document.getElementById("phase7List").innerHTML = plan.first_7_days.map(s => `
    <li class="p-2 rounded bg-gray-50 dark:bg-darkbg-700/60 border border-gray-200 dark:border-darkbg-600">
      <span class="font-medium text-gray-900 dark:text-white block mb-0.5">${s.task}</span>
      <span class="text-[10px] text-indigo-500 font-mono">KPI: ${s.kpi}</span>
    </li>
  `).join("");

  document.getElementById("phase30List").innerHTML = plan.first_30_days.map(s => `
    <li class="p-2 rounded bg-gray-50 dark:bg-darkbg-700/60 border border-gray-200 dark:border-darkbg-600">
      <span class="font-medium text-gray-900 dark:text-white block mb-0.5">${s.task}</span>
      <span class="text-[10px] text-purple-500 font-mono">KPI: ${s.kpi}</span>
    </li>
  `).join("");

  document.getElementById("phase60List").innerHTML = plan.first_60_days.map(s => `
    <li class="p-2 rounded bg-gray-50 dark:bg-darkbg-700/60 border border-gray-200 dark:border-darkbg-600">
      <span class="font-medium text-gray-900 dark:text-white block mb-0.5">${s.task}</span>
      <span class="text-[10px] text-emerald-500 font-mono">KPI: ${s.kpi}</span>
    </li>
  `).join("");

  document.getElementById("phase90List").innerHTML = plan.first_90_days.map(s => `
    <li class="p-2 rounded bg-gray-50 dark:bg-darkbg-700/60 border border-gray-200 dark:border-darkbg-600">
      <span class="font-medium text-gray-900 dark:text-white block mb-0.5">${s.task}</span>
      <span class="text-[10px] text-amber-500 font-mono">KPI: ${s.kpi}</span>
    </li>
  `).join("");

  // Pricing Tiers
  const pricingContainer = document.getElementById("pricingTiersContainer");
  pricingContainer.innerHTML = strat.recommended_pricing.map(tier => `
    <div class="p-5 rounded-2xl bg-gray-50 dark:bg-darkbg-700/50 border border-gray-200 dark:border-darkbg-600 space-y-2">
      <div class="flex items-center justify-between">
        <h4 class="text-sm font-bold text-gray-900 dark:text-white">${tier.tier}</h4>
        <span class="text-xs font-mono font-bold text-indigo-500">${tier.price}</span>
      </div>
      <p class="text-xs text-gray-400">${tier.target}</p>
      <p class="text-xs text-gray-600 dark:text-gray-300 pt-2 border-t border-gray-200 dark:border-darkbg-600">${tier.features}</p>
    </div>
  `).join("");
}

// Render Telemetry
function renderTelemetry(tm, rm) {
  document.getElementById("telemetryTotalTokens").textContent = tm.total_tokens.toLocaleString();
  document.getElementById("tokenSplitText").textContent = `Input: ${tm.total_input_tokens.toLocaleString()} | Output: ${tm.total_output_tokens.toLocaleString()}`;
  document.getElementById("telemetrySavedTokens").textContent = rm.total_token_weight_saved.toLocaleString();
  document.getElementById("telemetryEfficiencyPct").textContent = `${rm.efficiency_percentage}% efficiency reduction`;
  document.getElementById("telemetryCostUsd").textContent = `$${tm.estimated_total_cost_usd.toFixed(5)}`;
  document.getElementById("telemetrySkillsCount").textContent = `${rm.selected_count} / ${rm.total_skills_available}`;

  const usageBody = document.getElementById("agentUsageTableBody");
  usageBody.innerHTML = tm.agent_breakdown.map(a => `
    <tr>
      <td class="px-4 py-2.5 font-bold text-gray-800 dark:text-gray-200">${a.agent_name}</td>
      <td class="px-4 py-2.5 text-gray-500">${a.task_name}</td>
      <td class="px-4 py-2.5 font-mono text-gray-600 dark:text-gray-400">${a.input_tokens.toLocaleString()}</td>
      <td class="px-4 py-2.5 font-mono text-gray-600 dark:text-gray-400">${a.output_tokens.toLocaleString()}</td>
      <td class="px-4 py-2.5 font-mono font-semibold text-indigo-500">${a.total_tokens.toLocaleString()}</td>
      <td class="px-4 py-2.5 font-mono text-emerald-500">$${a.estimated_cost_usd.toFixed(5)}</td>
    </tr>
  `).join("");
}

// Render Industry Comparison
function renderComparisonView(cmp) {
  const container = document.getElementById("reportContainer");
  container.innerHTML = `
    <div class="bg-white dark:bg-darkbg-800 rounded-2xl p-6 border border-gray-200 dark:border-darkbg-700 shadow-sm space-y-6">
      <div class="flex items-center justify-between border-b border-gray-200 dark:border-darkbg-700 pb-4">
        <div>
          <span class="text-xs font-bold text-indigo-500 uppercase tracking-wider">STRATIFY Comparative Intelligence</span>
          <h2 class="text-2xl font-black text-gray-900 dark:text-white">${cmp.industry_1_name} vs ${cmp.industry_2_name}</h2>
          <span class="text-xs text-gray-400">Geographic Focus: ${cmp.location}</span>
        </div>
        <div class="text-right">
          <span class="text-xs font-semibold text-emerald-500 uppercase tracking-wider block">Strategic Advantage</span>
          <p class="text-sm font-bold text-gray-800 dark:text-gray-200 max-w-sm">${cmp.winner_summary}</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Industry 1 Card -->
        <div class="p-5 rounded-2xl bg-gray-50 dark:bg-darkbg-700/60 border border-gray-200 dark:border-darkbg-600 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-bold text-gray-900 dark:text-white">${cmp.industry_1.name}</h3>
            <span class="text-2xl font-black text-indigo-500">${cmp.industry_1.top_opportunity_score} <span class="text-xs text-gray-400">/ 100</span></span>
          </div>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Market TAM:</strong> ${cmp.industry_1.tam}</p>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Growth Rate:</strong> ${cmp.industry_1.cagr}</p>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Top Opportunity:</strong> ${cmp.industry_1.top_opportunity_name}</p>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Verified Prospects:</strong> ${cmp.industry_1.prospects_count} target accounts</p>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Competitors Analyzed:</strong> ${cmp.industry_1.competitors_count}</p>
          <button class="w-full mt-2 py-2 bg-indigo-600 text-white rounded-lg text-xs font-semibold" onclick="loadReportById('${cmp.industry_1.report_id}')">
            View Full ${cmp.industry_1.name} Report
          </button>
        </div>

        <!-- Industry 2 Card -->
        <div class="p-5 rounded-2xl bg-gray-50 dark:bg-darkbg-700/60 border border-gray-200 dark:border-darkbg-600 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-bold text-gray-900 dark:text-white">${cmp.industry_2.name}</h3>
            <span class="text-2xl font-black text-indigo-500">${cmp.industry_2.top_opportunity_score} <span class="text-xs text-gray-400">/ 100</span></span>
          </div>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Market TAM:</strong> ${cmp.industry_2.tam}</p>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Growth Rate:</strong> ${cmp.industry_2.cagr}</p>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Top Opportunity:</strong> ${cmp.industry_2.top_opportunity_name}</p>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Verified Prospects:</strong> ${cmp.industry_2.prospects_count} target accounts</p>
          <p class="text-xs text-gray-600 dark:text-gray-300"><strong class="text-gray-400">Competitors Analyzed:</strong> ${cmp.industry_2.competitors_count}</p>
          <button class="w-full mt-2 py-2 bg-indigo-600 text-white rounded-lg text-xs font-semibold" onclick="loadReportById('${cmp.industry_2.report_id}')">
            View Full ${cmp.industry_2.name} Report
          </button>
        </div>
      </div>
    </div>
  `;
}

// History List Loader
async function loadHistoryList() {
  const container = document.getElementById("historyListContainer");
  container.innerHTML = `<p class="text-xs text-gray-400">Loading previous sessions...</p>`;
  try {
    const res = await fetch("/api/stratify/history");
    const data = await res.json();
    if (!data.reports || data.reports.length === 0) {
      container.innerHTML = `<p class="text-xs text-gray-400">No saved research reports found.</p>`;
      return;
    }

    container.innerHTML = data.reports.map(r => `
      <div class="p-3 rounded-xl bg-gray-50 dark:bg-darkbg-700 border border-gray-200 dark:border-darkbg-600 flex items-center justify-between hover:border-indigo-400 transition cursor-pointer" onclick="loadReportById('${r.id}')">
        <div>
          <span class="text-xs font-bold text-gray-900 dark:text-white block">${r.industry} (${r.location})</span>
          <span class="text-[11px] text-gray-400 font-mono">${r.command}</span>
        </div>
        <div class="text-right">
          <span class="text-xs font-bold text-indigo-500">${r.top_opportunity_score || '--'}/100</span>
          <span class="text-[10px] text-gray-400 block">${r.depth}</span>
        </div>
      </div>
    `).join("");
  } catch (e) {
    container.innerHTML = `<p class="text-xs text-rose-500">Failed to load history.</p>`;
  }
}

window.loadReportById = async function(reportId) {
  document.getElementById("historyModal").classList.add("hidden");
  try {
    const res = await fetch(`/api/stratify/report/${reportId}`);
    const data = await res.json();
    if (data.report) {
      currentReport = data.report;
      // Re-inject main template if we were in comparison mode
      if (!document.getElementById("tamValue")) {
        window.location.reload();
      } else {
        renderDashboardReport(currentReport);
      }
    }
  } catch (e) {
    console.error("Error loading report:", e);
  }
};
