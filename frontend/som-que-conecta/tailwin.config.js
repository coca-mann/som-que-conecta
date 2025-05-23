/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./index.html", // Se aplicável
      "./src/**/*.{vue,js,ts,jsx,tsx}" // Essencial para o Vue
    ],
    theme: {
      extend: {
        // Suas personalizações de tema virão aqui
      },
    },
    plugins: [
      // Outros plugins do Tailwind (não PostCSS plugins) viriam aqui
    ],
  }