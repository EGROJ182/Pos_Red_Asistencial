function loadPageModalidades(event) {
    event.preventDefault(); 
    const pageLink = document.getElementById('pageLink');
    const page = document.getElementById('page-modalidades');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages-modalidades');
    
    let pageNumber = validateBlankModalidades(page.value);

    // Establece el número de página en la URL
    url.searchParams.set('page', pageNumber);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('modalidades-table-container').innerHTML = data.modalidades;
        validateNumberModalidades(pageNumber, totalPages);
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    pageLink.href = url.href;        
}

function updatePageLinkModalidades() {
    const pageInput = document.getElementById('page-modalidades');
    const pageLink = document.getElementById('pageLink');
    const pageNumber = pageInput.value;
    const totalPages = pageInput.getAttribute('data-total-pages-modalidades');
    
    if (pageNumber >= 1 && pageNumber <= totalPages) {
        pageLink.setAttribute('onclick', `loadPage(event, ${pageNumber})`);
    }
}

function validateNumberModalidades(page, totalPages) {
    if (parseInt(page) >= parseInt(totalPages)) {
        document.getElementById('page-number-modalidades').innerText = totalPages;
        document.getElementById('next-modalidades').innerText = parseInt(totalPages);
        document.getElementById('previous-modalidades').innerText = parseInt(totalPages)-1;
        document.getElementById('page-number-modalidades').innerText = totalPages;
        document.getElementById('page-modalidades').value = totalPages;
        document.getElementById('btn-next-modalidades').style.display = "none";
        document.getElementById('btn-last-modalidades').style.display = "none";
        document.getElementById('btn-first-modalidades').style.display = "block";
        document.getElementById('btn-previous-modalidades').style.display = "block";
    }
    else if (parseInt(page) <= 1) {
        document.getElementById('page-number-modalidades').innerText = 1;
        document.getElementById('next-modalidades').innerText = 2;
        document.getElementById('previous-modalidades').innerText = parseInt(totalPages);
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
        document.getElementById('btn-previous-mod').style.display = "block";
    }
}

function validateBlankModalidades(page) {
    if (page=="") return 1;
    else return page;
}