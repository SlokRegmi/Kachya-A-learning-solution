/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  purge: ['.src/**/*.{js,jsx,ts,tsx}', './dist/**/*.html'], // Cover all HTML files in the dist directory
  content: ["./dist/**/*.{html,js}"], // Cover all HTML and JS files in the dist directory
  theme: {
    fontFamily: {
      'sans': ['Chivo', 'sans-serif'],
      'krub': ['Krub', 'sans-serif'],
      'serif': ['ui-serif', 'Georgia'],
      'mono': ['ui-monospace', 'SFMono-Regular'],
    },
    extend: {
      width: {
        'w-30': '30rem',
      },
      colors: {
        'custom-white': '#fffdfd',
        blue: {
          DEFAULT: '#243f78',
          '50': '#eef2fc',
          '100': '#d4def6',
          '200': '#b8c8f0',
          '300': '#6cab9d',
          '400': '#319c9a',
          '500': '#2b6a83',
          '600': '#243f78',
          '700': '#131b47',
          '800': '#243f78',
          '900': '#192a52'
        },
        grey: {
          DEFAULT: '#243f78',
          '50': '#eef2fc',
          '100': '#d4def6',
          '200': '#e1e1e3',
          '300': '#6cab9d',
          '400': '#319c9a',
          '500': '#2b6a83',
          '600': '#243f78',
          '700': '#131b47',
          '800': '#243f78',
          '900': '#192a52'
        }
      },
    },
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: ["light", "dark", "wireframe"], // Specify the themes you want to use
  },
};
