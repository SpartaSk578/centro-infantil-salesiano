"""
Importación del Excel OFPROBOL 2025/2026 al sistema.
Columnas (fila 4):
 1=Nº  2=AP_PAT  3=AP_MAT  4=NOMBRES  5=SEXO  6=FEC_NAC  7=AÑO  8=MESES
 9=CI_NINO  10=DIRECCIÓN  11=PESO  12=TALLA  13=VACUNAS  14=SALA
 15=NOMBRE_TUTOR  16=CI_TUTOR  17=NRO_REGISTRO_ITDB  18=OCUPACION
 19=CARRERA  20=AÑO_SEM  21=TURNO  22=EDAD  23=CELULAR  24=(vacío)
"""

import openpyxl
import re
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from beneficiarios.models import Beneficiario, TutorPadre, CARRERA_CHOICES, TURNO_CHOICES
from ninos.models import Nino


# ─── MAPEOS ───────────────────────────────────────────────────────────────────
SALA_MAP = {
    'LACTANTES':    'LACTANTES',
    'LACTANTE':     'LACTANTES',
    'INFANTE I':    'INFANTE I',
    'INFANTE II A': 'INFANTE II A',
    'INFANTE IIA':  'INFANTE II A',
    'INFANTE II B': 'INFANTE II B',
    'INFANTE IIB':  'INFANTE II B',
    'INFANTE II':   'INFANTE II A',
}

CARRERA_MAP = {
    'CONTADURIA GENERAL':         'CONTADURIA_GENERAL',
    'CONTADURÍA GENERAL':         'CONTADURIA_GENERAL',
    'ADMINISTRACION DE EMPRESAS': 'ADMINISTRACION_EMPRESAS',
    'ADMINISTRACIÓN DE EMPRESAS': 'ADMINISTRACION_EMPRESAS',
    'SISTEMAS COMPUTACIONALES':   'SISTEMAS_COMPUTACIONALES',
    'EDUCACION':                  'EDUCACION',
    'EDUCACIÓN':                  'EDUCACION',
    'ENFERMERIA':                 'ENFERMERIA',
    'ENFERMERÍA':                 'ENFERMERIA',
    'INGENIERIA CIVIL':           'INGENIERIA_CIVIL',
    'INGENIERÍA CIVIL':           'INGENIERIA_CIVIL',
    'INGENIERIA INDUSTRIAL':      'INGENIERIA_INDUSTRIAL',
    'INGENIERÍA INDUSTRIAL':      'INGENIERIA_INDUSTRIAL',
    'PSICOLOGIA':                 'PSICOLOGIA',
    'PSICOLOGÍA':                 'PSICOLOGIA',
    'DERECHO':                    'DERECHO',
    'INGLES':                     'INGLES',
    'INGLÉS':                     'INGLES',
}

TURNO_MAP = {
    'MAÑANA': 'MANANA', 'MANANA': 'MANANA', 'TARDE': 'TARDE', 'NOCHE': 'NOCHE',
}

CARRERA_CHOICES_KEYS = {v for v, _ in CARRERA_CHOICES}


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def _limpiar(val):
    if val is None: return ''
    return str(val).strip()

def _normalizar(val):
    return _limpiar(val).upper()

def _mapear_sala(raw):
    n = _normalizar(raw)
    for k, v in SALA_MAP.items():
        if k in n:
            return v
    return None

def _mapear_turno(raw):
    return TURNO_MAP.get(_normalizar(raw), None)

def _mapear_carrera(raw):
    n = _normalizar(raw)
    if n in CARRERA_MAP:
        return CARRERA_MAP[n]
    for k, v in CARRERA_MAP.items():
        if k in n or n in k:
            return v
    return 'OTRO'

def _es_itdb(ocupacion_raw, nro_registro_itdb):
    """Determina si el tutor es estudiante ITDB."""
    n = _normalizar(ocupacion_raw)
    if 'ITDB' in n or 'ESTUDIANTE ITDB' in n:
        return True
    if nro_registro_itdb and str(nro_registro_itdb).strip() not in ('', 'None'):
        return True
    return False

