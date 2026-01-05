function loadPage(event) {
    event.preventDefault(); 
    const pageLink = document.getElementById('pageLink');
    const page = document.getElementById('page');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages');
    
    let pageNumber = validateBlank(page.value);

    // Establece el número de página en la URL
    url.searchParams.set('page', pageNumber);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('medicamentos-table-container').innerHTML = data.html;
        validateNumber(pageNumber, totalPages);
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    pageLink.href = url.href;        
}

function updatePageLink() {
    const pageInput = document.getElementById('page');
    const pageLink = document.getElementById('pageLink');
    const pageNumber = pageInput.value;
    const totalPages = pageInput.getAttribute('data-total-pages');
    
    if (pageNumber >= 1 && pageNumber <= totalPages) {
        pageLink.setAttribute('onclick', `loadPage(event, ${pageNumber})`);
    }
}

function validateNumber(page, totalPages) {
    if (parseInt(page) >= parseInt(totalPages)) {
        document.getElementById('page-number').innerText = totalPages;
        document.getElementById('next').innerText = parseInt(totalPages);
        document.getElementById('previous').innerText = parseInt(totalPages)-1;
        document.getElementById('page-number').innerText = totalPages;
        document.getElementById('page').value = totalPages;
        document.getElementById('btn-next').style.display = "none";
        document.getElementById('btn-last').style.display = "none";
        document.getElementById('btn-first').style.display = "block";
        document.getElementById('btn-previous').style.display = "block";
    }
    else if (parseInt(page) <= 1) {
        document.getElementById('page-number').innerText = 1;
        document.getElementById('next').innerText = 2;
        document.getElementById('previous').innerText = parseInt(totalPages);
        document.getElementById('btn-previous').style.display = "none";
        document.getElementById('btn-first').style.display = "none";
        document.getElementById('btn-next').style.display = "block";
        document.getElementById('btn-last').style.display = "block";
    }
    else {
        document.getElementById('previous').innerText = parseInt(page)-1;
        document.getElementById('next').innerText = parseInt(page)+1;
        document.getElementById('page-number').innerText = page;
        document.getElementById('btn-next').style.display = "block";
        document.getElementById('btn-first').style.display = "block";
        document.getElementById('btn-last').style.display = "block";
        document.getElementById('btn-previous').style.display = "block";
    }
}

function validateBlank(page) {
    if (page=="") return 1;
    else return page;
}