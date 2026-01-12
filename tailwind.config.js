/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class',
    content: [
        "./templates/**/*.html",
        "./static/js/**/*.js"
    ],
    safelist: [
        'translate-x-0',
        'overflow-hidden',
        // Mobile navbar classes
        'md:hidden',
        'md:pb-0',
        'pb-20',
        'fixed',
        'bottom-0',
        'left-0',
        'right-0',
        'top-0',
        'z-50',
        'grid-cols-2',
        'gap-3',
        'md:gap-4',
        'md:columns-3',
        'lg:columns-4',
        'md:space-y-4',
        'bg-background/60',
        'backdrop-blur-md',
        // Schedule Page Dynamic Classes
        'md:flex-row',
        'md:w-1/2',
        'space-y-16',
        'space-y-8',
        'relative',
        'flex',
        'flex-col',
        'top-8',
        'right-1/2',
        'left-1/2',
        'group-hover:scale-150',
        'group-hover:bg-primary/50',
        'group-hover:-translate-y-1',
        'group-hover:shadow-xl'
    ],
    theme: {
        extend: {
            colors: {
                border: "hsl(var(--border))",
                input: "hsl(var(--input))",
                ring: "hsl(var(--ring))",
                background: "hsl(var(--background))",
                foreground: "hsl(var(--foreground))",
                primary: {
                    DEFAULT: "hsl(var(--primary))",
                    foreground: "hsl(var(--primary-foreground))",
                },
                secondary: {
                    DEFAULT: "hsl(var(--secondary))",
                    foreground: "hsl(var(--secondary-foreground))",
                },
                destructive: {
                    DEFAULT: "hsl(var(--destructive))",
                    foreground: "hsl(var(--destructive-foreground))",
                },
                muted: {
                    DEFAULT: "hsl(var(--muted))",
                    foreground: "hsl(var(--muted-foreground))",
                },
                accent: {
                    DEFAULT: "hsl(var(--accent))",
                    foreground: "hsl(var(--accent-foreground))",
                },
                popover: {
                    DEFAULT: "hsl(var(--popover))",
                    foreground: "hsl(var(--popover-foreground))",
                },
                card: {
                    DEFAULT: "hsl(var(--card))",
                    foreground: "hsl(var(--card-foreground))",
                },
                'devops-blue': '#2563eb',
                'devops-purple': '#7c3aed',
                'devops-green': '#059669',
                'tech-dark': '#0f172a',
                'tech-gray': '#334155'
            },
            fontFamily: {
                'sans': ['Inter', 'system-ui', 'sans-serif'],
                'mono': ['JetBrains Mono', 'monospace']
            },
            backgroundImage: {
                'tech-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'dark-gradient': 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)'
            },
            animation: {
                'float': 'float 6s ease-in-out infinite',
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translatey(0px)' },
                    '50%': { transform: 'translatey(-20px)' }
                }
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
    ],
}
