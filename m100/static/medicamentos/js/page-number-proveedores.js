function loadPageProveedores(event) {
    event.preventDefault(); 
    const pageLink = document.getElementById('pageLink');
    const page = document.getElementById('page-proveedores');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-proveedores');
    
    let pageNumber = validateBlankProveedores(page.value);

    // Establece el número de página en la URL
    url.searchParams.set('page', pageNumber);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('proveedores-table-container').innerHTML = data.proveedores;
        validateNumberProveedores(pageNumber, totalPages);
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    pageLink.href = url.href;        
}

function updatePageLinkProveedores() {
    const pageInput = document.getElementById('page-proveedores');
    const pageLink = document.getElementById('pageLink');
    const pageNumber = pageInput.value;
    const totalPages = pageInput.getAttribute('data-total-pages-proveedores');
    
    if (pageNumber >= 1 && pageNumber <= totalPages) {
        pageLink.setAttribute('onclick', `loadPage(event, ${pageNumber})`);
    }
}

function validateNumberProveedores(page, totalPages) {
    if (parseInt(page) >= parseInt(totalPages)) {
        document.getElementById('page-number-proveedores').innerText = totalPages;
        document.getElementById('next-proveedores').innerText = parseInt(totalPages);
        document.getElementById('previous-proveedores').innerText = parseInt(totalPages)-1;
        document.getElementById('page-number-proveedores').innerText = totalPages;
        document.getElementById('page-proveedores').value = totalPages;
        document.getElementById('btn-next-proveedores').style.display = "none";
        document.getElementById('btn-last-proveedores').style.display = "none";
        document.getElementById('btn-first-proveedores').style.display = "block";
        document.getElementById('btn-previous-proveedores').style.display = "block";
    }
    else if (parseInt(page) <= 1) {
        document.getElementById('page-number-proveedores').innerText = 1;
        document.getElementById('next-proveedores').innerText = 2;
        document.getElementById('previous-proveedores').innerText = parseInt(totalPages);
        document.getElementById('btn-previous-proveedores').style.display = "none";
        document.getElementById('btn-first-proveedores').style.display = "none";
        document.getElementById('btn-next-proveedores').style.display = "block";
        document.getElementById('btn-last-proveedores').style.display = "block";
    }
    else {
        document.getElementById('previous-proveedores').innerText = parseInt(page)-1;
        document.getElementById('next-proveedores').innerText = parseInt(page)+1;
        document.getElementById('page-number-proveedores').innerText = page;
        document.getElementById('btn-next-proveedores').style.display = "block";
        document.getElementById('btn-first-proveedores').style.display = "block";
        document.getElementById('btn-last-proveedores').style.display = "block";
        document.getElementById('btn-previous-proveedores').style.display = "block";
    }
}

function validateBlankProveedores(page) {
    if (page=="") return 1;
    else return page;
}