document.addEventListener("DOMContentLoaded", function() {
    viewsButtonsPage();
});

function buttonFirst(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', 1);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePage(1, totalPages);
        document.getElementById('medicamentos-table-container').innerHTML = data.html;
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function buttonLast(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', totalPages);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePage(totalPages, totalPages);
        document.getElementById('medicamentos-table-container').innerHTML = data.html;
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}
function buttonNext(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages');
    let next = document.querySelector('#next').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', next);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('medicamentos-table-container').innerHTML = data.html;
        validatePage(parseInt(next), parseInt(totalPages));
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function buttonPrevious(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages');
    let previous = document.querySelector('#previous').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', previous);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        document.getElementById('medicamentos-table-container').innerHTML = data.html;
        validatePage(previous, totalPages);
    })
    .catch(error => console.error('Error:', error));
    
    // Actualiza el href del enlace
    // pageLink.href = url.href;        
}

function validatePage(page, totalPages) {
    if (parseInt(page) >= parseInt(totalPages)) {
        document.getElementById('page-number').innerText = totalPages;
        document.getElementById('next').innerText = totalPages;
        document.getElementById('previous').innerText = totalPages-1;
        // document.getElementById('page').value = totalPages;
        document.getElementById('btn-next').style.display = "none";
        document.getElementById('btn-last').style.display = "none";
        document.getElementById('btn-first').style.display = "block";
        document.getElementById('btn-previous').style.display = "block";
    }
    else if (parseInt(page) <= 1) {
        document.getElementById('page-number').innerText = 1;
        document.getElementById('next').innerText = 2;
        document.getElementById('previous').innerText = 1;
        // document.getElementById('page').value = 1;
        document.getElementById('btn-previous').style.display = "none";
        document.getElementById('btn-first').style.display = "none";
        document.getElementById('btn-next').style.display = "block";
        document.getElementById('btn-last').style.display = "block";
    }
    else {
        document.getElementById('previous').innerText = parseInt(page)-1;
        document.getElementById('next').innerText = parseInt(page)+1;
        document.getElementById('page-number').innerText = page;
        // document.getElementById('page').value = parseInt(page);
        document.getElementById('btn-next').style.display = "block";
        document.getElementById('btn-first').style.display = "block";
        document.getElementById('btn-last').style.display = "block";
        document.getElementById('btn-previous').style.display = "block";
    }
}

function viewsButtonsPage() {
    const result = document.getElementById('result-query').textContent;
    if(parseInt(result)<21) {
        document.getElementById('page').disabled = true;
        document.getElementById('btn-next').style.display = 'none';
        document.getElementById('btn-last').style.display = 'none';
        document.getElementById('btn-first').style.display = 'none';
        document.getElementById('btn-previous').style.display = 'none';
        document.getElementById('btn-page').style.display = 'none';
    }
    else{
        document.getElementById('page').disabled = false;
        document.getElementById('btn-first').style.display = 'none';
        document.getElementById('btn-previous').style.display = 'none';
        document.getElementById('btn-next').style.display = 'block';
        document.getElementById('btn-last').style.display = 'block';
        document.getElementById('btn-page').style.display = 'block';
    }
}