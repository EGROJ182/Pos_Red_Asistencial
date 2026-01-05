
def mapa2(dane_dpto, dane_municipios, prestadores_por_depto, prestadores_por_municipio, sedes_por_depto, reps_depto, prestadores_por_depto_reps, prestadores_por_municipio_reps, sedes_por_depto_reps, reps_depto_reps):
    dep_dict_mapa2 = {}
    for item in dane_dpto:
        dpto = item['departamento']
        dep_dict_mapa2[dpto] = {
            'prestadores': 0,
            'prestadores_reps': 0,
            'municipios': 0,
            'municipios_reps': 0,
            'dane': 0,
            'sedes': 0,
            'sedes_reps': 0,
            'reps_reps': 0
        }
    for item in prestadores_por_depto:
        dpto = item['departamento']
        if dpto in dep_dict_mapa2:
            dep_dict_mapa2[dpto]['prestadores'] = item['total']
    for item in prestadores_por_depto_reps:
        dpto = item['departamento']
        if dpto in dep_dict_mapa2:
            dep_dict_mapa2[dpto]['prestadores_reps'] = item['total']
    for item in prestadores_por_municipio:
        dpto = item['departamento']
        if dpto in dep_dict_mapa2:
            dep_dict_mapa2[dpto]['municipios'] = item['total']
    for item in prestadores_por_municipio_reps:
        dpto = item['departamento']
        if dpto in dep_dict_mapa2:
            dep_dict_mapa2[dpto]['municipios_reps'] = item['total']
    for item in dane_municipios:
        dpto = item['departamento']
        if dpto in dep_dict_mapa2:
            dep_dict_mapa2[dpto]['dane'] = item['total']
    for item in sedes_por_depto:
        dpto = item['departamento']
        if dpto in dep_dict_mapa2:
            dep_dict_mapa2[dpto]['sedes'] = item['total']
    for item in sedes_por_depto_reps:
        dpto = item['departamento']
        if dpto in dep_dict_mapa2:
            dep_dict_mapa2[dpto]['sedes_reps'] = item['total']
    for item in reps_depto:
        dpto = item['departamento']
        if dpto in dep_dict_mapa2:
            dep_dict_mapa2[dpto]['reps'] = item['total']
    for item in reps_depto_reps:
        dpto = item['departamento']
        if dpto in dep_dict_mapa2:
            dep_dict_mapa2[dpto]['reps_reps'] = item['total']
    
    return dep_dict_mapa2