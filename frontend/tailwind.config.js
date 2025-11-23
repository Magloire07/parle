/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Palette sombre de Parle
        dark: {
          bg: '#0a0a0a',
          'bg-secondary': '#1a1a1a',
          'bg-card': '#252525',
          text: '#e5e5e5',
          'text-secondary': '#a3a3a3',
        },
        primary: {
          DEFAULT: '#3b82f6',
          hover: '#2563eb',
        },
        secondary: {
          DEFAULT: '#8b5cf6',
          hover: '#7c3aed',
        },
        success: '#10b981',
        error: '#ef4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
