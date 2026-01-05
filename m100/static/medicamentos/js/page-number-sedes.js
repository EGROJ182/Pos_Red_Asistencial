function loadPageSedes(event) {
    event.preventDefault(); 
    const pageLink = document.getElementById('pageLink');
    const page = document.getElementById('page-sedes');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-sedes');
    
    let pageNumber = validateBlankSedes(page.value);

    // Establece el número de página en la URL
    url.searchParams.set('page', pageNumber);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('sedes-table-container').innerHTML = data.sedes;
        validateNumberSedes(pageNumber, totalPages);
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    pageLink.href = url.href;        
}

function updatePageLinkSedes() {
    const pageInput = document.getElementById('page-sedes');
    const pageLink = document.getElementById('pageLink');
    const pageNumber = pageInput.value;
    const totalPages = pageInput.getAttribute('data-total-pages-sedes');
    
    if (pageNumber >= 1 && pageNumber <= totalPages) {
        pageLink.setAttribute('onclick', `loadPage(event, ${pageNumber})`);
    }
}

function validateNumberSedes(page, totalPages) {
    if (parseInt(page) >= parseInt(totalPages)) {
        document.getElementById('page-number-sedes').innerText = totalPages;
        document.getElementById('next-sedes').innerText = parseInt(totalPages);
        document.getElementById('previous-sedes').innerText = parseInt(totalPages)-1;
        document.getElementById('page-number-sedes').innerText = totalPages;
        document.getElementById('page-sedes').value = totalPages;
        document.getElementById('btn-next-sedes').style.display = "none";
        document.getElementById('btn-last-sedes').style.display = "none";
        document.getElementById('btn-first-sedes').style.display = "block";
        document.getElementById('btn-previous-sedes').style.display = "block";
    }
    else if (parseInt(page) <= 1) {
        document.getElementById('page-number-sedes').innerText = 1;
        document.getElementById('next-sedes').innerText = 2;
        document.getElementById('previous-sedes').innerText = parseInt(totalPages);
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

function validateBlankSedes(page) {
    if (page=="") return 1;
    else return page;
}