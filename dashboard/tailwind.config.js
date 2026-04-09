/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#00D9FF',
        secondary: '#FF6B35',
        dark: '#1a1f2e',
        darker: '#0f1419',
      },
    },
  },
  plugins: [],
}
