/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        // Cores customizadas para Pokémon
        'pokemon-fire': '#F08030',
        'pokemon-water': '#6890F0',
        'pokemon-grass': '#78C850',
        'pokemon-electric': '#F8D030',
        'pokemon-ice': '#98D8D8',
        'pokemon-fighting': '#C03028',
        'pokemon-poison': '#A040A0',
        'pokemon-ground': '#E0C068',
        'pokemon-flying': '#A890F0',
        'pokemon-psychic': '#F85888',
        'pokemon-bug': '#A8B820',
        'pokemon-rock': '#B8A038',
        'pokemon-ghost': '#705898',
        'pokemon-dragon': '#7038F8',
        'pokemon-dark': '#705848',
        'pokemon-steel': '#B8B8D0',
        'pokemon-fairy': '#EE99AC',
      }
    },
  },
  plugins: [],
}
