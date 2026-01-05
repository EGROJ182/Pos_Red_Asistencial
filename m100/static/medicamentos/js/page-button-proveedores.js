document.addEventListener("DOMContentLoaded", function() {
    viewsButtonsPageProveedores();
});

function buttonFirstProveedores(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-proveedores');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-proveedores');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', 1);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePageProveedores(1, totalPages);
        document.getElementById('proveedores-table-container').innerHTML = data.proveedores;
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function buttonLastProveedores(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-proveedores');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-proveedores');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', totalPages);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePageProveedores(totalPages, totalPages);
        document.getElementById('proveedores-table-container').innerHTML = data.proveedores;
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}
function buttonNextProveedores(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-proveedores');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-proveedores');
    let next = document.querySelector('#next-proveedores').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', next);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('proveedores-table-container').innerHTML = data.proveedores;
        validatePageProveedores(parseInt(next), parseInt(totalPages));
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function buttonPreviousProveedores(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page-proveedores');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-proveedores');
    let previous = document.querySelector('#previous-proveedores').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', previous);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('proveedores-table-container').innerHTML = data.proveedores;
        validatePageProveedores(previous, totalPages);
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function validatePageProveedores(page, totalPages) {
    if (parseInt(page) >= parseInt(totalPages)) {
        document.getElementById('page-number-proveedores').innerText = totalPages;
        document.getElementById('next-proveedores').innerText = totalPages;
        document.getElementById('previous-proveedores').innerText = totalPages-1;
        // document.getElementById('page').value = totalPages;
        document.getElementById('btn-next-proveedores').style.display = "none";
        document.getElementById('btn-last-proveedores').style.display = "none";
        document.getElementById('btn-first-proveedores').style.display = "block";
        document.getElementById('btn-previous-proveedores').style.display = "block";
    }
    else if (parseInt(page) <= 1) {
        document.getElementById('page-number-proveedores').innerText = 1;
        document.getElementById('next-proveedores').innerText = 2;
        document.getElementById('previous-proveedores').innerText = 1;
        // document.getElementById('page').value = 1;
        document.getElementById('btn-previous-proveedores').style.display = "none";
        document.getElementById('btn-first-proveedores').style.display = "none";
        document.getElementById('btn-next-proveedores').style.display = "block";
        document.getElementById('btn-last-proveedores').style.display = "block";
    }
    else {
        document.getElementById('previous-proveedores').innerText = parseInt(page)-1;
        document.getElementById('next-proveedores').innerText = parseInt(page)+1;
        document.getElementById('page-number-proveedores').innerText = page;
        // document.getElementById('page').value = parseInt(page);
        document.getElementById('btn-next-proveedores').style.display = "block";
        document.getElementById('btn-first-proveedores').style.display = "block";
        document.getElementById('btn-last-proveedores').style.display = "block";
        document.getElementById('btn-previous-proveedores').style.display = "block";
    }
}

function viewsButtonsPageProveedores() {
    const result = document.getElementById('result-query').textContent;
    if(parseInt(result)<101) {
        document.getElementById('page-proveedores').disabled = true;
        document.getElementById('btn-next-proveedores').style.display = 'none';
        document.getElementById('btn-last-proveedores').style.display = 'none';
        document.getElementById('btn-first-proveedores').style.display = 'none';
        document.getElementById('btn-previous-proveedores').style.display = 'none';
        document.getElementById('btn-page-proveedores').style.display = 'none';
    }
    else{
        document.getElementById('page-proveedores').disabled = false;
        document.getElementById('btn-first-proveedores').style.display = 'none';
        document.getElementById('btn-previous-proveedores').style.display = 'none';
        document.getElementById('btn-next-proveedores').style.display = 'block';
        document.getElementById('btn-last-proveedores').style.display = 'block';
        document.getElementById('btn-page-proveedores').style.display = 'block';
    }
}