(function(){
  const DPR = Math.min(2, window.devicePixelRatio || 1);
  const cfg = {
    countBase: 140,
    speed: 0.015,       // forward speed towards viewer (affects z)
    spread: 2.4,        // world spread multiplier
    depth: 2.2,         // max depth range
    size: 1.4,          // base size
    // Flow field + color cycle
    flowScale: 0.18,    // spatial frequency of flow field
    flowAmp: 0.006,     // XY drift per frame
    timeScale: 0.0006,  // flow time speed
    hueBase: 270,       // start hue (violet)
    hueSpeed: 0.015,    // cycles per second
    sat: 78,            // percent
    light: 68           // percent
  };

  // Simple value noise (smooth hash) for 2D
  function smoothstep(t){ return t*t*(3-2*t); }
  function hash(x, y){
    // deterministic pseudo-random [0,1)
    const s = Math.sin(x*127.1 + y*311.7) * 43758.5453;
    return s - Math.floor(s);
  }
  function noise2D(x, y){
    const xi = Math.floor(x), yi = Math.floor(y);
    const xf = x - xi, yf = y - yi;
    const u = smoothstep(xf), v = smoothstep(yf);
    const n00 = hash(xi, yi);
    const n10 = hash(xi+1, yi);
    const n01 = hash(xi, yi+1);
    const n11 = hash(xi+1, yi+1);
    const nx0 = n00 + u*(n10 - n00);
    const nx1 = n01 + u*(n11 - n01);
    return nx0 + v*(nx1 - nx0); // [0,1)
  }
  function hsl(h, s, l){ return `hsl(${h} ${s}% ${l}%)`; }

  function init(){
    const canvas = document.getElementById('hero-canvas');
    if(!canvas) return;
    const ctx = canvas.getContext('2d');

    let width = 0, height = 0, cx = 0, cy = 0;
    let stars = [];
    let pointer = { x: 0, y: 0, tx: 0, ty: 0 };
    let startTime = performance.now();

    function resize(){
      const rect = canvas.getBoundingClientRect();
      width = Math.floor(rect.width * DPR);
      height = Math.floor(rect.height * DPR);
      canvas.width = width;
      canvas.height = height;
      cx = width / 2; cy = height / 2;
      spawn();
    }

    function spawn(){
      const area = (width * height) / (1000*1000); // megapixels
      const count = Math.max(100, Math.floor(cfg.countBase * area));
      stars = new Array(count).fill(0).map(()=> newStar());
    }

    function newStar(){
      // Random position in 3D cube around origin
      const z = Math.random() * cfg.depth + 0.2; // depth [0.2, depth+)
      const x = (Math.random() * 2 - 1) * cfg.spread * z;
      const y = (Math.random() * 2 - 1) * cfg.spread * z;
      return { x, y, z };
    }

    function step(now){
      const t = (now - startTime) / 1000; // seconds
      // Lerp pointer influence
      pointer.x += (pointer.tx - pointer.x) * 0.06;
      pointer.y += (pointer.ty - pointer.y) * 0.06;

      // Motion trails for a glowy look
      ctx.globalCompositeOperation = 'source-over';
      ctx.fillStyle = 'rgba(17,24,39,0.18)'; // slightly translucent clear
      ctx.fillRect(0, 0, width, height);

      ctx.save();
      ctx.translate(cx, cy);
      ctx.globalCompositeOperation = 'lighter';

      for(let s of stars){
        // Forward movement in z (towards viewer)
        s.z -= cfg.speed;
        if(s.z < 0.12){ Object.assign(s, newStar()); }

        // Noise-driven flow in XY
        const nx = s.x * cfg.flowScale;
        const ny = s.y * cfg.flowScale;
        const nt = t / (1/cfg.timeScale);
        const angle = noise2D(nx + nt*0.6, ny - nt*0.45) * Math.PI * 2;
        const drift = cfg.flowAmp * (1.1 + (1.0 - Math.min(1, s.z/cfg.depth))); // nearer moves slightly more
        s.x += Math.cos(angle) * drift;
        s.y += Math.sin(angle) * drift;

        // Parallax by pointer
        const px = s.x + pointer.x * 0.0015 * s.z;
        const py = s.y + pointer.y * 0.0015 * s.z;

        // Perspective projection
        const f = 260 / (s.z * 100);
        const sx = px * f * 100;
        const sy = py * f * 100;

        // Size and alpha by depth
        const size = Math.max(0.6, (cfg.size * (1.8 - s.z)) * DPR);
        const alpha = Math.max(0.12, 0.9 - s.z * 0.35);

        // Color cycling by time and depth
        const hue = (cfg.hueBase + (t * 360 * cfg.hueSpeed) + s.z * 24) % 360;
        ctx.globalAlpha = alpha;
        ctx.fillStyle = hsl(hue, cfg.sat, cfg.light);
        ctx.beginPath();
        ctx.arc(sx, sy, size, 0, Math.PI*2);
        ctx.fill();
      }

      ctx.restore();
      requestAnimationFrame(step);
    }

    function onPointer(e){
      const rect = canvas.getBoundingClientRect();
      const x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left - rect.width/2;
      const y = (e.touches ? e.touches[0].clientY : e.clientY) - rect.top - rect.height/2;
      pointer.tx = x * DPR; pointer.ty = y * DPR;
    }

    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', onPointer, { passive: true });
    window.addEventListener('touchmove', onPointer, { passive: true });

    resize();
    requestAnimationFrame(step);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  }else{ init(); }
})();