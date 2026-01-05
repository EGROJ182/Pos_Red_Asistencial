// <!-- Script para manejar la apertura y cierre de los paneles -->
document.addEventListener('DOMContentLoaded', function() {
    // Abrir panel de sedes
    document.querySelectorAll('.toggle-sedes').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // Evitar propagación del evento
            const nit = this.getAttribute('data-nit');
            console.log('Abriendo sedes para NIT:', nit);
            const sedesPanel = document.getElementById('sedes-' + nit);
            if (sedesPanel) {
                sedesPanel.style.display = 'flex';
                sedesPanel.style.zIndex = '9999'; // Asegurar z-index correcto
            } else {
                console.error('Panel de sedes no encontrado:', 'sedes-' + nit);
            }
        });
    });

    // Cerrar panel de sedes
    document.querySelectorAll('.close-sedes').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // Evitar propagación del evento
            const nit = this.getAttribute('data-nit');
            document.getElementById('sedes-' + nit).style.display = 'none';
        });
    });

    // Abrir panel de servicios
    document.querySelectorAll('.toggle-servicios').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // Evitar propagación del evento
            const sedeId = this.getAttribute('data-sede-id');
            console.log('Abriendo servicios para sede:', sedeId);
            const serviciosPanel = document.getElementById('servicios-' + sedeId);
            if (serviciosPanel) {
                serviciosPanel.style.display = 'flex';
                serviciosPanel.style.zIndex = '10001'; // Asegurar z-index correcto
            } else {
                console.error('Panel de servicios no encontrado:', 'servicios-' + sedeId);
            }
        });
    });

    // Cerrar panel de servicios
    document.querySelectorAll('.close-servicios').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // Evitar propagación del evento
            const sedeId = this.getAttribute('data-sede-id');
            document.getElementById('servicios-' + sedeId).style.display = 'none';
        });
    });

    // Añadir listener para cerrar los paneles al hacer clic fuera
    document.addEventListener('click', function(e) {
        // Verificar si el clic fue fuera de los paneles modales
        const modales = document.querySelectorAll('.informacion');
        let dentroDePaneles = false;
        
        modales.forEach(function(modal) {
            if (modal.contains(e.target) || modal.style.display === 'none') {
                dentroDePaneles = true;
            }
        });
        
        // Si el clic fue fuera, cerrar todos los paneles
        if (!dentroDePaneles) {
            modales.forEach(function(modal) {
                modal.style.display = 'none';
            });
        }
    });
});
