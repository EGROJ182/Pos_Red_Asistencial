const clientId = 'f52e30b9a34d41398c05f63776c6a597'; // Reemplaza esto con tu Client ID
const redirectUri = 'https://jdjrq144-8000.use.devtunnels.ms/'; // Reemplaza esto con tu Redirect URI
const scopes = 'user-read-private user-read-email user-library-read playlist-read-private streaming'; // Ajusta los scopes según sea necesario

let accessToken;

// Función para obtener el token de acceso
function getAccessToken() {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('access_token');
    if (token) {
        accessToken = token;
        window.history.replaceState({}, document.title, "/"); // Limpiar la URL
        getPlaylists(); // Obtener listas de reproducción después de obtener el token
    } else {
        window.location = `https://accounts.spotify.com/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes}&response_type=token`;
    }
}

// Función para obtener las listas de reproducción
async function getPlaylists() {
    const response = await fetch('https://api.spotify.com/v1/me/playlists', {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    });
    
    if (response.ok) {
        const data = await response.json();
        displayPlaylists(data.items);
    } else if (response.status === 401) {
        console.error('Token de acceso inválido o expirada.');
        getAccessToken(); // Vuelve a obtener el token
    } else {
        console.error('Error fetching playlists:', response.status, response.statusText);
    }
}

// Función para mostrar las listas de reproducción
function displayPlaylists(playlists) {
    const playlistsContainer = document.getElementById('playlists');
    playlistsContainer.innerHTML = '';
    
    playlists.forEach(playlist => {
        const playlistElement = document.createElement('div');
        playlistElement.className = 'bg-white p-4 rounded shadow-md mb-2'; // Añadido margen inferior
        playlistElement.innerHTML = `
            <h3 class="font-bold">${playlist.name}</h3>
            <a href="${playlist.external_urls.spotify}" target="_blank" class="text-blue-500">Ver en Spotify</a>
        `;
        playlistsContainer.appendChild(playlistElement);
    });
}

// Ejecutar funciones al cargar el documento
document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('login-button');
    
    // Asegúrate de que el elemento existe antes de añadir el evento
    if (loginButton) {
        loginButton.addEventListener('click', getAccessToken);
    } else {
        console.error('El botón de inicio de sesión no se encontró en el DOM.');
    }
    
    // Intenta obtener el token de acceso al cargar
    getAccessToken(); 
});