def _parse_fecha(val):
    if isinstance(val, datetime): return val.date()
    if isinstance(val, date): return val
    s = _limpiar(val)
    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%d/%m/%y'):
        try: return datetime.strptime(s, fmt).date()
        except: pass
    m = re.search(r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})', s)
    if m:
        try:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if y < 100: y += 2000
            return date(y, mo, d)
        except: pass
    return None

def _parse_contacto(val):
    if val is None: return ''
    s = re.sub(r'\D', '', str(val))
    return s[:15]

def _parse_peso(val):
    """Extrae peso en kg como float."""
    if val is None: return None
    s = str(val).strip().upper()
    if s in ('', 'FALTA', 'S/D', 'N/D', '-'): return None
    # "9,9 KILOS" -> 9.9
    m = re.search(r'(\d+)[,.](\d+)', s)
    if m: return float(f"{m.group(1)}.{m.group(2)}")
    m = re.search(r'(\d+)', s)
    if m: return float(m.group(1))
    return None

def _parse_talla(val):
    """Extrae talla en cm como float."""
    if val is None: return None
    s = str(val).strip().upper()
    if s in ('', 'FALTA', 'S/D', 'N/D', '-'): return None
    # "73cm" o "79,5cm" -> 73.0 / 79.5
    s = s.replace(',', '.')
    m = re.search(r'(\d+\.?\d*)', s)
    if m: return float(m.group(1))
    return None

def _parse_vacunas(val):
    s = _normalizar(val)
    return s in ('SI', 'SÍ', 'S', 'YES', 'Y', '1', 'TRUE', 'COMPLETAS')

def _extraer_partes_nombre(nombre_completo):
    partes = _normalizar(nombre_completo).split()
    if not partes: return ('SIN NOMBRE', '', '')
    if partes[0] in ('TUTORA', 'TUTOR', 'DR', 'DRA', 'LIC'): partes = partes[1:]
    if not partes: return ('SIN NOMBRE', '', '')
    if len(partes) == 1: return (partes[0], '', '')
    if len(partes) == 2: return (partes[0], partes[1], '')
    if len(partes) >= 3:
        ap_mat = partes[-1]
        ap_pat = partes[-2]
        nombres = ' '.join(partes[:-2])
        return (nombres, ap_pat, ap_mat)
    return (partes[0], '', '')

def _generar_ci_temporal(nombres, ap_pat, contacto):
    iniciales = ''
    for p in [ap_pat, nombres]:
        if p: iniciales += p[0]
    tel = contacto[:6] if contacto else '000000'
    return f"IMP-{iniciales}{tel}".upper()[:15]


