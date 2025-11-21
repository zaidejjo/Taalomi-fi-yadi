// legendary.js
(function(){
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const lerp = (a,b,t) => a + (b-a)*t;

  /***************
   3D Tilt
  ***************/
  function initTiltCards() {
    const cards = document.querySelectorAll('.card-legendary');
    if(!cards.length || prefersReducedMotion) return;

    cards.forEach(card=>{
      card.style.transformStyle = 'preserve-3d';
      card.style.willChange = 'transform';
      card.dataset.tiltMax = parseFloat(card.dataset.tilt) || 12;

      card.addEventListener('mousemove', e=>{
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const px = (x/rect.width -0.5)*2;
        const py = (y/rect.height -0.5)*2;
        const rx = py*card.dataset.tiltMax;
        const ry = -px*card.dataset.tiltMax;
        card.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg) scale(1.05)`;
      });

      card.addEventListener('mouseleave', ()=>{
        card.style.transform = 'rotateX(0) rotateY(0) scale(1)';
      });
    });
  }

  /***************
   Ripple effect
  ***************/
  function initRipples() {
    document.addEventListener('pointerdown', function(e){
      const el = e.target.closest('.ripple, .btn');
      if(!el) return;
      const rect = el.getBoundingClientRect();
      const circle = document.createElement('span');
      const size = Math.max(rect.width, rect.height) * 1.5;
      circle.style.width = circle.style.height = size + 'px';
      circle.style.left = (e.clientX - rect.left - size/2) + 'px';
      circle.style.top = (e.clientY - rect.top - size/2) + 'px';
      circle.className = 'legendary-ripple';
      el.appendChild(circle);
      setTimeout(()=>circle.remove(), 600);
    });
  }

  /***************
   Particles background
  ***************/
  function initParticles() {
    if(prefersReducedMotion) return;
    const canvas = document.createElement('canvas');
    canvas.id='legendary-particles';
    canvas.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:-1;';
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    let w = window.innerWidth, h = window.innerHeight;
    const DPR = window.devicePixelRatio || 1;

    function resize(){
      w = window.innerWidth; h=window.innerHeight;
      canvas.width=w*DPR; canvas.height=h*DPR;
      canvas.style.width=w+'px'; canvas.style.height=h+'px';
      ctx.setTransform(DPR,0,0,DPR,0,0);
    }
    window.addEventListener('resize', resize);
    resize();

    const particles=[];
    const NUM = Math.floor((w*h)/80000)+25;
    for(let i=0;i<NUM;i++){
      particles.push({x:Math.random()*w,y:Math.random()*h,r:0.6+Math.random()*1.5,vx:(Math.random()-0.5)*0.1,vy:-0.05-Math.random()*0.1,alpha:0.05+Math.random()*0.2});
    }

    function loop(){
      ctx.clearRect(0,0,canvas.width,canvas.height);
      particles.forEach(p=>{
        p.x+=p.vx; p.y+=p.vy;
        if(p.y<-10){p.y=h+10;p.x=Math.random()*w;}
        if(p.x<-20)p.x=w+20;
        if(p.x>w+20)p.x=-20;
        ctx.beginPath();
        ctx.globalAlpha=p.alpha;
        ctx.fillStyle='rgba(255,255,255,1)';
        ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
        ctx.fill();
      });
      ctx.globalAlpha=1;
      requestAnimationFrame(loop);
    }
    loop();
  }

  function initAll(){
    initTiltCards();
    initRipples();
    initParticles();
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', initAll);
  } else { initAll(); }
})();
