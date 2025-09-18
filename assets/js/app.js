// 元素
const nav = document.querySelector('.nav');
const items = [...document.querySelectorAll('.nav-item')];
const slider = document.querySelector('.slider');
const content = document.getElementById('content');

// 设置滑块到当前激活项
function placeSliderTo(el){
  const y = el.offsetTop + 2;
  slider.style.transform = `translateY(${y}px)`;
  slider.style.height = `${el.offsetHeight}px`;
}

// 初始定位
placeSliderTo(document.querySelector('.nav-item.is-active'));

// 加载右侧片段
async function loadFragment(url, push=true){
  try{
    const res = await fetch(url, {cache:'no-store'});
    if(!res.ok) throw new Error(res.statusText);
    const html = await res.text();
    content.classList.remove('fade-in');
    content.innerHTML = html;
    // 触发重绘以重放动画
    void content.offsetWidth;
    content.classList.add('fade-in');

    if(push) history.pushState({fragment:url}, '', `#${encodeURIComponent(url)}`);
    content.focus();
  }catch(err){
    content.innerHTML = `<h2>Erreur</h2><p>Impossible de charger: ${url}</p>`;
  }
}

// 切换激活项
function setActive(el){
  items.forEach(i => {
    const active = i === el;
    i.classList.toggle('is-active', active);
    i.setAttribute('aria-selected', active ? 'true' : 'false');
  });
  placeSliderTo(el);
  loadFragment(el.dataset.fragment, true);
}

// 点击导航
items.forEach(item => item.addEventListener('click', () => setActive(item)));

// 键盘导航（↑/↓/Enter/Space）
nav.addEventListener('keydown', (e) => {
  const idx = items.findIndex(i => i.classList.contains('is-active'));
  if(e.key === 'ArrowDown'){
    e.preventDefault();
    setActive(items[Math.min(idx+1, items.length-1)]);
  }else if(e.key === 'ArrowUp'){
    e.preventDefault();
    setActive(items[Math.max(idx-1, 0)]);
  }else if(e.key === 'Enter' || e.key === ' '){
    e.preventDefault();
    setActive(items[idx] || items[0]);
  }
});

// 历史记录（前进后退）
window.addEventListener('popstate', (e) => {
  const url = (e.state && e.state.fragment) ||
              (location.hash ? decodeURIComponent(location.hash.slice(1)) : null);
  if(!url) return;
  const target = items.find(i => i.dataset.fragment === url);
  if(target){
    items.forEach(i => i.classList.toggle('is-active', i === target));
    placeSliderTo(target);
    loadFragment(url, false);
  }
});

// 支持带 hash 直达某片段
(function initFromHash(){
  const url = location.hash ? decodeURIComponent(location.hash.slice(1)) : null;
  if(!url) return;
  const target = items.find(i => i.dataset.fragment === url);
  if(target) setActive(target);
})();
