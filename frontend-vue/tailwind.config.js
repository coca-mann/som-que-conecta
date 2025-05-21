// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{vue,js,ts,jsx,tsx}", // Escaneia todos os arquivos Vue e JS/TS dentro de src
    ],
    theme: {
      extend: {
        // Você pode estender o tema padrão aqui (cores, fontes, espaçamentos, etc.)
        // Exemplo baseado nas cores que você usou:
        colors: {
          emerald: {
            50: '#ecfdf5',
            100: '#d1fae5',
            200: '#a7f3d0',
            // ... adicione outros tons se precisar estender ou customizar
            500: '#10b981',
            600: '#059669',
            700: '#047857',
            800: '#065f46',
          },
          amber: {
            // ...
          },
          rose: {
            // ...
          }
        },
        fontFamily: {
          // sans: ['Inter', 'sans-serif'], // Exemplo se você importar a fonte Inter
        }
      },
    },
    plugins: [
      // require('@tailwindcss/forms'), // Exemplo de plugin
    ],
  }