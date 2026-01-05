def alert_color(novedad):
    if novedad.lower() == 'no aplica' or novedad.lower() == 'ok' or novedad.lower() == 'sin novedad':
        return 'default'
    else:
        return 'red'

def alert_color_termometro(factores_precio):
    if factores_precio.lower() == 'bajo':
        return 'green'
    elif factores_precio.lower() == 'medio':
        return 'orange'
    else:
        return 'red'

def alert_color_estandar(total_cums):
    if int(total_cums) >= 2900:
        return 'green'
    elif int(total_cums) >= 2000:
        return 'orange'
    else:
        return 'red'
    
def alert_img_zona(zona_especial):
    if zona_especial.lower() == 'si':
        return 'legal.png'
    else:
        return 'medio.png'
    
def alert_color_zona(zona_especial):
    if zona_especial.lower() == 'si':
        return 'red'
    else:
        return 'default'
    