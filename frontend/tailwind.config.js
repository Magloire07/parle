/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  safelist: [
    'shadow-luxury',
    'shadow-luxury-lg',
    'shadow-gold',
  ],
  theme: {
    extend: {
      colors: {
        // Palette premium
        dark: {
          bg: '#0f0f0f',
          'bg-secondary': '#1c1c1e',
          'bg-card': '#2c2c2e',
          'bg-hover': '#3a3a3c',
          text: '#f5f5f7',
          'text-secondary': '#98989d',
          border: '#48484a',
        },
        gold: {
          DEFAULT: '#d4af37',
          light: '#f4e5b0',
          dark: '#b8941f',
        },
        primary: {
          DEFAULT: '#0a84ff',
          hover: '#0070e0',
          light: '#64b5ff',
        },
        accent: {
          DEFAULT: '#bf5af2',
          hover: '#a845d8',
          light: '#d98fff',
        },
        onion: {
          DEFAULT: '#5a189a',
          light: '#7b2cbf',
          dark: '#3c096c',
        },
        success: '#30d158',
        warning: '#ff9f0a',
        error: '#ff453a',
      },
      fontFamily: {
        serif: ['Playfair Display', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'luxury': '0 10px 40px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.2)',
        'luxury-lg': '0 20px 60px rgba(0, 0, 0, 0.4), 0 4px 16px rgba(0, 0, 0, 0.3)',
        'gold': '0 4px 20px rgba(212, 175, 55, 0.2)',
      },
    },
  },
  plugins: [],
}
