/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./dist/*.{html,js}"], // Adjust this path as per your project structure
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: ["light", "dark", "wireframe"], // Specify the themes you want to use
  },
}
