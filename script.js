// ===== UTILITY FUNCTIONS =====
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// Debounce function for performance
const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// ===== NAVIGATION =====
class Navigation {
  constructor() {
    this.navbar = $('#navbar');
    this.navToggle = $('#nav-toggle');
    this.navMenu = $('#nav-menu');
    this.navLinks = $$('.nav-link');

    this.init();
  }

  init() {
    this.bindEvents();
    this.initScrollEffect();
  }

  bindEvents() {
    // Mobile menu toggle
    this.navToggle?.addEventListener('click', () => this.toggleMobileMenu());

    // Close mobile menu when clicking on links
    this.navLinks.forEach(link => {
      link.addEventListener('click', () => this.closeMobileMenu());
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!this.navbar.contains(e.target) && this.navMenu.classList.contains('active')) {
        this.closeMobileMenu();
      }
    });
  }

  toggleMobileMenu() {
    this.navMenu.classList.toggle('active');
    this.navToggle.classList.toggle('active');
    document.body.style.overflow = this.navMenu.classList.contains('active') ? 'hidden' : '';
  }

  closeMobileMenu() {
    this.navMenu.classList.remove('active');
    this.navToggle.classList.remove('active');
    document.body.style.overflow = '';
  }

  initScrollEffect() {
    const handleScroll = debounce(() => {
      const scrollY = window.scrollY;
      if (scrollY > 50) {
        this.navbar.style.background = 'rgba(15, 15, 35, 0.98)';
        this.navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.3)';
      } else {
        this.navbar.style.background = 'rgba(15, 15, 35, 0.95)';
        this.navbar.style.boxShadow = 'none';
      }
    }, 10);

    window.addEventListener('scroll', handleScroll);
  }
}

// ===== SMOOTH SCROLLING =====
class SmoothScroll {
  constructor() {
    this.init();
  }

  init() {
    // Smooth scroll for navigation links
    $$('a[href^="#"]').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetElement = $(targetId);

        if (targetElement) {
          const offsetTop = targetElement.offsetTop - 70; // Account for fixed navbar
          window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
          });
        }
      });
    });
  }
}

// ===== ANIMATED COUNTERS =====
class AnimatedCounters {
  constructor() {
    this.counters = $$('.stat-number');
    this.init();
  }

  init() {
    this.createObserver();
  }

  createObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    this.counters.forEach(counter => observer.observe(counter));
  }

  animateCounter(counter) {
    const target = parseInt(counter.getAttribute('data-target'));
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      counter.textContent = Math.floor(current);
    }, 16);
  }
}

// ===== SKILL BARS ANIMATION =====
class SkillBars {
  constructor() {
    this.skillBars = $$('.skill-progress');
    this.init();
  }

  init() {
    this.createObserver();
  }

  createObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateSkillBar(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    this.skillBars.forEach(bar => observer.observe(bar));
  }

  animateSkillBar(bar) {
    const width = bar.getAttribute('data-width');
    setTimeout(() => {
      bar.style.width = `${width}%`;
    }, 300);
  }
}

// ===== SCROLL ANIMATIONS =====
class ScrollAnimations {
  constructor() {
    this.animatedElements = $$('.section, .project-card, .skill-category, .timeline-item');
    this.init();
  }

  init() {
    this.createObserver();
  }

  createObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    this.animatedElements.forEach(element => {
      element.style.opacity = '0';
      element.style.transform = 'translateY(30px)';
      element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      observer.observe(element);
    });
  }
}

// ===== PARTICLE SYSTEM =====
class ParticleSystem {
  constructor() {
    this.canvas = $('#particle-canvas');
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.animationId = null;

    this.init();
  }

  init() {
    this.setupCanvas();
    this.createParticles();
    this.animate();
    this.handleResize();
  }

  setupCanvas() {
    const resizeCanvas = () => {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
  }

  createParticles() {
    const particleCount = Math.min(150, Math.floor((window.innerWidth * window.innerHeight) / 8000));

    for (let i = 0; i < particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 2 + 1,
        opacity: Math.random() * 0.5 + 0.2,
        color: `hsl(${Math.random() * 60 + 200}, 70%, 60%)` // Blue to purple range
      });
    }
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    this.particles.forEach((particle, index) => {
      // Update position
      particle.x += particle.vx;
      particle.y += particle.vy;

      // Wrap around edges
      if (particle.x < 0) particle.x = this.canvas.width;
      if (particle.x > this.canvas.width) particle.x = 0;
      if (particle.y < 0) particle.y = this.canvas.height;
      if (particle.y > this.canvas.height) particle.y = 0;

      // Draw particle
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      this.ctx.fillStyle = particle.color;
      this.ctx.globalAlpha = particle.opacity;
      this.ctx.fill();

      // Draw connections
      this.particles.slice(index + 1).forEach(otherParticle => {
        const distance = Math.sqrt(
          Math.pow(particle.x - otherParticle.x, 2) +
          Math.pow(particle.y - otherParticle.y, 2)
        );

        if (distance < 100) {
          this.ctx.beginPath();
          this.ctx.moveTo(particle.x, particle.y);
          this.ctx.lineTo(otherParticle.x, otherParticle.y);
          this.ctx.strokeStyle = particle.color;
          this.ctx.globalAlpha = (100 - distance) / 100 * 0.2;
          this.ctx.lineWidth = 0.5;
          this.ctx.stroke();
        }
      });
    });

    this.animationId = requestAnimationFrame(() => this.animate());
  }

  handleResize() {
    window.addEventListener('resize', debounce(() => {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
    }, 250));
  }
}

