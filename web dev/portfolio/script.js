/* ================================================
   SHIVANSH DARJI - AI/ML PORTFOLIO
   Interactive JavaScript - Neural Network Background,
   Typewriter, Scroll Animations, Custom Cursor
   ================================================ */

// ==========================================
//  PRELOADER
// ==========================================
window.addEventListener('load', () => {
    setTimeout(() => {
        document.getElementById('preloader').classList.add('loaded');
    }, 2000);
});

// ==========================================
//  NEURAL NETWORK BACKGROUND CANVAS
// ==========================================
class NeuralNetwork {
    constructor() {
        this.canvas = document.getElementById('neural-bg');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: null, y: null };
        this.particleCount = 80;
        this.connectionDistance = 150;
        this.init();
    }

    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
        this.createParticles();
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.2,
                pulseSpeed: Math.random() * 0.02 + 0.01,
                pulsePhase: Math.random() * Math.PI * 2
            });
        }
    }

    drawParticle(p, time) {
        const pulse = Math.sin(time * p.pulseSpeed + p.pulsePhase) * 0.3 + 0.7;
        const r = p.radius * pulse;
        
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
        this.ctx.fillStyle = `rgba(108, 92, 231, ${p.opacity * pulse})`;
        this.ctx.fill();
        
        // Glow effect
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, r * 3, 0, Math.PI * 2);
        this.ctx.fillStyle = `rgba(108, 92, 231, ${p.opacity * pulse * 0.1})`;
        this.ctx.fill();
    }

    drawConnections() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < this.connectionDistance) {
                    const opacity = (1 - dist / this.connectionDistance) * 0.15;
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.strokeStyle = `rgba(108, 92, 231, ${opacity})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            }
        }
    }

    drawMouseConnections() {
        if (!this.mouse.x || !this.mouse.y) return;
        
        for (const p of this.particles) {
            const dx = p.x - this.mouse.x;
            const dy = p.y - this.mouse.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 200) {
                const opacity = (1 - dist / 200) * 0.3;
                this.ctx.beginPath();
                this.ctx.moveTo(p.x, p.y);
                this.ctx.lineTo(this.mouse.x, this.mouse.y);
                this.ctx.strokeStyle = `rgba(0, 210, 255, ${opacity})`;
                this.ctx.lineWidth = 0.8;
                this.ctx.stroke();
            }
        }
    }

    update() {
        for (const p of this.particles) {
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;

            // Mouse interaction - subtle attraction
            if (this.mouse.x && this.mouse.y) {
                const dx = this.mouse.x - p.x;
                const dy = this.mouse.y - p.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 200) {
                    p.vx += dx * 0.00005;
                    p.vy += dy * 0.00005;
                }
            }

            // Limit velocity
            const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
            if (speed > 1) {
                p.vx *= 0.99;
                p.vy *= 0.99;
            }
        }
    }

    animate() {
        const time = Date.now();
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.drawConnections();
        this.drawMouseConnections();
        
        for (const p of this.particles) {
            this.drawParticle(p, time);
        }
        
        this.update();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize neural network after DOM loaded
document.addEventListener('DOMContentLoaded', () => {
    new NeuralNetwork();
});

// ==========================================
//  CUSTOM CURSOR
// ==========================================
const cursorDot = document.querySelector('.cursor-dot');
const cursorRing = document.querySelector('.cursor-ring');

if (cursorDot && cursorRing) {
    let mouseX = 0, mouseY = 0;
    let ringX = 0, ringY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        cursorDot.style.transform = `translate(${mouseX - 3}px, ${mouseY - 3}px)`;
    });

    function animateCursor() {
        ringX += (mouseX - ringX) * 0.15;
        ringY += (mouseY - ringY) * 0.15;
        cursorRing.style.transform = `translate(${ringX - 18}px, ${ringY - 18}px)`;
        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // Hover effect
    const hoverElements = document.querySelectorAll('a, button, .project-card, .achievement-card, .skill-category, .timeline-content, .contact-method, .education-card');
    hoverElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursorRing.classList.add('hover'));
        el.addEventListener('mouseleave', () => cursorRing.classList.remove('hover'));
    });
}

// ==========================================
//  TYPEWRITER EFFECT
// ==========================================
class Typewriter {
    constructor(element, texts, speed = 60) {
        this.element = element;
        this.texts = texts;
        this.speed = speed;
        this.deleteSpeed = 30;
        this.pauseTime = 2000;
        this.currentTextIndex = 0;
        this.currentCharIndex = 0;
        this.isDeleting = false;
        this.type();
    }

    type() {
        const currentText = this.texts[this.currentTextIndex];
        
        if (this.isDeleting) {
            this.currentCharIndex--;
            this.element.textContent = currentText.substring(0, this.currentCharIndex);
            
            if (this.currentCharIndex === 0) {
                this.isDeleting = false;
                this.currentTextIndex = (this.currentTextIndex + 1) % this.texts.length;
                setTimeout(() => this.type(), 500);
                return;
            }
            setTimeout(() => this.type(), this.deleteSpeed);
        } else {
            this.currentCharIndex++;
            this.element.textContent = currentText.substring(0, this.currentCharIndex);
            
            if (this.currentCharIndex === currentText.length) {
                this.isDeleting = true;
                setTimeout(() => this.type(), this.pauseTime);
                return;
            }
            setTimeout(() => this.type(), this.speed);
        }
    }
}

// Initialize typewriter after preloader
setTimeout(() => {
    const typewriterEl = document.getElementById('typewriter');
    if (typewriterEl) {
        new Typewriter(typewriterEl, [
            'cat role.txt → AI/ML Engineer & Data Scientist',
            'python train_model.py --epochs 100 --lr 0.001',
            'echo "Passionate about building intelligent systems"',
            'git commit -m "Pushing innovation forward 🚀"',
            'jupyter notebook --port 8888',
            'sklearn.fit(data) → accuracy: 97.3%'
        ]);
    }
}, 2200);

// ==========================================
//  NAVBAR SCROLL EFFECT
// ==========================================
const navbar = document.getElementById('navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    
    if (currentScroll > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// Active nav link based on scroll
const sections = document.querySelectorAll('.section, #hero');
const navLinks = document.querySelectorAll('.nav-links a');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 200;
        if (window.scrollY >= sectionTop) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// ==========================================
//  MOBILE MENU
// ==========================================
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mobileMenu.classList.toggle('active');
    });

    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            mobileMenu.classList.remove('active');
        });
    });
}

// ==========================================
//  SCROLL REVEAL ANIMATIONS
// ==========================================
const revealElements = document.querySelectorAll('.reveal-up, .reveal-text');

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const delay = entry.target.dataset.delay || 0;
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, parseInt(delay));
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

revealElements.forEach(el => revealObserver.observe(el));

// ==========================================
//  SKILL BAR ANIMATION
// ==========================================
const skillBars = document.querySelectorAll('.skill-progress');

const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const width = entry.target.dataset.width;
            entry.target.style.width = width + '%';
            entry.target.classList.add('animated');
        }
    });
}, {
    threshold: 0.3
});

skillBars.forEach(bar => skillObserver.observe(bar));

// ==========================================
//  COUNTER ANIMATION
// ==========================================
const counters = document.querySelectorAll('.stat-number');

const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const target = parseInt(entry.target.dataset.count);
            const duration = 2000;
            const start = 0;
            const startTime = Date.now();

            function updateCounter() {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing function
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = Math.floor(start + (target - start) * eased);
                
                entry.target.textContent = current;
                
                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    entry.target.textContent = target;
                }
            }

            updateCounter();
            counterObserver.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.5
});

counters.forEach(counter => counterObserver.observe(counter));

// ==========================================
//  SMOOTH SCROLL FOR ANCHOR LINKS
// ==========================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ==========================================
//  CONTACT FORM
// ==========================================
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const btn = contactForm.querySelector('.btn-submit');
        const originalText = btn.innerHTML;
        
        btn.innerHTML = '<span>Sending...</span><i class="fas fa-spinner fa-spin"></i>';
        btn.disabled = true;
        
        // Simulate sending (replace with actual form handler)
        setTimeout(() => {
            btn.innerHTML = '<span>Message Sent!</span><i class="fas fa-check"></i>';
            btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.style.background = '';
                btn.disabled = false;
                contactForm.reset();
            }, 3000);
        }, 1500);
    });
}

// ==========================================
//  TILT EFFECT FOR PROJECT CARDS
// ==========================================
const projectCards = document.querySelectorAll('.project-card');

projectCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        
        // Move glow
        const glow = card.querySelector('.project-glow');
        if (glow) {
            glow.style.left = `${x - rect.width}px`;
            glow.style.top = `${y - rect.height}px`;
        }
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = '';
    });
});

// ==========================================
//  PARALLAX EFFECT FOR HERO
// ==========================================
window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const hero = document.querySelector('.hero-content');
    if (hero && scrolled < window.innerHeight) {
        hero.style.transform = `translateY(${scrolled * 0.3}px)`;
        hero.style.opacity = 1 - scrolled / (window.innerHeight * 0.8);
    }
});

// ==========================================
//  KONAMI-STYLE EASTER EGG (Data Matrix)
// ==========================================
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    if (JSON.stringify(konamiCode) === JSON.stringify(konamiSequence)) {
        document.body.style.transition = 'filter 2s ease';
        document.body.style.filter = 'hue-rotate(180deg)';
        setTimeout(() => {
            document.body.style.filter = 'none';
        }, 3000);
    }
});

// ==========================================
//  PAGE VISIBILITY - PAUSE ANIMATIONS
// ==========================================
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        document.title = "Come back! 👋 | Shivansh Darji";
    } else {
        document.title = "Shivansh Darji | AI/ML Engineer & Data Scientist";
    }
});
