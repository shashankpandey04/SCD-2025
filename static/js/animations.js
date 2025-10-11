(function(){
  // IntersectionObserver to reveal elements
  const revealEls = Array.from(document.querySelectorAll('.reveal'));
  const counters = Array.from(document.querySelectorAll('[data-count]'));
  const parallaxEls = Array.from(document.querySelectorAll('[data-parallax]'));

  const io = new IntersectionObserver((entries)=>{
    for(const e of entries){
      if(e.isIntersecting){
        e.target.classList.add('is-visible');
        // Start counters once when visible
        const target = e.target;
        if(target.hasAttribute('data-count-started')) continue;
        const num = target.querySelector('[data-count]');
        if(num){
          target.setAttribute('data-count-started','1');
          animateCount(num);
        }
      }
    }
  }, { threshold: 0.2});

  revealEls.forEach(el=> io.observe(el));
  counters.forEach(el=> io.observe(el.closest('[data-count-parent]') || el));

  function animateCount(el){
    const to = parseInt(el.getAttribute('data-count')||'0',10);
    const duration = parseInt(el.getAttribute('data-count-duration')||'1200',10);
    const start = performance.now();
    const from = 0;

    function step(now){
      const t = Math.min(1, (now-start)/duration);
      const eased = easeOutCubic(t);
      const val = Math.floor(from + (to-from)*eased);
      el.textContent = val.toLocaleString();
      if(t<1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function easeOutCubic(t){ return 1 - Math.pow(1 - t, 3); }

  // Simple parallax effect
  let lastY = window.scrollY;
  function onScroll(){
    const y = window.scrollY;
    const dy = y - lastY; // not used, but can help smooth
    parallaxEls.forEach(el=>{
      const depth = parseFloat(el.getAttribute('data-parallax')) || 0.2;
      const translate = y * depth;
      el.style.transform = `translateY(${translate}px)`;
    });
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();