// ===== FORM VALIDATION =====
class ContactForm {
  constructor() {
    this.form = $('#contact-form');
    this.init();
  }

  init() {
    if (!this.form) return;

    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    this.addInputValidation();
  }

  handleSubmit(e) {
    e.preventDefault();

    if (this.validateForm()) {
      this.showSuccessMessage();
      this.form.reset();
    }
  }

  validateForm() {
    const name = $('#name').value.trim();
    const email = $('#email').value.trim();
    const subject = $('#subject').value.trim();
    const message = $('#message').value.trim();

    if (!name || !email || !subject || !message) {
      this.showError('Please fill in all fields');
      return false;
    }

    if (!this.isValidEmail(email)) {
      this.showError('Please enter a valid email address');
      return false;
    }

    return true;
  }

  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  addInputValidation() {
    const inputs = this.form.querySelectorAll('input, textarea');

    inputs.forEach(input => {
      input.addEventListener('blur', () => {
        if (input.value.trim()) {
          input.style.borderColor = 'var(--success-color)';
        } else {
          input.style.borderColor = 'var(--error-color)';
        }
      });

      input.addEventListener('focus', () => {
        input.style.borderColor = 'var(--primary-color)';
      });
    });
  }

  showError(message) {
    this.showMessage(message, 'error');
  }

  showSuccessMessage() {
    this.showMessage('Message sent successfully! I\'ll get back to you soon.', 'success');
  }

  showMessage(message, type) {
    // Remove existing message
    const existingMessage = $('.form-message');
    if (existingMessage) existingMessage.remove();

    const messageElement = document.createElement('div');
    messageElement.className = `form-message ${type}`;
    messageElement.textContent = message;

    messageElement.style.cssText = `
      padding: 1rem;
      border-radius: 0.5rem;
      margin-bottom: 1rem;
      font-weight: 500;
      background: ${type === 'error' ? 'var(--error-color)' : 'var(--success-color)'};
      color: white;
      opacity: 0;
      transform: translateY(-10px);
      transition: all 0.3s ease;
    `;

    this.form.insertBefore(messageElement, this.form.firstChild);

    // Animate in
    setTimeout(() => {
      messageElement.style.opacity = '1';
      messageElement.style.transform = 'translateY(0)';
    }, 10);

    // Remove after 5 seconds
    setTimeout(() => {
      messageElement.style.opacity = '0';
      messageElement.style.transform = 'translateY(-10px)';
      setTimeout(() => messageElement.remove(), 300);
    }, 5000);
  }
}

// ===== THEME SWITCHER =====
class ThemeSwitcher {
  constructor() {
    this.init();
  }

  init() {
    // Add theme switcher button to navigation
    this.addThemeButton();
  }

  addThemeButton() {
    const navMenu = $('.nav-menu');
    if (!navMenu) return;

    const themeButton = document.createElement('li');
    themeButton.className = 'nav-item';
    themeButton.innerHTML = '<button class="theme-toggle" id="theme-toggle"><i class="fas fa-moon"></i></button>';

    navMenu.appendChild(themeButton);

    $('#theme-toggle').addEventListener('click', () => this.toggleTheme());
  }

  toggleTheme() {
    document.body.classList.toggle('light-theme');
    const icon = $('.theme-toggle i');

    if (document.body.classList.contains('light-theme')) {
      icon.className = 'fas fa-sun';
      localStorage.setItem('theme', 'light');
    } else {
      icon.className = 'fas fa-moon';
      localStorage.setItem('theme', 'dark');
    }
  }
}

// ===== PERFORMANCE OPTIMIZATIONS =====
class PerformanceOptimizer {
  constructor() {
    this.init();
  }

  init() {
    this.optimizeImages();
    this.addPreloadHints();
  }

  optimizeImages() {
    // Lazy loading for images
    const images = $$('img[data-src]');

    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
          }
        });
      });

      images.forEach(img => imageObserver.observe(img));
    }
  }

  addPreloadHints() {
    // Add preload hints for critical resources
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'font';
    link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap';
    link.crossOrigin = 'anonymous';
    document.head.appendChild(link);
  }
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
  // Initialize all components
  new Navigation();
  new SmoothScroll();
  new AnimatedCounters();
  new SkillBars();
  new ScrollAnimations();
  new ParticleSystem();
  new ContactForm();
  new ThemeSwitcher();
  new PerformanceOptimizer();

  // Add loading animation
  document.body.style.opacity = '0';
  setTimeout(() => {
    document.body.style.transition = 'opacity 0.5s ease';
    document.body.style.opacity = '1';
  }, 100);
});

// ===== ERROR HANDLING =====
window.addEventListener('error', (e) => {
  console.error('JavaScript error:', e.error);
});

// ===== ACCESSIBILITY =====
document.addEventListener('keydown', (e) => {
  // Skip to main content with Tab
  if (e.key === 'Tab' && !e.shiftKey) {
    const focusableElements = $$('a, button, input, textarea, select');
    if (focusableElements.length > 0) {
      focusableElements[0].focus();
    }
  }

  // Close mobile menu with Escape
  if (e.key === 'Escape') {
    const navigation = new Navigation();
    if (navigation.navMenu?.classList.contains('active')) {
      navigation.closeMobileMenu();
    }
  }
});

// ===== WEBKIT BACKDROP FILTER FIX =====
if (CSS.supports('backdrop-filter', 'blur(10px)') === false) {
  const navbar = $('#navbar');
  if (navbar) {
    navbar.style.background = 'rgba(15, 15, 35, 0.98)';
  }
}
