/* ============================================================
   Posts page: search, year/tag filters, pagination
   Reads from posts.json, renders dynamically
   ============================================================ */

(function () {
  'use strict';

  const POSTS_PER_PAGE = 20;

  let allPosts = [];
  let filteredPosts = [];
  let currentPage = 1;
  let activeYear = null;
  let activeTags = new Set();
  let searchQuery = '';

  // --- DOM refs ---
  const archiveSection = document.getElementById('archive-section');
  const archiveList = document.getElementById('archive-list');
  const searchInput = document.getElementById('search-input');
  const yearFilters = document.getElementById('year-filters');
  const tagFilters = document.getElementById('tag-filters');
  const filterStatus = document.getElementById('filter-status');
  const emptyState = document.getElementById('empty-state');
  const loadMoreContainer = document.getElementById('load-more-container');
  const loadMoreBtn = document.getElementById('load-more-btn');
  const postsCount = document.getElementById('posts-count');

  // --- Init ---
  async function init() {
    try {
      const resp = await fetch('/posts/posts.json');
      if (!resp.ok) {
        // Try relative path for file:// serving
        const resp2 = await fetch('posts.json');
        allPosts = await resp2.json();
      } else {
        allPosts = await resp.json();
      }
    } catch (e) {
      try {
        const resp2 = await fetch('posts.json');
        allPosts = await resp2.json();
      } catch (e2) {
        console.error('Failed to load posts.json', e2);
        return;
      }
    }

    readUrlParams();
    buildYearFilters();
    buildTagFilters();
    applyFilters();
    bindEvents();
  }

  // --- URL Params ---
  function readUrlParams() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('year')) {
      activeYear = params.get('year');
    }
    if (params.get('tag')) {
      params.get('tag').split(',').forEach(t => activeTags.add(t.toLowerCase()));
    }
    if (params.get('q')) {
      searchQuery = params.get('q');
      if (searchInput) searchInput.value = searchQuery;
    }
  }

  function updateUrlParams() {
    const params = new URLSearchParams();
    if (activeYear) params.set('year', activeYear);
    if (activeTags.size) params.set('tag', [...activeTags].join(','));
    if (searchQuery) params.set('q', searchQuery);
    const qs = params.toString();
    const url = window.location.pathname + (qs ? '?' + qs : '');
    history.replaceState(null, '', url);
  }

  // --- Build Filters ---
  function buildYearFilters() {
    if (!yearFilters) return;
    const years = [...new Set(allPosts.map(p => p.date.slice(0, 4)))].sort().reverse();

    let html = '<button class="year-btn' + (!activeYear ? ' active' : '') + '" data-year="">ALL</button>';
    years.forEach(y => {
      html += '<button class="year-btn' + (activeYear === y ? ' active' : '') + '" data-year="' + y + '">' + y + '</button>';
    });
    yearFilters.innerHTML = html;
  }

  function buildTagFilters() {
    if (!tagFilters) return;
    // Count tag frequency
    const tagCounts = {};
    allPosts.forEach(p => {
      (p.tags || []).forEach(t => {
        const key = String(t).toLowerCase();
        tagCounts[key] = (tagCounts[key] || 0) + 1;
      });
    });
    // Top 15 tags
    const topTags = Object.entries(tagCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15)
      .map(([t]) => t);

    let html = '';
    topTags.forEach(t => {
      html += '<button class="tag-btn' + (activeTags.has(t) ? ' active' : '') + '" data-tag="' + t + '">' + t + '</button>';
    });
    tagFilters.innerHTML = html;
  }

  // --- Filter Logic ---
  function isFiltering() {
    return activeYear || activeTags.size > 0 || searchQuery.length > 0;
  }

  function applyFilters() {
    currentPage = 1;
    filteredPosts = allPosts.filter(p => {
      if (activeYear && !p.date.startsWith(activeYear)) return false;
      if (activeTags.size > 0) {
        const postTags = (p.tags || []).map(t => String(t).toLowerCase());
        for (const t of activeTags) {
          if (!postTags.includes(t)) return false;
        }
      }
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        const haystack = (p.title + ' ' + p.preview + ' ' + (p.tags || []).map(String).join(' ')).toLowerCase();
        if (!haystack.includes(q)) return false;
      }
      return true;
    });

    updateUrlParams();
    render();
  }

  // --- Render ---
  function render() {
    const filtering = isFiltering();

    if (archiveSection) archiveSection.style.display = '';

    // Filter status
    if (filterStatus) {
      if (filtering) {
        const parts = [];
        if (activeYear) parts.push('YEAR:' + activeYear);
        if (activeTags.size) parts.push('TAGS:' + [...activeTags].join('+'));
        if (searchQuery) parts.push('SEARCH:"' + searchQuery + '"');
        filterStatus.textContent = 'FILTERED_BY: { ' + parts.join(' , ') + ' }  //  ' + filteredPosts.length + ' results';
        filterStatus.classList.add('visible');
      } else {
        filterStatus.classList.remove('visible');
      }
    }

    // Update count
    if (postsCount) {
      postsCount.textContent = filteredPosts.length + ' posts';
    }

    // Empty state
    if (emptyState) {
      emptyState.classList.toggle('visible', filteredPosts.length === 0 && filtering);
    }

    renderArchive();
  }

  function renderArchive() {
    if (!archiveList) return;

    const postsToShow = filteredPosts.slice(0, currentPage * POSTS_PER_PAGE);
    let html = '';
    postsToShow.forEach(p => {
      html += renderListCard(p);
    });

    archiveList.innerHTML = html;

    // Observe new elements for scroll reveal
    observeNewElements(archiveList);

    // Load more button
    if (loadMoreContainer) {
      if (postsToShow.length < filteredPosts.length) {
        loadMoreContainer.style.display = '';
      } else {
        loadMoreContainer.style.display = 'none';
      }
    }
  }

  function renderListCard(post) {
    const tags = (post.tags || [])
      .map(t => '<span class="tag">' + escapeHtml(t) + '</span>')
      .join('');

    var thumb = '';
    if (post.media) {
      var thumbSrc = '../posts/' + post.year + '/' + post.month + '/' + post.slug + '/media/' + post.media;
      thumb = '<div class="list-card-image"><img src="' + thumbSrc + '" alt="" loading="lazy"></div>';
    }

    return '<a href="' + post.url + '" class="list-card">' +
      '<div class="list-card-body">' +
      '<div class="list-card-title">' + escapeHtml(post.title) + '</div>' +
      '<div class="list-card-preview">' + escapeHtml(post.preview) + '</div>' +
      '<div class="card-footer"><div class="card-tags">' + tags + '</div>' +
      '<div class="card-meta"><span class="card-date">' + post.date + '</span>' +
      '<span class="card-reading-time">' + (post.reading_time || '') + '</span></div></div>' +
      '</div>' +
      thumb +
      '</a>';
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // --- Events ---
  function bindEvents() {
    // Search
    if (searchInput) {
      let timeout;
      searchInput.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
          searchQuery = searchInput.value.trim();
          applyFilters();
        }, 250);
      });
    }

    // Year filters
    if (yearFilters) {
      yearFilters.addEventListener('click', (e) => {
        const btn = e.target.closest('.year-btn');
        if (!btn) return;
        activeYear = btn.dataset.year || null;
        yearFilters.querySelectorAll('.year-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        applyFilters();
      });
    }

    // Tag filters
    if (tagFilters) {
      tagFilters.addEventListener('click', (e) => {
        const btn = e.target.closest('.tag-btn');
        if (!btn) return;
        const tag = btn.dataset.tag;
        if (activeTags.has(tag)) {
          activeTags.delete(tag);
          btn.classList.remove('active');
        } else {
          activeTags.add(tag);
          btn.classList.add('active');
        }
        applyFilters();
      });
    }

    // Load more
    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', () => {
        loadMoreBtn.classList.add('loading');
        loadMoreBtn.textContent = 'Loading...';
        // Small delay for visual feedback
        setTimeout(() => {
          currentPage++;
          renderArchive();
          loadMoreBtn.classList.remove('loading');
          loadMoreBtn.textContent = 'Load more';
        }, 150);
      });
    }
  }

  // --- Start ---
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();


