/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{html,js,jsx,ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        heading: ["Lexend", "sans-serif"],
      },
      colors: {
        // Deep teal accent, picked to match the illustrations' lamp colour
        brand: {
          50: "#eef8f6",
          100: "#d5eee9",
          200: "#acdcd3",
          300: "#79c2b6",
          400: "#4aa497",
          500: "#2e877b",
          600: "#226d64",
          700: "#1d5852",
          800: "#1a4844",
          900: "#0f3d3e",
          950: "#082627",
        },
        sand: {
          50: "#fcfbf9",
          100: "#f8f6f3",
          200: "#efebe4",
          300: "#e2dcd1",
        },
        ink: "#141414",
      },
    },
  },
  plugins: [],
};
