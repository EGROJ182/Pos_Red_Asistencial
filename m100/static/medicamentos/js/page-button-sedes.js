document.addEventListener("DOMContentLoaded", function() {
    viewsButtonsPageSedes();
});

function buttonFirstSedes(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-sedes');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-sedes');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', 1);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePageSedes(1, totalPages);
        document.getElementById('sedes-table-container').innerHTML = data.proveedores;
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function buttonLastSedes(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-sedes');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-sedes');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', totalPages);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePageSedes(totalPages, totalPages);
        document.getElementById('sedes-table-container').innerHTML = data.sedes;
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}
function buttonNextSedes(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-sedes');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-sedes');
    let next = document.querySelector('#next-sedes').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', next);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('sedes-table-container').innerHTML = data.sedes;
        validatePageSedes(parseInt(next), parseInt(totalPages));
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function buttonPreviousSedes(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-sedes');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-sedes');
    let previous = document.querySelector('#previous-sedes').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', previous);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('sedes-table-container').innerHTML = data.sedes;
        validatePageProveedores(previous, totalPages);
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function validatePageSedes(page, totalPages) {
    if (parseInt(page) >= parseInt(totalPages)) {
        document.getElementById('page-number-sedes').innerText = totalPages;
        document.getElementById('next-sedes').innerText = totalPages;
        document.getElementById('previous-sedes').innerText = totalPages-1;
        document.getElementById('btn-next-sedes').style.display = "none";
        document.getElementById('btn-last-sedes').style.display = "none";
        document.getElementById('btn-first-sedes').style.display = "block";
        document.getElementById('btn-previous-sedes').style.display = "block";
    }
    else if (parseInt(page) <= 1) {
        document.getElementById('page-number-sedes').innerText = 1;
        document.getElementById('next-sedes').innerText = 2;
        document.getElementById('previous-sedes').innerText = 1;
        document.getElementById('btn-previous-sedes').style.display = "none";
        document.getElementById('btn-first-sedes').style.display = "none";
        document.getElementById('btn-next-sedes').style.display = "block";
        document.getElementById('btn-last-sedes').style.display = "block";
    }
    else {
        document.getElementById('previous-sedes').innerText = parseInt(page)-1;
        document.getElementById('next-sedes').innerText = parseInt(page)+1;
        document.getElementById('page-number-sedes').innerText = page;
        document.getElementById('btn-next-sedes').style.display = "block";
        document.getElementById('btn-first-sedes').style.display = "block";
        document.getElementById('btn-last-sedes').style.display = "block";
        document.getElementById('btn-previous-sedes').style.display = "block";
    }
}

function viewsButtonsPageSedes() {
    const result = document.getElementById('result-query-sedes').textContent;
    if(parseInt(result)<101) {
        document.getElementById('page-sedes').disabled = true;
        document.getElementById('btn-next-sedes').style.display = 'none';
        document.getElementById('btn-last-sedes').style.display = 'none';
        document.getElementById('btn-first-sedes').style.display = 'none';
        document.getElementById('btn-previous-sedes').style.display = 'none';
        document.getElementById('btn-page-sedes').style.display = 'none';
    }
    else{
        document.getElementById('page-sedes').disabled = false;
        document.getElementById('btn-first-sedes').style.display = 'none';
        document.getElementById('btn-previous-sedes').style.display = 'none';
        document.getElementById('btn-next-sedes').style.display = 'block';
        document.getElementById('btn-last-sedes').style.display = 'block';
        document.getElementById('btn-page-sedes').style.display = 'block';
    }
}