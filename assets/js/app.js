// 基础获取
const nav = document.querySelector('.nav');
const slider = document.querySelector('.slider');
const content = document.getElementById('content');
const items = nav ? Array.from(nav.querySelectorAll('.nav-item')) : [];

if (!nav || !slider || !content || items.length === 0) {
  console.warn('[app] 导航初始化失败：缺少必需元素。');
  // 不再继续绑定，避免报错
} else {

  // ===== 工具函数 =====
  function placeSliderTo(el) {
    if (!el) return;
    const navRect = nav.getBoundingClientRect();
    const itemRect = el.getBoundingClientRect();
    const styles = getComputedStyle(nav);
    const borderLeft = parseFloat(styles.borderLeftWidth) || 0;
    const borderTop  = parseFloat(styles.borderTopWidth)  || 0;

    const x = itemRect.left - navRect.left + nav.scrollLeft - borderLeft;
    const y = itemRect.top  - navRect.top  + nav.scrollTop  - borderTop;

    slider.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    slider.style.width  = `${itemRect.width}px`;
    slider.style.height = `${itemRect.height}px`;
  }

  let currentIndex = -1;       // 默认不选中
  let currentFragment = null;  // 默认没有已加载片段
  let activeController = null; // 控制并发加载

  async function loadFragment(rawUrl, { push = true, anchor = null } = {}) {
    if (!rawUrl) return;
    const raw = String(rawUrl).trim();
    if (!raw) return;

    const [base, ...anchorParts] = raw.split('#');
    const fragment = base;
    const targetAnchor = anchor ?? (anchorParts.length > 0 ? anchorParts.join('#') : null);

    const pushStateIfNeeded = () => {
      if (!push || !fragment) return;
      const hashString = targetAnchor ? `${fragment}#${targetAnchor}` : fragment;
      const encodedHash = encodeURIComponent(hashString);
      const state = { fragment, anchor: targetAnchor };
      if (!history.state || history.state.fragment !== fragment || history.state.anchor !== targetAnchor) {
        history.pushState(state, '', `#${encodedHash}`);
      }
    };

    const scrollToAnchor = () => {
      if (!targetAnchor) return;
      const safeId = targetAnchor.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
      const el = content.querySelector(`[id="${safeId}"]`);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    if (!fragment) {
      pushStateIfNeeded();
      scrollToAnchor();
      return;
    }

    if (fragment === currentFragment) {
      pushStateIfNeeded();
      scrollToAnchor();
      return;
    }

    // 取消上一次尚未完成的加载
    if (activeController) activeController.abort();
    const controller = new AbortController();
    activeController = controller;

    try {
      const res = await fetch(fragment, { cache: 'no-store', signal: controller.signal });
      if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
      const html = await res.text();

      content.classList.remove('fade-in');
      content.innerHTML = html;
      void content.offsetWidth;         // 触发重绘以重放动画
      content.classList.add('fade-in');

      currentFragment = fragment;
      pushStateIfNeeded();
      scrollToAnchor();

      if (typeof content.focus === 'function') {
        try { content.focus({ preventScroll: true }); } catch { content.focus(); }
      }
    } catch (err) {
      if (err.name === 'AbortError') return; // 被取消的请求不提示
      content.innerHTML = `<h2>Erreur</h2><p>Impossible de charger: ${fragment}<br><small>${String(err)}</small></p>`;
      console.error('[app] Failed to load fragment:', err);
    } finally {
      if (activeController === controller) activeController = null;
    }
  }

  function setActive(target, { push = true, anchor = null } = {}) {
    if (!target) return;
    const nextIndex = items.indexOf(target);
    if (nextIndex === -1) return;

    const fragment = (target.dataset.fragment || '').trim();
    if (!fragment) return;

    // 第一次点击：让光标出现
    if (!slider.classList.contains('is-on')) slider.classList.add('is-on');

    // 位置先对齐再加载
    placeSliderTo(target);

    // 更新选中态
    items.forEach((item, idx) => {
      const active = idx === nextIndex;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    currentIndex = nextIndex;

    // 加载右侧内容
    return loadFragment(fragment, { push, anchor });
  }

  // 事件绑定
  nav.addEventListener('click', (ev) => {
    const target = ev.target.closest('.nav-item');
    if (!target || !nav.contains(target)) return;
    ev.preventDefault();
    setActive(target);
  });

  nav.addEventListener('keydown', (ev) => {
    if (ev.defaultPrevented) return;
    const maxIndex = items.length - 1;
    let nextIndex = currentIndex >= 0 ? currentIndex : 0;

    switch (ev.key) {
      case 'ArrowDown':
      case 'ArrowRight':
        ev.preventDefault();
        nextIndex = Math.min(nextIndex + 1, maxIndex);
        break;
      case 'ArrowUp':
      case 'ArrowLeft':
        ev.preventDefault();
        nextIndex = Math.max(nextIndex - 1, 0);
        break;
      case 'Enter':
      case ' ':
        ev.preventDefault();
        setActive(items[nextIndex] || items[0]);
        return;
      default:
        return;
    }
    if (items[nextIndex]) setActive(items[nextIndex]);
  });

  content.addEventListener('click', (ev) => {
    if (ev.defaultPrevented) return;
    if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
    const link = ev.target.closest('a[href]');
    if (!link || !content.contains(link)) return;
    if (link.target && link.target !== '_self') return;

    let href = link.getAttribute('href');
    if (!href) return;
    if (href.startsWith('#')) {
      href = href.slice(1);
    }
    if (!href.startsWith('fragments/')) return;

    ev.preventDefault();

    const [path, ...anchorParts] = href.split('#');
    const anchor = anchorParts.length > 0 ? anchorParts.join('#') : null;
    const target = items.find(i => (i.dataset.fragment || '').trim() === path);

    if (target) {
      setActive(target, { anchor });
    } else {
      loadFragment(path, { anchor });
    }
  });

  window.addEventListener('popstate', (ev) => {
    let raw = null;
    if (ev.state?.fragment) {
      raw = ev.state.anchor ? `${ev.state.fragment}#${ev.state.anchor}` : ev.state.fragment;
    } else if (location.hash) {
      raw = decodeURIComponent(location.hash.slice(1));
    }

    if (!raw) return;

    const [path, ...anchorParts] = raw.split('#');
    const anchor = anchorParts.length > 0 ? anchorParts.join('#') : null;
    const target = items.find(i => (i.dataset.fragment || '').trim() === path);

    if (target) {
      setActive(target, { push: false, anchor });
    } else {
      loadFragment(path, { push: false, anchor });
    }
  });

  const repositionActive = () => {
    const activeItem = (currentIndex >= 0 ? items[currentIndex] : null) || items.find(i => i.classList.contains('is-active'));
    if (activeItem) placeSliderTo(activeItem);
  };
  window.addEventListener('resize', () => requestAnimationFrame(repositionActive));
  nav.addEventListener('scroll', () => requestAnimationFrame(repositionActive));

  items.forEach(item => {
    item.addEventListener('pointerleave', () => {
      if (!item.classList.contains('is-active')) return;
      requestAnimationFrame(repositionActive);
    });
  });

  nav.addEventListener('transitionend', (ev) => {
    const item = ev.target.closest('.nav-item');
    if (!item || !item.classList.contains('is-active')) return;
    requestAnimationFrame(repositionActive);
  });

  // ===== 初始化：不默认选中；只有带 hash 才直接选中 =====
  items.forEach(i => i.setAttribute('aria-selected', 'false'));  // 全部未选

  const fromHash = location.hash ? decodeURIComponent(location.hash.slice(1)) : null;
  if (fromHash) {
    const [path, ...anchorParts] = fromHash.split('#');
    const anchor = anchorParts.length > 0 ? anchorParts.join('#') : null;
    const target = items.find(i => (i.dataset.fragment || '').trim() === path);
    if (target) {
      setActive(target, { push: false, anchor });
    } else if (path) {
      loadFragment(path, { push: false, anchor });
    } else if (anchor) {
      loadFragment(currentFragment || '', { push: false, anchor });
    }
  }
}


