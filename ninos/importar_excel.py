"""
Lógica de importación del Excel OFPROBOL al sistema.
Se importa desde ninos/views.py
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
    'LACTANTES': 'LACTANTES',
    'LACTANTE':  'LACTANTES',
    'INFANTE I': 'INFANTE I',
    'INFANTE II A': 'INFANTE II A',
    'INFANTE IIA':  'INFANTE II A',
    'INFANTE II B': 'INFANTE II B',
    'INFANTE IIB':  'INFANTE II B',
    'INFANTE II':   'INFANTE II A',  # fallback genérico
}

CARRERA_MAP = {
    'CONTADURIA GENERAL':          'CONTADURIA_GENERAL',
    'CONTADURÍA GENERAL':          'CONTADURIA_GENERAL',
    'ADMINISTRACION DE EMPRESAS':  'ADMINISTRACION_EMPRESAS',
    'ADMINISTRACIÓN DE EMPRESAS':  'ADMINISTRACION_EMPRESAS',
    'ADMINISTRACIÓN DE EMORESAS':  'ADMINISTRACION_EMPRESAS',
    'ADMINISTRACION DE EMORESAS':  'ADMINISTRACION_EMPRESAS',
    'SISTEMAS COMPUTACIONALES':    'SISTEMAS_COMPUTACIONALES',
    'EDUCACION':                   'EDUCACION',
    'EDUCACIÓN':                   'EDUCACION',
    'ENFERMERIA':                  'ENFERMERIA',
    'ENFERMERÍA':                  'ENFERMERIA',
    'INGENIERIA CIVIL':            'INGENIERIA_CIVIL',
    'INGENIERÍA CIVIL':            'INGENIERIA_CIVIL',
    'INGENIERIA INDUSTRIAL':       'INGENIERIA_INDUSTRIAL',
    'INGENIERÍA INDUSTRIAL':       'INGENIERIA_INDUSTRIAL',
    'MECANICA INDUSTRIAL':         'INGENIERIA_INDUSTRIAL',
    'MECÁNICA INDUSTRIAL':         'INGENIERIA_INDUSTRIAL',
    'MECANICA AUTOMOTRIZ':         'INGENIERIA_INDUSTRIAL',
    'PSICOLOGIA':                  'PSICOLOGIA',
    'PSICOLOGÍA':                  'PSICOLOGIA',
    'DERECHO':                     'DERECHO',
    'INGLES':                      'INGLES',
    'INGLÉS':                      'INGLES',
    'SECRETARIADO':                'SISTEMAS_COMPUTACIONALES',  # más cercano
    'ARTES GRAFICAS':              'SISTEMAS_COMPUTACIONALES',
    'ARTES GRÁFICAS':              'SISTEMAS_COMPUTACIONALES',
    'ELECTRICIDAD INDUSTRIAL':     'INGENIERIA_INDUSTRIAL',
}

TURNO_MAP = {
    'MAÑANA':  'MANANA',
    'MANANA':  'MANANA',
    'MAÃANA':  'MANANA',
    'TARDE':   'TARDE',
    'NOCHE':   'NOCHE',
}

CARRERA_CHOICES_KEYS = {v for v, _ in CARRERA_CHOICES}


def _limpiar(val):
    """Devuelve string limpio o vacío."""
    if val is None:
        return ''
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
    n = _normalizar(raw)
    return TURNO_MAP.get(n, None)


def _mapear_carrera(raw):
    n = _normalizar(raw)
    # Búsqueda exacta
    if n in CARRERA_MAP:
        return CARRERA_MAP[n]
    # Búsqueda parcial
    for k, v in CARRERA_MAP.items():
        if k in n or n in k:
            return v
    # Si el valor ya es una clave válida, se devuelve
    if n in CARRERA_CHOICES_KEYS:
        return n
    return 'OTRO'


def _es_itdb(ocupacion_raw):
    """Determina si el tutor es estudiante ITDB."""
    n = _normalizar(ocupacion_raw)
    return 'ITDB' in n or 'ESTUDIANTE ITDB' in n


def _parse_fecha(val):
    """Intenta parsear varios formatos de fecha."""
    if isinstance(val, (datetime,)):
        return val.date()
    if isinstance(val, date):
        return val
    s = _limpiar(val)
    # Intentar formatos comunes
    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%d/%m/%y'):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            pass
    # Extraer fecha si hay texto extra: "1 5/02/2021"
    m = re.search(r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})', s)
    if m:
        try:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if y < 100:
                y += 2000
            return date(y, mo, d)
        except Exception:
            pass
    return None


def _parse_contacto(val):
    """Limpia y valida teléfono (solo dígitos, max 15)."""
    if val is None:
        return ''
    s = re.sub(r'\D', '', str(val))
    return s[:15]


def _extraer_partes_nombre(nombre_completo):
    """
    Intenta separar: APELLIDO_PAT APELLIDO_MAT NOMBRES
    o bien NOMBRES APELLIDO_PAT APELLIDO_MAT según el orden.
    El Excel tiene el nombre del tutor en una sola celda, sin estructura garantizada.
    Devuelve (nombres, ap_pat, ap_mat).
    """
    partes = _normalizar(nombre_completo).split()
    if not partes:
        return ('SIN NOMBRE', '', '')
    if len(partes) == 1:
        return (partes[0], '', '')
    if len(partes) == 2:
        return (partes[0], partes[1], '')
    # Heurística: si hay prefijos como "TUTORA", descartarlos
    if partes[0] in ('TUTORA', 'TUTOR', 'DR', 'DRA', 'LIC'):
        partes = partes[1:]
    # Asumimos: NOMBRES (1 o más) + AP_PAT + AP_MAT
    # Como los apellidos del niño están en otras columnas, aquí tomamos
    # primer apellido = -2, segundo apellido = -1, nombre = resto
    if len(partes) >= 3:
        ap_mat = partes[-1]
        ap_pat = partes[-2]
        nombres = ' '.join(partes[:-2])
    else:
        ap_pat = partes[-1]
        ap_mat = ''
        nombres = ' '.join(partes[:-1])
    return (nombres, ap_pat, ap_mat)


def _generar_ci_temporal(nombres, ap_pat, contacto):
    """
    Genera un CI temporal para tutores externos que no tienen CI en el Excel.
    Formato: IMP-<iniciales><telefono_parcial>
    """
    iniciales = ''
    for p in [ap_pat, nombres]:
        if p:
            iniciales += p[0]
    tel = contacto[:6] if contacto else '000000'
    return f"IMP-{iniciales}{tel}".upper()[:15]


def procesar_excel(filepath, usuario):
    """
    Lee el Excel y retorna:
      - resultados: list[dict] con estado de cada fila
      - stats: dict con conteos
    No hace commit hasta que se confirme.
    """
    try:
        wb = openpyxl.load_workbook(filepath)
    except Exception as e:
        return None, None, f"No se pudo abrir el archivo: {e}"

    ws = wb.active
    resultados = []
    stats = {'creados': 0, 'existentes': 0, 'errores': 0, 'tutores_creados': 0}

    for row_idx, row in enumerate(ws.iter_rows(min_row=4, values_only=True), start=4):
        # Ignorar filas completamente vacías
        if all(v is None for v in row):
            continue

        # Columnas: Nº | AP_PAT | AP_MAT | NOMBRES | SEXO | FEC_NAC | AÑO | MESES | SALA | TUTOR | OCUPACION | CARRERA | AÑO_SEM | TURNO | CELULAR
        (nro, ap_pat_nino, ap_mat_nino, nombres_nino, sexo_raw,
         fec_nac_raw, _, _, sala_raw,
         nombre_tutor, ocupacion_raw, carrera_raw, anio_sem, turno_raw, celular_raw) = row

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
            # ── Validaciones básicas del niño ──
            if not nombres_nino:
                raise ValueError("Falta el nombre del niño")

            fecha_nac = _parse_fecha(fec_nac_raw)
            if fecha_nac is None:
                fila_info['advertencias'].append(f"Fecha de nacimiento no reconocida ({fec_nac_raw!r}), se dejará vacía")

            sala = _mapear_sala(sala_raw)
            if not sala:
                fila_info['advertencias'].append(f"Sala no reconocida ({sala_raw!r})")

            sexo = _normalizar(sexo_raw)
            if sexo not in ('M', 'F'):
                fila_info['advertencias'].append(f"Sexo no reconocido ({sexo_raw!r}), se usará 'M'")
                sexo = 'M'

            # ── Procesar tutor ──
            contacto = _parse_contacto(celular_raw)
            es_itdb = _es_itdb(ocupacion_raw)
            fila_info['es_itdb'] = es_itdb

            tutor_obj = None
            beneficiario_obj = None

            if es_itdb:
                # Es Beneficiario (estudiante ITDB)
                carrera_key = _mapear_carrera(carrera_raw)
                turno_key = _mapear_turno(turno_raw)
                anio_sem_str = _normalizar(anio_sem)
                ocupacion_extra = _normalizar(ocupacion_raw)

                # CI temporal basado en nombre+teléfono
                noms_t, ap_p_t, ap_m_t = _extraer_partes_nombre(nombre_tutor)
                ci_temp = _generar_ci_temporal(noms_t, ap_p_t, contacto)

                # Buscar por teléfono o CI temporal
                b_existente = None
                if contacto:
                    b_existente = Beneficiario.objects.filter(contacto=contacto).first()
                if not b_existente:
                    b_existente = Beneficiario.objects.filter(CI_beneficiario=ci_temp).first()

                if b_existente:
                    beneficiario_obj = b_existente
                    fila_info['advertencias'].append(f"Tutor IDS ya existía: {b_existente.get_full_name()}")
                else:
                    noms, ap_p, ap_m = _extraer_partes_nombre(nombre_tutor)
                    beneficiario_obj = Beneficiario(
                        CI_beneficiario=ci_temp,
                        nombres=noms or 'SIN NOMBRE',
                        apellido_paterno=ap_p or 'S/N',
                        apellido_materno=ap_m,
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
                    fila_info['advertencias'].append(f"Tutor IDS creado con CI temporal: {ci_temp}")

            else:
                # Es TutorPadre (externo)
                contacto_busca = contacto
                t_existente = None
                if contacto_busca:
                    t_existente = TutorPadre.objects.filter(contacto=contacto_busca).first()

                if t_existente:
                    tutor_obj = t_existente
                    fila_info['advertencias'].append(f"Tutor externo ya existía: {t_existente.get_full_name()}")
                else:
                    noms_t, ap_p_t, ap_m_t = _extraer_partes_nombre(nombre_tutor)
                    ci_temp = _generar_ci_temporal(noms_t, ap_p_t, contacto)
                    noms, ap_p, ap_m = _extraer_partes_nombre(nombre_tutor)
                    ocupacion_extra = _normalizar(ocupacion_raw)
                    tutor_obj = TutorPadre(
                        CI_tutor=ci_temp,
                        nombres=noms or 'SIN NOMBRE',
                        apellido_paterno=ap_p or 'S/N',
                        apellido_materno=ap_m,
                        ocupacion='OTRO',
                        ocupacion_especifica=ocupacion_extra[:100] if ocupacion_extra else '',
                        contacto=contacto,
                        registrado_por=usuario,
                    )
                    tutor_obj.save()
                    stats['tutores_creados'] += 1
                    fila_info['advertencias'].append(f"Tutor externo creado con CI temporal: {ci_temp}")

            # ── Verificar si el niño ya existe ──
            nino_existe = Nino.objects.filter(
                nombres__iexact=_normalizar(nombres_nino),
                apellido_paterno__iexact=_normalizar(ap_pat_nino or ''),
            ).first()

            if nino_existe:
                fila_info['estado'] = 'existente'
                fila_info['mensaje'] = f"Ya registrado (ID {nino_existe.pk})"
                stats['existentes'] += 1
            else:
                # Buscar el grupo que coincida con la sala
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
                    sexo=sexo,
                    fecha_nacimiento=fecha_nac or date.today(),
                    fecha_ingreso=date.today(),
                    sala=sala,
                    id_grupo=grupo_obj,
                    CI_beneficiario=beneficiario_obj,
                    CI_tutor_padre=tutor_obj,
                    registrado_por=usuario,
                )
                nino.save()
                fila_info['estado'] = 'creado'
                fila_info['mensaje'] = f"Niño creado exitosamente (ID {nino.pk})"
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

        # Guardar temporalmente en memoria
        import tempfile, os
        suffix = '.xlsx'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
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

        contexto.update({
            'resultados': resultados,
            'stats': stats,
            'procesado': True,
        })
        return render(request, 'ninos/importar_excel.html', contexto)

    return render(request, 'ninos/importar_excel.html', contexto)