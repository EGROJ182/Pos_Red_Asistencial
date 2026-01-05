document.addEventListener("DOMContentLoaded", function() {
    viewsButtonConsult();
});

function viewsButtonConsult() {
    if(document.getElementById('result-query')) {
        const result = document.getElementById('result-query').textContent;
        const tableContainer = document.getElementById('medicamentos-table-container');
        const paginationContent = document.getElementById('content-pagination');
        
        const sectionContent = document.getElementById('table-pagination');
        
        if (result != 0) {
            tableContainer.classList.remove('fade-out');
            paginationContent.classList.remove('fade-out');
            tableContainer.style.display = 'block';
            paginationContent.style.display = 'block';
            tableContainer.classList.add('fade-in');
            paginationContent.classList.add('fade-in');
            
            sectionContent.style.transition = 'max-height 1s ease';
            sectionContent.style.maxHeight = '700px'; // Expande la sección

        } else {
            tableContainer.classList.remove('fade-in');
            paginationContent.classList.remove('fade-in');
            tableContainer.classList.add('fade-out');
            paginationContent.classList.add('fade-out');
            
            // sectionContent.style.transition = 'max-height 1s ease';
            sectionContent.style.maxHeight = sectionContent.scrollHeight + "px"; // Colapsa la sección
            
            setTimeout(() => {
                tableContainer.style.display = 'none';
                paginationContent.style.display = 'none';
            }, 1000); // Ajusta el tiempo para que coincida con la duración de la animación
            
        }
    }
}