/* ============================================================
   Global: scroll reveal, scroll-to-top, nav shadow
   Runs on all pages
   ============================================================ */

(function () {
  'use strict';

  // --- Intersection Observer for scroll reveal ---
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  // Observe all existing .reveal elements and cards/sections
  function initReveal() {
    // Add .reveal class to cards, featured cards, timeline nodes, etc.
    const selectors = [
      '.card',
      '.list-card',
      '.about-teaser',
      '.section',
      '.timeline-node',
      '.skill-row',
      '.speaking-cta',
      '.about-intro-row',
    ];
    document.querySelectorAll(selectors.join(',')).forEach(el => {
      if (!el.classList.contains('reveal')) {
        el.classList.add('reveal');
      }
    });

    document.querySelectorAll('.reveal').forEach(el => {
      revealObserver.observe(el);
    });
  }

  // Expose for dynamically added elements (posts.js archive rows)
  window.observeNewElements = function (container) {
    container.querySelectorAll('.reveal:not(.visible)').forEach(el => {
      revealObserver.observe(el);
    });
  };

  // --- Nav shadow on scroll ---
  const nav = document.querySelector('.nav');
  let lastScrollY = 0;

  function updateNav() {
    const y = window.scrollY;
    if (nav) {
      nav.classList.toggle('scrolled', y > 20);
    }
    lastScrollY = y;
  }

  // --- Reading progress bar ---
  const progressBar = document.getElementById('reading-progress');

  function updateProgress() {
    if (!progressBar) return;
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const pct = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
    progressBar.style.width = pct + '%';
  }

  // --- Scroll to top button ---
  const scrollTopBtn = document.getElementById('scroll-top');

  function updateScrollTop() {
    if (scrollTopBtn) {
      scrollTopBtn.classList.toggle('visible', window.scrollY > 400);
    }
  }

  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- Scroll handler (throttled via rAF) ---
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        updateNav();
        updateScrollTop();
        updateProgress();
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // --- Code block copy buttons ---
  function initCodeCopy() {
    document.querySelectorAll('.post-content pre, .article-content pre').forEach(pre => {
      if (pre.parentElement.classList.contains('code-block-wrapper')) return;
      const wrapper = document.createElement('div');
      wrapper.className = 'code-block-wrapper';
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);

      const btn = document.createElement('button');
      btn.className = 'code-copy-btn';
      btn.textContent = 'Copy';
      btn.addEventListener('click', () => {
        const code = pre.querySelector('code') || pre;
        navigator.clipboard.writeText(code.textContent).then(() => {
          btn.textContent = 'Copied!';
          setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
        });
      });
      wrapper.appendChild(btn);
    });
  }

  // --- Init ---
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initReveal();
      initCodeCopy();
      updateNav();
      updateScrollTop();
      updateProgress();
    });
  } else {
    initReveal();
    initCodeCopy();
    updateNav();
    updateScrollTop();
    updateProgress();
  }
})();
