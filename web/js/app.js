/**
 * KUTSAL EŞİK - DİJİTAL BEŞERİ BİLİMLER PORTALI
 * Uygulama Mantığı ve Etkileşimler
 */

(function () {
  "use strict";

  const data = window.KUTSAL_ESIK_DATA || {
    quotes: [],
    concepts: [],
    timeline: [],
    traditions: [],
    bibliography: [],
    docs: {}
  };

  // State
  let currentQuoteIndex = 0;
  let currentDocKey = Object.keys(data.docs)[0] || "";

  // DOM Elements
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const navBtns = document.querySelectorAll(".nav-btn");
  const tabContents = document.querySelectorAll(".tab-content");
  const searchInput = document.getElementById("searchInput");

  // Wisdom Card
  const wisdomText = document.getElementById("wisdomText");
  const wisdomAuthor = document.getElementById("wisdomAuthor");
  const wisdomSource = document.getElementById("wisdomSource");
  const nextQuoteBtn = document.getElementById("nextQuoteBtn");
  const copyQuoteBtn = document.getElementById("copyQuoteBtn");

  // Grids
  const conceptsGrid = document.getElementById("conceptsGrid");
  const timelineContainer = document.getElementById("timelineContainer");
  const traditionsGrid = document.getElementById("traditionsGrid");
  const bibGrid = document.getElementById("bibGrid");

  // Reader
  const docList = document.getElementById("docList");
  const readerArticleBody = document.getElementById("readerArticleBody");

  // Modal
  const conceptModal = document.getElementById("conceptModal");
  const modalCloseBtn = document.getElementById("modalCloseBtn");
  const modalBody = document.getElementById("modalBody");

  // Toast
  const toast = document.getElementById("toast");

  // 1. Tema Yönetimi
  function initTheme() {
    const saved = localStorage.getItem("kutsal_esik_theme") || "light";
    document.documentElement.setAttribute("data-theme", saved);
    updateThemeIcon(saved);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme") || "light";
    const next = current === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("kutsal_esik_theme", next);
    updateThemeIcon(next);
  }

  function updateThemeIcon(theme) {
    if (themeToggleBtn) {
      themeToggleBtn.innerHTML = theme === "dark" ? "☀️ Işık" : "🌙 Gece";
    }
  }

  // 2. Sekme Yönetimi
  function switchTab(tabId) {
    navBtns.forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-tab") === tabId);
    });
    tabContents.forEach((tc) => {
      tc.classList.toggle("active", tc.id === tabId);
    });
    window.scrollTo({ top: 380, behavior: "smooth" });
  }

  // 3. Bilgelik Pusulası (Alıntılar)
  function renderQuote(index) {
    if (!data.quotes.length) return;
    const q = data.quotes[index % data.quotes.length];
    if (wisdomText) wisdomText.textContent = q.text;
    if (wisdomAuthor) wisdomAuthor.textContent = q.author;
    if (wisdomSource) wisdomSource.textContent = `${q.source} • ${q.culture}`;
  }

  function nextQuote() {
    currentQuoteIndex = Math.floor(Math.random() * data.quotes.length);
    renderQuote(currentQuoteIndex);
  }

  function copyCurrentQuote() {
    const q = data.quotes[currentQuoteIndex % data.quotes.length];
    if (!q) return;
    const textToCopy = `"${q.text}"\n— ${q.author} (${q.source})`;
    navigator.clipboard.writeText(textToCopy).then(() => {
      showToast("Alıntı panoya kopyalandı!");
    });
  }

  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => {
      toast.classList.remove("show");
    }, 2500);
  }

  // 4. Kavramlar Render
  function renderConcepts(filterText = "") {
    if (!conceptsGrid) return;
    conceptsGrid.innerHTML = "";
    const filtered = data.concepts.filter((c) => {
      const match = `${c.name} ${c.definition} ${c.civilization}`.toLowerCase();
      return match.includes(filterText.toLowerCase());
    });

    if (!filtered.length) {
      conceptsGrid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 2rem;">Aramanızla eşleşen kavram bulunamadı.</p>`;
      return;
    }

    filtered.forEach((c) => {
      const card = document.createElement("div");
      card.className = "concept-card";
      card.innerHTML = `
        <div class="concept-header">
          <h4 class="concept-title">${c.name}</h4>
          <span class="concept-badge">${c.civilization}</span>
        </div>
        <p class="concept-def">${c.definition}</p>
        <div class="concept-footer">
          <span>${c.era || "Kadim Çağ"}</span>
          <span style="color: var(--accent); font-weight: 600;">Detayları Gör →</span>
        </div>
      `;
      card.addEventListener("click", () => openConceptModal(c));
      conceptsGrid.appendChild(card);
    });
  }

  function openConceptModal(c) {
    if (!conceptModal || !modalBody) return;
    modalBody.innerHTML = `
      <div style="margin-bottom: 1rem;">
        <span class="concept-badge" style="margin-bottom: 0.5rem; display: inline-block;">${c.civilization}</span>
        <h2 style="font-size: 2rem; color: var(--accent);">${c.name}</h2>
        ${c.pronunciation ? `<p style="font-style: italic; color: var(--text-muted);">Okunuş: [${c.pronunciation}]</p>` : ""}
      </div>
      <p style="font-size: 1.05rem; line-height: 1.7; margin-bottom: 1.5rem;">${c.definition}</p>
      <h4 style="margin-bottom: 0.5rem; font-size: 1.1rem;">Temel İlkeler:</h4>
      <ul style="padding-left: 1.25rem; margin-bottom: 1.5rem; line-height: 1.6;">
        ${(c.core_principles || []).map((p) => `<li>${p}</li>`).join("")}
      </ul>
      <h4 style="margin-bottom: 0.5rem; font-size: 1.1rem;">Önemli Kaynaklar:</h4>
      <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
        ${(c.key_sources || []).map((s) => `<span class="symbol-tag">${s}</span>`).join("")}
      </div>
    `;
    conceptModal.classList.add("active");
  }

  // 5. Zaman Çizelgesi Render
  function renderTimeline(filterText = "") {
    if (!timelineContainer) return;
    timelineContainer.innerHTML = "";
    const filtered = data.timeline.filter((t) => {
      const match = `${t.year} ${t.title} ${t.region} ${t.description}`.toLowerCase();
      return match.includes(filterText.toLowerCase());
    });

    filtered.forEach((t) => {
      const item = document.createElement("div");
      item.className = "timeline-item";
      item.innerHTML = `
        <div class="timeline-content">
          <span class="timeline-year">${t.year} • ${t.period}</span>
          <h4 class="timeline-title">${t.title}</h4>
          <p class="timeline-desc">${t.description}</p>
          <div class="timeline-tags">
            <strong>Bölge:</strong> ${t.region} | <strong>Kavram:</strong> ${t.concept}
          </div>
        </div>
      `;
      timelineContainer.appendChild(item);
    });
  }

  // 6. Medeniyetler Atlası Render
  function renderTraditions() {
    if (!traditionsGrid) return;
    traditionsGrid.innerHTML = "";
    data.traditions.forEach((tr) => {
      const card = document.createElement("div");
      card.className = "tradition-card";
      card.innerHTML = `
        <h4 style="font-size: 1.5rem; color: var(--text-primary);">${tr.name}</h4>
        <p style="color: var(--accent); font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">${tr.region}</p>
        <div class="tradition-symbols">
          ${(tr.symbols || []).map((s) => `<span class="symbol-tag">${s}</span>`).join("")}
        </div>
        <p style="font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 1rem;">${tr.summary}</p>
        <blockquote class="tradition-proverb">“${tr.famous_saying}”</blockquote>
        <h5 style="margin: 0.75rem 0 0.4rem; font-size: 0.95rem;">Ayin ve Ritüeller:</h5>
        <ul style="padding-left: 1.2rem; font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5;">
          ${(tr.rituals || []).map((r) => `<li>${r}</li>`).join("")}
        </ul>
      `;
      traditionsGrid.appendChild(card);
    });
  }

  // 7. Okuma Odası (Monografiler)
  function initReader() {
    if (!docList) return;
    docList.innerHTML = "";
    const titles = {
      "01_antik_cag_ve_mitoloji": "1. Antik Çağ & Mitolojide Xenia",
      "02_dogu_ve_asya_felsefeleri": "2. Doğu Felsefesi, Ren & Omotenashi",
      "03_ibrahimi_ve_anadolu_irfani": "3. İbrahimi İnançlar & Ahilik",
      "04_antropoloji_ve_bedevi_kulturu": "4. Antropoloji & Bozkır Dehaleti",
      "05_modern_felsefe_ve_etik": "5. Kant, Levinas & Derrida",
      "06_dijital_cag_ve_yeni_esikler": "6. Dijital Çağ & Siber Müşterekler"
    };

    const docKeys = Object.keys(data.docs);
    docKeys.forEach((key, index) => {
      const li = document.createElement("li");
      li.className = `doc-item ${key === currentDocKey ? "active" : ""}`;
      li.textContent = titles[key] || key;
      li.addEventListener("click", () => {
        document.querySelectorAll(".doc-item").forEach((el) => el.classList.remove("active"));
        li.classList.add("active");
        currentDocKey = key;
        renderArticle(key);
      });
      docList.appendChild(li);
    });

    if (docKeys.length > 0) {
      renderArticle(docKeys[0]);
    }
  }

  // Hafif Markdown -> HTML Çevirici
  function parseMarkdown(md) {
    if (!md) return "";
    let html = md
      // Escape
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      // Headers
      .replace(/^### (.*$)/gim, "<h3>$1</h3>")
      .replace(/^## (.*$)/gim, "<h2>$1</h2>")
      .replace(/^# (.*$)/gim, "<h1>$1</h1>")
      // Blockquote
      .replace(/^\> (.*$)/gim, "<blockquote>$1</blockquote>")
      // Bold & Italic
      .replace(/\*\*\*(.*?)\*\*\*/gim, "<strong><em>$1</em></strong>")
      .replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/gim, "<em>$1</em>")
      // Unordered List
      .replace(/^\* (.*$)/gim, "<li>$1</li>")
      .replace(/^- (.*$)/gim, "<li>$1</li>")
      // Code blocks
      .replace(/`([^`]+)`/gim, "<code>$1</code>")
      // Horizontal rule
      .replace(/^---$/gim, "<hr style='border: none; border-top: 1px solid var(--border-subtle); margin: 2rem 0;' />")
      // Paragraphs
      .replace(/\n\n/gim, "</p><p>");

    return `<p>${html}</p>`;
  }

  function renderArticle(docKey) {
    if (!readerArticleBody) return;
    const rawMarkdown = data.docs[docKey] || "";
    readerArticleBody.innerHTML = parseMarkdown(rawMarkdown);
  }

  // 8. Kaynakça Render
  function renderBibliography() {
    if (!bibGrid) return;
    bibGrid.innerHTML = "";
    data.bibliography.forEach((b) => {
      const card = document.createElement("div");
      card.className = "concept-card";
      card.innerHTML = `
        <div class="concept-header">
          <h4 class="concept-title" style="font-size: 1.25rem;">${b.title}</h4>
          <span class="concept-badge">${b.year}</span>
        </div>
        <p style="font-weight: 600; color: var(--accent); margin-bottom: 0.4rem;">${b.author}</p>
        <p class="concept-def" style="margin-bottom: 0.8rem;">${b.summary}</p>
        <div class="concept-footer">
          <span>${b.category}</span>
          <span>${b.publisher || ""}</span>
        </div>
      `;
      bibGrid.appendChild(card);
    });
  }

  // 9. Canlı Arama
  function handleSearch(e) {
    const query = e.target.value.trim().toLowerCase();
    renderConcepts(query);
    renderTimeline(query);
  }

  // Event Listeners
  function initEvents() {
    if (themeToggleBtn) {
      themeToggleBtn.addEventListener("click", toggleTheme);
    }

    navBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const tabId = btn.getAttribute("data-tab");
        switchTab(tabId);
      });
    });

    if (nextQuoteBtn) {
      nextQuoteBtn.addEventListener("click", nextQuote);
    }

    if (copyQuoteBtn) {
      copyQuoteBtn.addEventListener("click", copyCurrentQuote);
    }

    if (searchInput) {
      searchInput.addEventListener("input", handleSearch);
    }

    if (modalCloseBtn) {
      modalCloseBtn.addEventListener("click", () => {
        conceptModal.classList.remove("active");
      });
    }

    if (conceptModal) {
      conceptModal.addEventListener("click", (e) => {
        if (e.target === conceptModal) {
          conceptModal.classList.remove("active");
        }
      });
    }

    const exportBibtexBtn = document.getElementById("exportBibtexBtn");
    if (exportBibtexBtn) {
      exportBibtexBtn.addEventListener("click", () => {
        let bibtex = "";
        data.bibliography.forEach((item) => {
          bibtex += `@book{${item.id},\n  author = {${item.author}},\n  title = {${item.title}},\n  year = {${item.year}},\n  publisher = {${item.publisher || ""}}\n}\n\n`;
        });
        navigator.clipboard.writeText(bibtex).then(() => {
          showToast("BibTeX kaynakçası panoya kopyalandı!");
        });
      });
    }
  }

  // Başlatma
  function init() {
    initTheme();
    renderQuote(0);
    renderConcepts();
    renderTimeline();
    renderTraditions();
    initReader();
    renderBibliography();
    initEvents();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
