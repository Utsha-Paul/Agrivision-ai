/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        agri: {
          dark: '#0B291A',
          sidebar: '#0D3522',
          sidebarHover: '#164830',
          forest: '#134E35',
          emerald: '#166534',
          primary: '#10B981',
          accent: '#22C55E',
          lime: '#4ADE80',
          soft: '#E8F5E9',
          lightBg: '#F3F6F4',
          card: '#FFFFFF',
          border: '#E2E8F0',
          danger: '#EF4444',
          warning: '#F59E0B'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(16, 185, 129, 0.08), 0 2px 14px 0 rgba(0, 0, 0, 0.04)',
        'card': '0 4px 20px -2px rgba(18, 53, 34, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.02)',
        'hover': '0 12px 30px -4px rgba(16, 185, 129, 0.15), 0 4px 12px -2px rgba(0, 0, 0, 0.05)'
      }
    },
  },
  plugins: [],
}

