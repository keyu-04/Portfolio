(function () {
  const params = new URLSearchParams(location.search);
  const next = params.get('next') || 'home.html';
  const fill = document.getElementById('fill');
  const status = document.getElementById('status');
  const bar = document.querySelector('.bar');

  // 可选：尽量避免“后退”回到 loading
  history.replaceState({from:'loading'}, '', location.href);
  window.addEventListener('pageshow', e => {
    if (e.persisted) location.replace(next);
  });

  // 方案 A：定时模拟进度（简单稳定）
  const DURATION = 2200; // ms
  const start = performance.now();

  // 可选：预取 Home 的关键资源（命中缓存后跳转更顺滑）
  const preloads = [
    '../assets/css/home.css',
    '../assets/css/base.css',
    '../home.html'
  ].map(u => fetch(u, {cache:'force-cache'}).catch(()=>{}));

  function tick(now){
    const t = Math.min(1, (now - start) / DURATION);
    const eased = 1 - Math.pow(1 - t, 3); // easeOutCubic
    const pct = Math.round(eased * 100);
    fill.style.width = pct + '%';
    bar.setAttribute('aria-valuenow', String(pct));
    status.textContent = pct < 100 ? `hacking the system ${pct}%` : 'successful，entering…';
    if (t < 1) requestAnimationFrame(tick);
    else Promise.allSettled(preloads).finally(()=> { location.replace(next); });
  }
  requestAnimationFrame(tick);

  // —— 进阶（可选）：真正按资源进度更新 —— 
  // 如果你后面想根据实际资源加载来驱动进度，可统计 fetch/图片等完成数量后更新 pct。
})();
