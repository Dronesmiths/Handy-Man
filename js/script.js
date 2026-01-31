// Basic interactions scripts
document.addEventListener('DOMContentLoaded', () => {
    console.log('[BUSINESS_NAME] site loaded');

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Mobile Menu Toggle
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    const icon = mobileBtn ? mobileBtn.querySelector('i') : null;

    if (mobileBtn && navMenu) {
        mobileBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent bubbling
            navMenu.classList.toggle('active');

            // Toggle icon
            if (icon) {
                if (navMenu.classList.contains('active')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });

        // Close menu when clicking a link
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (navMenu.classList.contains('active') && !navMenu.contains(e.target) && !mobileBtn.contains(e.target)) {
                navMenu.classList.remove('active');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }


    // Dynamic Year in Footer
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // FAQ Accordion Functionality
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', function () {
            const item = this.parentElement;
            const content = item.querySelector('.accordion-content');
            const icon = this.querySelector('i');

            // Toggle active class
            item.classList.toggle('active');

            // Toggle content visibility
            if (item.classList.contains('active')) {
                content.style.maxHeight = content.scrollHeight + 'px';
                if (icon) icon.style.transform = 'rotate(180deg)';
            } else {
                content.style.maxHeight = '0';
                if (icon) icon.style.transform = 'rotate(0deg)';
            }
        });
    });

    // Comparison Slider Logic (Enhanced with Mobile Support)
    document.querySelectorAll('.av-yard-ba-slider').forEach(slider => {
        const range = slider.querySelector('.av-yard-range');
        const after = slider.querySelector('.av-yard-after');
        const divider = slider.querySelector('.av-yard-divider');
        const handle = slider.querySelector('.av-yard-handle');

        function update(val) {
            try {
                const clampedVal = Math.max(0, Math.min(100, val));
                if (after) after.style.clipPath = `inset(0 0 0 ${clampedVal}%)`;
                if (divider) divider.style.left = clampedVal + '%';
                if (handle) handle.style.left = clampedVal + '%';
            } catch (e) {
                console.error('Slider update error:', e);
            }
        }

        if (range && after && divider && handle) {
            // Initialize
            update(range.value || 50);

            // Desktop: input event
            range.addEventListener('input', e => update(e.target.value));

            // Mobile: touch events for better responsiveness
            range.addEventListener('touchstart', e => {
                e.preventDefault();
            }, { passive: false });

            range.addEventListener('touchmove', e => {
                e.preventDefault();
                const touch = e.touches[0];
                const rect = range.getBoundingClientRect();
                const percent = Math.max(0, Math.min(100, ((touch.clientX - rect.left) / rect.width) * 100));
                range.value = percent;
                update(percent);
            }, { passive: false });
        }
    });

    // Fence Restoration Slider Logic
    const baRange = document.getElementById('ba-range');
    const beforeImage = document.getElementById('before-image');
    if (baRange && beforeImage) {
        baRange.addEventListener('input', (e) => {
            beforeImage.style.width = e.target.value + '%';
        });
        // Initial state
        beforeImage.style.width = baRange.value + '%';
    }
});
