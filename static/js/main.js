// DevOps Jogja Website JavaScript
// This file contains global JavaScript functionality for all pages
// Page-specific scripts are located in separate files (e.g., homepage.js)

document.addEventListener('DOMContentLoaded', function () {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');

            // Toggle hamburger icon
            const icon = this.querySelector('svg');
            if (mobileMenu.classList.contains('hidden')) {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
            } else {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
            }
        });
    }

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

    // Add scroll effect to navbar
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Initialize code copy functionality
    setTimeout(() => {
        initCodeCopy();
    }, 500);

    // Also try to initialize on window load
    window.addEventListener('load', function () {
        console.log('Window loaded, initializing copy again...');
        initCodeCopy();
    });

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe cards and tech icons for animation
    document.querySelectorAll('.tech-card, .event-card, .blog-card, .organizer-card').forEach(el => {
        el.classList.add('animate-out');
        observer.observe(el);
    });

    // Tech icons floating animation on homepage
    const techIcons = document.querySelectorAll('.animate-float');
    techIcons.forEach((icon, index) => {
        icon.style.animationDelay = `${index * 0.5}s`;
    });

    // Copy to clipboard functionality
    function copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(function () {
                showToast('Copied to clipboard!');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showToast('Copied to clipboard!');
        }
    }

    // Toast notification
    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'fixed bottom-4 right-4 bg-devops-blue text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-opacity duration-300';
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 2000);
    }

    // Search functionality (if search input exists)
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = this.value.toLowerCase();
            const items = document.querySelectorAll('.searchable-item');

            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(query)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Back to top button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = `
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path>
        </svg>
    `;
    backToTopBtn.className = 'fixed bottom-4 left-4 bg-devops-blue text-white p-3 rounded-full shadow-lg opacity-0 transition-opacity duration-300 hover:bg-blue-700 z-40';
    backToTopBtn.style.display = 'none';
    document.body.appendChild(backToTopBtn);

    backToTopBtn.addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    window.addEventListener('scroll', function () {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = 'block';
            setTimeout(() => {
                backToTopBtn.style.opacity = '1';
            }, 10);
        } else {
            backToTopBtn.style.opacity = '0';
            setTimeout(() => {
                backToTopBtn.style.display = 'none';
            }, 300);
        }
    });

    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
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



    // External link handling
    document.querySelectorAll('a[target="_blank"]').forEach(link => {
        link.setAttribute('rel', 'noopener noreferrer');
    });

    // Form validation (if forms exist)
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                } else {
                    field.classList.remove('border-red-500');
                }
            });

            if (!isValid) {
                e.preventDefault();
                showToast('Please fill in all required fields');
            }
        });
    });
});

// Alternative initialization for code copy
document.addEventListener('readystatechange', function () {
    if (document.readyState === 'complete') {
        console.log('Document ready state is complete, initializing copy...');
        initCodeCopy();
    }
});

// Code Copy Functionality
function initCodeCopy() {
    console.log('Initializing code copy functionality...');
    // Wrap all pre tags with code-container
    const preElements = document.querySelectorAll('pre');
    console.log('Found pre elements:', preElements.length);

    preElements.forEach((pre, index) => {
        console.log('Processing pre element', index, pre);
        if (!pre.closest('.code-container')) {
            const container = document.createElement('div');
            container.className = 'code-container';
            pre.parentNode.insertBefore(container, pre);
            container.appendChild(pre);

            // Add copy button
            const copyButton = createCopyButton();
            container.appendChild(copyButton);
            console.log('Added copy button to pre element', index);
        }
    });
}

function createCopyButton() {
    console.log('Creating copy button...');
    const button = document.createElement('button');
    button.className = 'copy-button';

    // Create SVG icon
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'copy-icon');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('viewBox', '0 0 24 24');

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('stroke-linecap', 'round');
    path.setAttribute('stroke-linejoin', 'round');
    path.setAttribute('stroke-width', '2');
    path.setAttribute('d', 'M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z');

    svg.appendChild(path);

    const span = document.createElement('span');
    span.textContent = 'Copy';

    button.appendChild(svg);
    button.appendChild(span);

    button.addEventListener('click', function () {
        console.log('Copy button clicked!');
        const codeContainer = this.closest('.code-container');
        const codeElement = codeContainer.querySelector('pre code') || codeContainer.querySelector('pre');
        const textToCopy = codeElement.textContent;

        console.log('Text to copy:', textToCopy.substring(0, 100) + '...');

        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(textToCopy).then(() => {
                console.log('Successfully copied to clipboard');
                // Success feedback
                this.classList.add('copied');

                // Change to checkmark icon
                path.setAttribute('d', 'M5 13l4 4L19 7');
                span.textContent = 'Copied!';

                setTimeout(() => {
                    this.classList.remove('copied');
                    // Change back to copy icon
                    path.setAttribute('d', 'M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z');
                    span.textContent = 'Copy';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                // Fallback for older browsers
                fallbackCopyTextToClipboard(textToCopy);
            });
        } else {
            console.log('Using fallback copy method');
            fallbackCopyTextToClipboard(textToCopy);
        }
    });

    console.log('Copy button created successfully');
    return button;
}

function fallbackCopyTextToClipboard(text) {
    console.log('Using fallback copy method for text:', text.substring(0, 50) + '...');
    const textArea = document.createElement("textarea");
    textArea.value = text;

    // Avoid scrolling to bottom
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            console.log('Fallback: Copying text command was successful');
            // Show success feedback
            const button = document.querySelector('.copy-button:hover') || document.querySelector('.copy-button');
            if (button) {
                button.classList.add('copied');
                const span = button.querySelector('span');
                const path = button.querySelector('path');
                if (span) span.textContent = 'Copied!';
                if (path) path.setAttribute('d', 'M5 13l4 4L19 7');

                setTimeout(() => {
                    button.classList.remove('copied');
                    if (span) span.textContent = 'Copy';
                    if (path) path.setAttribute('d', 'M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z');
                }, 2000);
            }
        } else {
            console.log('Fallback: Unable to copy');
        }
    } catch (err) {
        console.error('Fallback: Unable to copy', err);
    }

    document.body.removeChild(textArea);
}

// Copy to clipboard function for sharing
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function () {
            // Show success feedback
            showCopyFeedback('Link copied to clipboard!');
        }, function (err) {
            console.error('Could not copy text: ', err);
            fallbackCopyTextToClipboard(text);
        });
    } else {
        fallbackCopyTextToClipboard(text);
    }
}

// Fallback function for older browsers
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;

    // Avoid scrolling to bottom
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopyFeedback('Link copied to clipboard!');
        } else {
            showCopyFeedback('Failed to copy link', 'error');
        }
    } catch (err) {
        console.error('Fallback: Unable to copy', err);
        showCopyFeedback('Failed to copy link', 'error');
    }

    document.body.removeChild(textArea);
}

// Show copy feedback message
function showCopyFeedback(message, type = 'success') {
    // Remove existing feedback if any
    const existingFeedback = document.querySelector('.copy-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }

    // Create feedback element
    const feedback = document.createElement('div');
    feedback.className = `copy-feedback fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all duration-300 transform translate-y-0 ${type === 'error' ? 'bg-red-500 text-white' : 'bg-green-500 text-white'}`;
    feedback.textContent = message;

    document.body.appendChild(feedback);

    // Auto remove after 3 seconds
    setTimeout(() => {
        feedback.style.transform = 'translate-y-full opacity-0';
        setTimeout(() => {
            if (feedback.parentNode) {
                feedback.parentNode.removeChild(feedback);
            }
        }, 300);
    }, 3000);
}
