/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        gemini: {
          blue: {
            light: '#89b4f8', // Lighter blue for highlights or secondary elements
            DEFAULT: '#1a73e8', // Primary Gemini blue
            dark: '#1665c0', // Darker blue for hover states or deeper elements
          },
          gray: {
            50: '#f8f9fa', // Renaming from 100 to 50 to match common scale
            100: '#f1f3f4',
            200: '#e8eaed',
            300: '#dadce0',
            400: '#bdc1c6',
            500: '#80868b',
            600: '#5f6368',
            700: '#3c4043',
            800: '#202124',
            900: '#111827', // Darkest gray, almost black
          },
          background: '#ffffff', // Default background
          surface: '#ffffff', // Surface color for cards, dialogs
          onPrimary: '#ffffff', // Text on primary color
          onSurface: '#202124', // Text on surface color
        },
        primary: {
          light: '#89b4f8',
          DEFAULT: '#1a73e8',
          dark: '#1665c0',
          // Adding shades for primary based on Gemini blue
          50: '#e8f0fe',
          100: '#d1e3fc',
          200: '#a8c7fa',
          300: '#8ab4f8',
          400: '#61a0f5',
          500: '#3b82f6', // Default from existing primary, similar to Gemini blue
          600: '#1b6ef3',
          700: '#1a73e8', // DEFAULT Gemini Blue
          800: '#1665c0',
          900: '#0d47a1',
        },
        gray: {
          // Replacing old gray with Gemini gray
          50: '#f8f9fa',
          100: '#f1f3f4',
          200: '#e8eaed',
          300: '#dadce0',
          400: '#bdc1c6',
          500: '#80868b',
          600: '#5f6368',
          700: '#3c4043',
          800: '#202124',
          900: '#111827',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-in': 'bounceIn 0.6s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        bounceIn: {
          '0%': { transform: 'scale(0.3)', opacity: '0' },
          '50%': { transform: 'scale(1.05)' },
          '70%': { transform: 'scale(0.9)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [() => import('@tailwindcss/typography')],
}
