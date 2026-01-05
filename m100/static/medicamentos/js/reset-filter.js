document.addEventListener("DOMContentLoaded", function () {
    const resetFilters = document.querySelector(".reset-filters");

    if (resetFilters) {
        resetFilters.addEventListener("click", function (event) {
            event.preventDefault(); // Evita que se envíe el formulario al hacer clic en el botón
            const filters = document.querySelectorAll("#nombre, #nit, #codigo_de_habilitacion, #serv_nombre, #grse_nombre, #numero_contrato, #year_contrato, #sucursal, #supervisor, #categoria_cuentas_medicas, #numero_sede, #departamento, #municipio, #ese, #serv_codigo, #grse_codigo, #modalidad_intramural, #modalidad_unidad_movil, #modalidad_domiciliario, #modalidad_jornada_salud, #telemedicina_interactiva, #telemedicina_no_interactiva, #modalidad_tele_experticia, #modalidad_tele_monitoreo"); 
            
            filters.forEach((input) => {
                input.value = "";  // Limpia el contenido del input
                input.classList.remove("text-[red]");
                input.classList.remove("font-semibold");
                // input.style.removeProperty("color");
                // input.style.color = "black";  // Restaura el color del texto
            });
            
            // Opcionalmente, dispara el evento 'submit' si deseas actualizar la tabla al limpiar filtros
            // document.getElementById("filter-form").dispatchEvent(new Event("submit"));
        });
    }
});
