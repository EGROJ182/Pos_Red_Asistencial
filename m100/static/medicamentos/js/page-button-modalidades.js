document.addEventListener("DOMContentLoaded", function() {
    viewsButtonsPageModalidades();
});

function buttonFirstModalidades(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-modalidades');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-modalidades');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', 1);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePageModalidades(1, totalPages);
        document.getElementById('modalidades-table-container').innerHTML = data.modalidades;
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function buttonLastModalidades(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-modalidades');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-modalidades');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', totalPages);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePageModalidades(totalPages, totalPages);
        document.getElementById('modalidades-table-container').innerHTML = data.modalidades;
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}
function buttonNextModalidades(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-modalidades');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-modalidades');
    let next = document.querySelector('#next-modalidades').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', next);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('modalidades-table-container').innerHTML = data.modalidades;
        validatePageModalidades(parseInt(next), parseInt(totalPages));
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function buttonPreviousModalidades(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-modalidades');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-modalidades');
    let previous = document.querySelector('#previous-modalidades').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', previous);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('modalidades-table-container').innerHTML = data.modalidades;
        validatePageProveedores(previous, totalPages);
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function validatePageModalidades(page, totalPages) {
    if (parseInt(page) >= parseInt(totalPages)) {
        document.getElementById('page-number-modalidades').innerText = totalPages;
        document.getElementById('next-modalidades').innerText = totalPages;
        document.getElementById('previous-modalidades').innerText = totalPages-1;
        document.getElementById('btn-next-modalidades').style.display = "none";
        document.getElementById('btn-last-modalidades').style.display = "none";
        document.getElementById('btn-first-modalidades').style.display = "block";
        document.getElementById('btn-previous-modalidades').style.display = "block";
    }
    else if (parseInt(page) <= 1) {
        document.getElementById('page-number-modalidades').innerText = 1;
        document.getElementById('next-modalidades').innerText = 2;
        document.getElementById('previous-modalidades').innerText = 1;
        document.getElementById('btn-previous-modalidades').style.display = "none";
        document.getElementById('btn-first-modalidades').style.display = "none";
        document.getElementById('btn-next-modalidades').style.display = "block";
        document.getElementById('btn-last-modalidades').style.display = "block";
    }
    else {
        document.getElementById('previous-modalidades').innerText = parseInt(page)-1;
        document.getElementById('next-modalidades').innerText = parseInt(page)+1;
        document.getElementById('page-number-modalidades').innerText = page;
        document.getElementById('btn-next-modalidades').style.display = "block";
        document.getElementById('btn-first-modalidades').style.display = "block";
        document.getElementById('btn-last-modalidades').style.display = "block";
        document.getElementById('btn-previous-modalidades').style.display = "block";
    }
}

function viewsButtonsPageModalidades() {
    const result = document.getElementById('result-query-modalidades').textContent;
    if(parseInt(result)<101) {
        document.getElementById('page-modalidades').disabled = true;
        document.getElementById('btn-next-modalidades').style.display = 'none';
        document.getElementById('btn-last-modalidades').style.display = 'none';
        document.getElementById('btn-first-modalidades').style.display = 'none';
        document.getElementById('btn-previous-modalidades').style.display = 'none';
        document.getElementById('btn-page-modalidades').style.display = 'none';
    }
    else{
        document.getElementById('page-modalidades').disabled = false;
        document.getElementById('btn-first-modalidades').style.display = 'none';
        document.getElementById('btn-previous-modalidades').style.display = 'none';
        document.getElementById('btn-next-modalidades').style.display = 'block';
        document.getElementById('btn-last-modalidades').style.display = 'block';
        document.getElementById('btn-page-modalidades').style.display = 'block';
    }
}