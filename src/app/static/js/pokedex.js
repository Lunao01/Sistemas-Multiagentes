let currentOffset = 0;
const limit = 20;
const apiUrl = "https://pokeapi.co/api/v2/pokemon";
const grid = document.getElementById("pokedex-grid");
const loadMoreButton = document.getElementById("load-more");
const sortSelect = document.getElementById("sort-select");

// Cargar Pokémon desde la API
async function fetchPokemons(offset, limit) {
    const response = await fetch(`${apiUrl}?offset=${offset}&limit=${limit}`);
    const data = await response.json();
    return data.results;
}

// Crear tarjeta HTML para un Pokémon
async function createPokemonCard(pokemon) {
    const response = await fetch(pokemon.url);
    const details = await response.json();
    const types = details.types.map(t => `<span class="type ${t.type.name}">${t.type.name}</span>`).join("");
    return `
        <div class="pokemon-card">
            <img src="${details.sprites.front_default}" alt="${pokemon.name}">
            <div class="number">N.º ${details.id.toString().padStart(4, "0")}</div>
            <h2>${pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1)}</h2>
            <div class="types">${types}</div>
        </div>
    `;
}

// Renderizar Pokémon en el grid
async function renderPokemons(offset, limit) {
    const pokemons = await fetchPokemons(offset, limit);
    const cards = await Promise.all(pokemons.map(createPokemonCard));
    grid.innerHTML += cards.join("");
}

// Ordenar Pokémon (reemplazar lógica según back)
function sortPokemons() {
    // Para implementar ordenación
}

// Evento: Cargar más Pokémon
loadMoreButton.addEventListener("click", async () => {
    currentOffset += limit;
    await renderPokemons(currentOffset, limit);
});

// Evento: Ordenar Pokémon
sortSelect.addEventListener("change", () => {
    grid.innerHTML = ""; // Limpiar el grid
    currentOffset = 0; // Reiniciar paginación
    renderPokemons(currentOffset, limit);
});

// Cargar Pokémon inicial
renderPokemons(currentOffset, limit);
