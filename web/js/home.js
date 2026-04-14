/* ============================================================
   Homepage: particle canvas, spotlight rotation, content tabs
   Vanilla JS, no dependencies
   ============================================================ */

(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ----------------------------------------------------------
     1. Particle Network Canvas
     ---------------------------------------------------------- */
  function initParticles() {
    var canvas = document.getElementById('hero-canvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var dpr = window.devicePixelRatio || 1;
    var w, h;
    var particles = [];
    var mouseX = -9999, mouseY = -9999;
    var rafId = null;

    function resize() {
      w = canvas.offsetWidth;
      h = canvas.offsetHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function createParticles() {
      var count = w < 768 ? 50 : 80;
      particles = [];
      for (var i = 0; i < count; i++) {
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          r: Math.random() * 1.5 + 0.8,
          alpha: Math.random() * 0.35 + 0.15
        });
      }
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);
      var len = particles.length;

      for (var i = 0; i < len; i++) {
        var p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h;
        if (p.y > h) p.y = 0;

        var dx = p.x - mouseX;
        var dy = p.y - mouseY;
        var dist = Math.sqrt(dx * dx + dy * dy);
        var a = p.alpha;
        if (dist < 150) {
          a = Math.min(a + 0.3 * (1 - dist / 150), 0.8);
          var push = 0.7 * (1 - dist / 150);
          p.x += (dx / dist) * push;
          p.y += (dy / dist) * push;
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(68,216,241,' + a + ')';
        ctx.fill();
      }

      for (var i = 0; i < len; i++) {
        for (var j = i + 1; j < len; j++) {
          var dx = particles[i].x - particles[j].x;
          var dy = particles[i].y - particles[j].y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            var lineAlpha = (1 - dist / 120) * 0.12;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = 'rgba(68,216,241,' + lineAlpha + ')';
            ctx.lineWidth = 0.6;
            ctx.stroke();
          }
        }
      }
    }

    function loop() {
      draw();
      rafId = requestAnimationFrame(loop);
    }

    canvas.addEventListener('mousemove', function (e) {
      var rect = canvas.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
    });

    canvas.addEventListener('mouseleave', function () {
      mouseX = -9999;
      mouseY = -9999;
    });

    // Click to spawn a new particle
    canvas.addEventListener('click', function (e) {
      var rect = canvas.getBoundingClientRect();
      var cx = e.clientX - rect.left;
      var cy = e.clientY - rect.top;
      particles.push({
        x: cx,
        y: cy,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        r: Math.random() * 1.5 + 0.8,
        alpha: Math.random() * 0.35 + 0.15
      });
    });

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
      } else if (!reducedMotion && !rafId) {
        rafId = requestAnimationFrame(loop);
      }
    });

    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        resize();
        createParticles();
      }, 200);
    });

    resize();
    createParticles();

    if (reducedMotion) {
      draw();
    } else {
      loop();
    }
  }

  /* ----------------------------------------------------------
     2. Featured Spotlight Rotation
     ---------------------------------------------------------- */
  function initSpotlight() {
    var slides = document.querySelectorAll('.spotlight-slide');
    var dots = document.querySelectorAll('.spotlight-dot');
    if (slides.length < 2) return;

    var current = 0;
    var timer = null;
    var viewport = document.querySelector('.spotlight-viewport');

    function show(index) {
      slides[current].classList.remove('active');
      if (dots[current]) dots[current].classList.remove('active');
      current = index;
      slides[current].classList.add('active');
      if (dots[current]) dots[current].classList.add('active');
    }

    function advance() {
      show((current + 1) % slides.length);
    }

    function startTimer() {
      if (reducedMotion) return;
      stopTimer();
      timer = setInterval(advance, 12000);
    }

    function stopTimer() {
      if (timer) { clearInterval(timer); timer = null; }
    }

    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        show(i);
        startTimer();
      });
    });

    if (viewport) {
      viewport.addEventListener('mouseenter', function () { stopTimer(); });
      viewport.addEventListener('mouseleave', function () { startTimer(); });
      viewport.addEventListener('focusin', function () { stopTimer(); });
      viewport.addEventListener('focusout', function () { startTimer(); });
    }

    startTimer();
  }

  /* ----------------------------------------------------------
     3. Content Tabs (Latest / Top)
     ---------------------------------------------------------- */
  function initTabs() {
    var tabs = document.querySelectorAll('.content-tab');
    var panels = document.querySelectorAll('.tab-panel');
    if (!tabs.length || !panels.length) return;

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var target = tab.getAttribute('data-tab');

        // Switch active tab
        tabs.forEach(function (t) { t.classList.remove('active'); });
        tab.classList.add('active');

        // Switch visible panel
        panels.forEach(function (p) {
          if (p.id === 'tab-' + target) {
            p.classList.add('active');
          } else {
            p.classList.remove('active');
          }
        });
      });
    });
  }

  /* ----------------------------------------------------------
     Init all on DOMContentLoaded
     ---------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
    initParticles();
    initSpotlight();
    initTabs();
  });
})();
