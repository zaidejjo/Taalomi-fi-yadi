// legendary.js
// تأثيرات 3D, parallax, particles, navbar effects, ripple buttons.
// يشتغل بعد DOMContentLoaded

(function(){
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /*************************
   * Helpers
   *************************/
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a,b,t) => a + (b-a)*t;

  /*************************
   * 3D Tilt for .card-legendary
   *************************/
  function initTiltCards() {
    const cards = document.querySelectorAll('.card-legendary');
    if(!cards.length || prefersReducedMotion) return;

    cards.forEach(card => {
      // ensure relative container
      card.style.transformStyle = 'preserve-3d';
      card.style.willChange = 'transform';
      // create glare overlay
      let glare = card.querySelector('.tilt-glare');
      if(!glare){
        glare = document.createElement('div');
        glare.className = 'tilt-glare';
        card.appendChild(glare);
      }

      let rect = null;
      let rafId = null;
      let state = { rx:0, ry:0, sx:1 };

      function onMove(e){
        rect = rect || card.getBoundingClientRect();
        const x = (e.clientX ?? e.touches?.[0]?.clientX) - rect.left;
        const y = (e.clientY ?? e.touches?.[0]?.clientY) - rect.top;
        const px = (x / rect.width) - 0.5; // -0.5 .. 0.5
        const py = (y / rect.height) - 0.5;

        // angles
        const maxTilt = parseFloat(card.dataset.tilt || 12);
        const ry = clamp( px * maxTilt * -1, -maxTilt, maxTilt);
        const rx = clamp( py * maxTilt, -maxTilt, maxTilt);
        const scale = parseFloat(card.dataset- scale) || 1.03;

        state.ry = ry;
        state.rx = rx;
        state.sx = scale;

        if(!rafId){
          rafId = requestAnimationFrame(render);
        }
      }

      function onLeave(){
        state.rx = 0; state.ry = 0; state.sx = 1;
        if(!rafId) rafId = requestAnimationFrame(render);
      }

      function render(){
        rafId = null;
        const transform = `perspective(1200px) rotateX(${state.rx}deg) rotateY(${state.ry}deg) scale(${state.sx})`;
        card.style.transform = transform;

        // glare position
        const glareX = (50 + (state.ry * 2)); // tweak
        const glareY = (50 - (state.rx * 2));
        glare.style.background = `radial-gradient(circle at ${glareX}% ${glareY}%, rgba(255,255,255,0.55), rgba(255,255,255,0.15) 25%, rgba(255,255,255,0) 60%)`;
      }

      card.addEventListener('mousemove', onMove, {passive:true});
      card.addEventListener('touchmove', onMove, {passive:true});
      card.addEventListener('mouseleave', onLeave);
      card.addEventListener('touchend', onLeave);
    });
  }

  /*************************
   * Parallax micro-movements for elements with [data-parallax]
   *************************/
  function initParallax() {
    if(prefersReducedMotion) return;
    const layers = Array.from(document.querySelectorAll('[data-parallax]'));
    if(!layers.length) return;

    let winW = window.innerWidth, winH = window.innerHeight;
    const state = { x:0, y:0, tx:0, ty:0 };

    window.addEventListener('resize', ()=> { winW = window.innerWidth; winH = window.innerHeight; });

    document.addEventListener('mousemove', e => {
      const cx = e.clientX - (winW/2);
      const cy = e.clientY - (winH/2);
      state.tx = cx / (winW/2);
      state.ty = cy / (winH/2);
    }, {passive:true});

    function update(){
      state.x = lerp(state.x, state.tx, 0.08);
      state.y = lerp(state.y, state.ty, 0.08);

      layers.forEach(el => {
        const depth = parseFloat(el.dataset.parallax) || 8; // higher = more movement
        const tx = -state.x * depth;
        const ty = -state.y * depth;
        el.style.transform = `translate3d(${tx}px, ${ty}px, 0)`;
      });

      requestAnimationFrame(update);
    }
    update();
  }

  /*************************
   * Particles background (canvas)
   *************************/
  function initParticles() {
    if(prefersReducedMotion) return;
    // create canvas overlay once
    if(document.getElementById('legendary-particles')) return;
    const canvas = document.createElement('canvas');
    canvas.id = 'legendary-particles';
    canvas.style.position = 'fixed';
    canvas.style.left = 0; canvas.style.top = 0;
    canvas.style.width = '100%'; canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = 0; // behind content; adjust in CSS if needed
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let DPR = Math.max(1, window.devicePixelRatio || 1);

    function resize(){
      canvas.width = Math.floor(window.innerWidth * DPR);
      canvas.height = Math.floor(window.innerHeight * DPR);
      canvas.style.width = window.innerWidth + 'px';
      canvas.style.height = window.innerHeight + 'px';
      ctx.setTransform(DPR,0,0,DPR,0,0);
    }
    window.addEventListener('resize', resize);
    resize();

    // create small particles
    const particles = [];
    const NUM = Math.floor((window.innerWidth * window.innerHeight) / 80000) + 25; // scale with viewport

    for(let i=0;i<NUM;i++){
      particles.push({
        x: Math.random()*window.innerWidth,
        y: Math.random()*window.innerHeight,
        r: 0.6 + Math.random()*1.6,
        vx: (Math.random()-0.5)*0.12,
        vy: -0.05 - Math.random()*0.12,
        alpha: 0.05 + Math.random()*0.2
      });
    }

    function loop(){
      ctx.clearRect(0,0,canvas.width, canvas.height);
      particles.forEach(p=>{
        p.x += p.vx;
        p.y += p.vy;
        if(p.y < -10) { p.y = window.innerHeight + 10; p.x = Math.random()*window.innerWidth; }
        if(p.x < -20) p.x = window.innerWidth + 20;
        if(p.x > window.innerWidth + 20) p.x = -20;
        ctx.beginPath();
        ctx.globalAlpha = p.alpha;
        ctx.fillStyle = 'rgba(255,255,255,1)';
        ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
        ctx.fill();
      });
      ctx.globalAlpha = 1;
      requestAnimationFrame(loop);
    }
    loop();
  }

  /*************************
   * Navbar blur & shrink on scroll
   *************************/
  function initNavbarScroll() {
    const nav = document.querySelector('.navbar');
    if(!nav) return;
    let lastScroll = 0;
    const maxOffset = 80;

    function onScroll(){
      const y = window.scrollY || window.pageYOffset;
      const t = clamp(y / maxOffset, 0, 1);
      // blur and background fade
      nav.style.backdropFilter = `blur(${lerp(0,6,t)}px)`;
      nav.style.backgroundColor = `rgba(18, 24, 36, ${lerp(0.06, 0.95, t)})`;
      nav.style.transition = 'background-color 220ms linear, backdrop-filter 220ms linear';
      // shrink
      nav.style.padding = lerp(16,8,t) + 'px 0';
      lastScroll = y;
    }

    window.addEventListener('scroll', onScroll, {passive:true});
    onScroll();
  }

  /*************************
   * Button ripple for anchors and buttons
   *************************/
  function initRipples() {
    document.addEventListener('pointerdown', function(e){
      const el = e.target.closest('.ripple, .btn, .nav-link, .dropdown-item, button');
      if(!el) return;
      const rect = el.getBoundingClientRect();
      const circle = document.createElement('span');
      const size = Math.max(rect.width, rect.height) * 1.4;
      circle.style.width = circle.style.height = size + 'px';
      circle.style.left = (e.clientX - rect.left - size/2) + 'px';
      circle.style.top  = (e.clientY - rect.top  - size/2) + 'px';
      circle.className = 'legendary-ripple';
      el.appendChild(circle);
      // remove after animation
      setTimeout(()=> circle.remove(), 650);
    }, {passive:true});
  }

  /*************************
   * Small helper: animate gradient on elements with [data-animate-gradient]
   *************************/
  function initAnimatedGradients() {
    const els = document.querySelectorAll('[data-animate-gradient]');
    if(!els.length || prefersReducedMotion) return;
    els.forEach(el => {
      el.classList.add('legendary-animated-gradient');
    });
  }

  /*************************
   * Init all
   *************************/
  function initAll() {
    initTiltCards();
    initParallax();
    initParticles();
    initNavbarScroll();
    initRipples();
    initAnimatedGradients();
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

})();
