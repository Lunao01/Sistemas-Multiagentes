
// Control de errores en login/password
const popup = document.getElementById('popup');
const closePopupBtn = document.getElementById('closePopup');

// Cerrar el popup
closePopupBtn.addEventListener('click', () => {
    popup.style.display = 'none'; // Ocultar el popup
});
