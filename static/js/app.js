document.addEventListener('DOMContentLoaded', function() {
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 800 } },
            color: { value: "#ffffff" },
            shape: { type: "circle" },
            opacity: { value: 0.5, random: true },
            size: { value: 3, random: true },
            line_linked: { enable: true, distance: 150, color: "#ffffff", opacity: 0.4, width: 1 },
            move: { enable: true, speed: 2, direction: "none", random: true, straight: false, out_mode: "out" }
        },
        interactivity: {
            detect_on: "canvas",
            events: {
                onhover: { enable: true, mode: "repulse" },
                onclick: { enable: true, mode: "push" }
            }
        }
    });

    // Magnetic Buttons Effect
    const magneticButtons = document.querySelectorAll('.magnetic');
    magneticButtons.forEach(button => {
        button.addEventListener('mousemove', (e) => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const deltaX = (x - centerX) / centerX * 10;
            const deltaY = (y - centerY) / centerY * 10;

            button.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = '';
        });
    });

    // Navbar Scroll Effect
    window.addEventListener('scroll', () => {
        const navbarEl = document.querySelector('.navbar');
        if (!navbarEl) return;
        if (window.scrollY > 50) {
            navbarEl.classList.add('scrolled');
        } else {
            navbarEl.classList.remove('scrolled');
        }
    });


    const navbar = document.querySelector('.navbar');
    const container = document.querySelector('.navbar .container');
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const logo = container ? container.querySelector('.logo') : null;

    if (!navbar || !container || !hamburger || !navLinks || !logo) return;

    function updateNavbarLayout() {
        const wasCollapsed = navbar.classList.contains('is-collapsed');

        navbar.classList.remove('is-collapsed');
        navLinks.classList.remove('active');
        document.body.classList.remove('menu-open');

        var gutter = 24;
        var logoWidth = Math.ceil(logo.getBoundingClientRect().width);
        var navWidth = Math.ceil(navLinks.scrollWidth);
        var used = logoWidth + navWidth + gutter;

        if (used > container.clientWidth) {
            navbar.classList.add('is-collapsed');
        } else if (wasCollapsed) {
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    }

    function debounce(fn, delay) {
        let t;
        return function() {
            clearTimeout(t);
            const args = arguments;
            const ctx = this;
            t = setTimeout(function(){ fn.apply(ctx, args); }, delay);
        };
    }

    if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(updateNavbarLayout);
    }
    setTimeout(updateNavbarLayout, 0);

    window.addEventListener('resize', debounce(updateNavbarLayout, 150));
    window.addEventListener('orientationchange', updateNavbarLayout);

    hamburger.addEventListener('click', () => {
        if (!navbar.classList.contains('is-collapsed')) return;

        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');

        const open = navLinks.classList.contains('active');
        hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
        document.body.classList.toggle('menu-open', open);
    });

    navLinks.addEventListener('click', (e) => {
        if (!navbar.classList.contains('is-collapsed')) return;
        if (e.target.closest('a')) {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('menu-open');
        }
    });
});