# ─── PROCESAMIENTO PRINCIPAL ──────────────────────────────────────────────────
def procesar_excel(filepath, usuario):
    try:
        wb = openpyxl.load_workbook(filepath)
    except Exception as e:
        return None, None, f"No se pudo abrir el archivo: {e}"

    ws = wb.active
    resultados = []
    stats = {'creados': 0, 'existentes': 0, 'errores': 0, 'tutores_creados': 0}

    # Detectar fila de inicio de datos (buscar fila con "APELLIDO PATERNO" o primera fila con datos reales)
    fila_inicio = 5  # default
    for row_idx in range(1, 10):
        val = ws.cell(row_idx, 2).value
        if val and 'APELLIDO' in str(val).upper():
            fila_inicio = row_idx + 1
            break

    for row_idx, row in enumerate(ws.iter_rows(min_row=fila_inicio, values_only=True), start=fila_inicio):
        if all(v is None for v in row):
            continue

        # Desempaquetar las 24 columnas de forma segura
        row_list = list(row)
        # Rellenar si hay menos columnas
        while len(row_list) < 24:
            row_list.append(None)

        (nro, ap_pat_nino, ap_mat_nino, nombres_nino, sexo_raw,
         fec_nac_raw, anio_raw, meses_raw,
         ci_nino_raw, direccion_raw, peso_raw, talla_raw, vacunas_raw, sala_raw,
         nombre_tutor, ci_tutor_raw, nro_registro_itdb, ocupacion_raw,
         carrera_raw, anio_sem, turno_raw, edad_raw, celular_raw, _) = row_list[:24]

        # Saltar si no hay nombre de niño
        if not nombres_nino and not ap_pat_nino:
            continue

        fila_info = {
            'fila': row_idx,
            'nino': f"{_normalizar(ap_pat_nino)} {_normalizar(ap_mat_nino)} {_normalizar(nombres_nino)}".strip(),
            'tutor': _normalizar(nombre_tutor),
            'sala': _normalizar(sala_raw),
            'estado': '',
            'mensaje': '',
            'es_itdb': False,
            'advertencias': [],
        }

        try:
            if not nombres_nino:
                raise ValueError("Falta el nombre del niño")

            fecha_nac = _parse_fecha(fec_nac_raw)
            if fecha_nac is None:
                fila_info['advertencias'].append(f"Fecha no reconocida ({fec_nac_raw!r}), se usará hoy")

            sala = _mapear_sala(sala_raw)
            if not sala:
                fila_info['advertencias'].append(f"Sala no reconocida ({sala_raw!r})")

            sexo = _normalizar(sexo_raw)
            if sexo not in ('M', 'F'):
                sexo = 'M'

            # Datos nuevos del niño
            peso = _parse_peso(peso_raw)
            talla = _parse_talla(talla_raw)
            vacunas = _parse_vacunas(vacunas_raw)
            direccion = _limpiar(direccion_raw)
            ci_nino = _limpiar(ci_nino_raw)

            # Procesar tutor
            contacto = _parse_contacto(celular_raw)
            ci_tutor = _limpiar(ci_tutor_raw)
            nro_itdb = _limpiar(nro_registro_itdb)
            es_itdb = _es_itdb(ocupacion_raw, nro_registro_itdb)
            fila_info['es_itdb'] = es_itdb

            tutor_obj = None
            beneficiario_obj = None

            if es_itdb:
                carrera_key = _mapear_carrera(carrera_raw)
                turno_key = _mapear_turno(turno_raw)
                anio_sem_str = _normalizar(anio_sem)
                ocupacion_extra = _normalizar(ocupacion_raw)

                # Buscar por CI real del tutor, luego por celular, luego por CI temporal
                b_existente = None
                if ci_tutor and len(ci_tutor) > 3:
                    b_existente = Beneficiario.objects.filter(CI_beneficiario=ci_tutor).first()
                if not b_existente and contacto:
                    b_existente = Beneficiario.objects.filter(contacto=contacto).first()

                if b_existente:
                    beneficiario_obj = b_existente
                    fila_info['advertencias'].append(f"Tutor IDS ya existía: {b_existente.get_full_name()}")
                else:
                    noms_t, ap_p_t, ap_m_t = _extraer_partes_nombre(nombre_tutor or '')
                    # Usar CI real si está disponible, sino generar temporal
                    ci_key = ci_tutor if (ci_tutor and len(ci_tutor) > 3) else _generar_ci_temporal(noms_t, ap_p_t, contacto)
                    beneficiario_obj = Beneficiario(
                        CI_beneficiario=ci_key,
                        nombres=noms_t or 'SIN NOMBRE',
                        apellido_paterno=ap_p_t or 'S/N',
                        apellido_materno=ap_m_t,
                        ocupacion='ESTUDIANTE_ITDB',
                        ocupacion_especifica=ocupacion_extra[:100] if ocupacion_extra else '',
                        carrera=carrera_key,
                        anio_semestre=anio_sem_str[:50] if anio_sem_str else '',
                        turno=turno_key,
                        contacto=contacto,
                        registrado_por=usuario,
                    )
                    beneficiario_obj.save()
                    stats['tutores_creados'] += 1
                    fila_info['advertencias'].append(f"Tutor IDS creado: CI={ci_key}")

            else:
                t_existente = None
                if ci_tutor and len(ci_tutor) > 3:
                    t_existente = TutorPadre.objects.filter(CI_tutor=ci_tutor).first()
                if not t_existente and contacto:
                    t_existente = TutorPadre.objects.filter(contacto=contacto).first()

                if t_existente:
                    tutor_obj = t_existente
                    fila_info['advertencias'].append(f"Tutor externo ya existía: {t_existente.get_full_name()}")
                else:
                    noms_t, ap_p_t, ap_m_t = _extraer_partes_nombre(nombre_tutor or '')
                    ci_key = ci_tutor if (ci_tutor and len(ci_tutor) > 3) else _generar_ci_temporal(noms_t, ap_p_t, contacto)
                    ocupacion_extra = _normalizar(ocupacion_raw)
                    tutor_obj = TutorPadre(
                        CI_tutor=ci_key,
                        nombres=noms_t or 'SIN NOMBRE',
                        apellido_paterno=ap_p_t or 'S/N',
                        apellido_materno=ap_m_t,
                        ocupacion='OTRO',
                        ocupacion_especifica=ocupacion_extra[:100] if ocupacion_extra else '',
                        contacto=contacto,
                        registrado_por=usuario,
                    )
                    tutor_obj.save()
                    stats['tutores_creados'] += 1
                    fila_info['advertencias'].append(f"Tutor externo creado: CI={ci_key}")

            # Verificar duplicados
            nino_existe = Nino.objects.filter(
                nombres__iexact=_normalizar(nombres_nino),
                apellido_paterno__iexact=_normalizar(ap_pat_nino or ''),
            ).first()

            if nino_existe:
                fila_info['estado'] = 'existente'
                fila_info['mensaje'] = f"Ya registrado (ID {nino_existe.pk})"
                stats['existentes'] += 1
            else:
                # Buscar grupo por sala
                from grupos.models import Grupo
                grupo_obj = None
                if sala:
                    for g in Grupo.objects.all():
                        if _normalizar(sala) == _normalizar(g.nombre_grupo):
                            grupo_obj = g
                            break

                nino = Nino(
                    nombres=_normalizar(nombres_nino),
                    apellido_paterno=_normalizar(ap_pat_nino or ''),
                    apellido_materno=_normalizar(ap_mat_nino or ''),
                    ci_nino=ci_nino or None,
                    sexo=sexo,
                    fecha_nacimiento=fecha_nac or date.today(),
                    fecha_ingreso=date.today(),
                    direccion=direccion or None,
                    sala=sala,
                    id_grupo=grupo_obj,
                    peso_kg=peso,
                    talla_cm=talla,
                    vacunas_al_dia=vacunas,
                    CI_beneficiario=beneficiario_obj,
                    CI_tutor_padre=tutor_obj,
                    registrado_por=usuario,
                )
                nino.save()
                fila_info['estado'] = 'creado'
                fila_info['mensaje'] = f"Creado exitosamente (ID {nino.pk})"
                stats['creados'] += 1

        except Exception as e:
            fila_info['estado'] = 'error'
            fila_info['mensaje'] = str(e)
            stats['errores'] += 1

        resultados.append(fila_info)

    return resultados, stats, None


@login_required
def importar_excel_ninos(request):
    contexto = {'titulo': 'Importar Excel OFPROBOL'}

    if request.method == 'POST':
        archivo = request.FILES.get('archivo_excel')
        if not archivo:
            messages.error(request, 'Selecciona un archivo Excel (.xlsx)')
            return render(request, 'ninos/importar_excel.html', contexto)
        if not archivo.name.endswith('.xlsx'):
            messages.error(request, 'Solo se aceptan archivos .xlsx')
            return render(request, 'ninos/importar_excel.html', contexto)

        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            for chunk in archivo.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            resultados, stats, error = procesar_excel(tmp_path, request.user)
        finally:
            os.unlink(tmp_path)

        if error:
            messages.error(request, error)
            return render(request, 'ninos/importar_excel.html', contexto)

        contexto.update({'resultados': resultados, 'stats': stats, 'procesado': True})
        return render(request, 'ninos/importar_excel.html', contexto)

    return render(request, 'ninos/importar_excel.html', contexto)
