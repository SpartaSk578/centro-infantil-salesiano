"""
Script para crear datos iniciales con conexiones familiares lógicas (Beneficiario -> Tutor -> Niño).
"""
import os
import django
import sys
from datetime import date

# Ajustar el path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centro_infantil_config.settings')
django.setup()

from usuarios.models import Rol, Usuario
from grupos.models import Grupo
from beneficiarios.models import Beneficiario, TutorPadre
from ninos.models import Nino

print("Configurando Roles y Usuarios...")
roles = {n: Rol.objects.get_or_create(nombre_rol=n)[0] for n in ['Administrador', 'Directora', 'Educadora']}
# (Usuarios omitidos aquí por brevedad pero se mantienen los existentes)

print("\nCreando Grupos...")
educadora1 = Usuario.objects.filter(nombre_usuario='educadora1').first()
grupos = {
    'Sala 1': Grupo.objects.get_or_create(nombre_grupo='Sala 1 (2 años)', defaults={'educador_responsable': educadora1})[0],
    'Sala 2': Grupo.objects.get_or_create(nombre_grupo='Sala 2 (3 años)', defaults={'educador_responsable': educadora1})[0],
}

print("\nGenerando Estructura Familiar (6 Familias)...")
familias = [
    {
        'madre': ('10001', 'Elena', 'Quispe', 'Mamani', '71111111'),
        'padre': ('20001', 'Ricardo', 'Quispe', 'Condori', '61111111'),
        'hijo': ('Sofia', 'Quispe', 'Quispe', date(2022, 5, 10), 'Sala 1')
    },
    {
        'madre': ('10002', 'Maria', 'Torrez', 'Luna', '72222222'),
        'padre': ('20002', 'Juan Carlos', 'Torrez', 'Vargas', '62222222'),
        'hijo': ('Mateo', 'Torrez', 'Torrez', date(2021, 2, 15), 'Sala 2')
    },
    {
        'madre': ('10003', 'Rosa', 'Mamani', 'Flores', '73333333'),
        'padre': ('20003', 'Pedro', 'Mamani', 'Roca', '63333333'),
        'hijo': ('Lucia', 'Mamani', 'Mamani', date(2022, 11, 20), 'Sala 1')
    },
    {
        'madre': ('10004', 'Ana', 'Condori', 'Paz', '74444444'),
        'padre': ('20004', 'Luis', 'Condori', 'Lima', '64444444'),
        'hijo': ('Andres', 'Condori', 'Condori', date(2020, 1, 30), 'Sala 2')
    },
    {
        'madre': ('10005', 'Carmen', 'Lima', 'Sosa', '75555555'),
        'padre': ('20005', 'Fernando', 'Lima', 'Choque', '65555555'),
        'hijo': ('Valentina', 'Lima', 'Lima', date(2022, 7, 5), 'Sala 1')
    },
    {
        'madre': ('10006', 'Sonia', 'Vargas', 'Rios', '76666666'),
        'padre': ('20006', 'Marcos', 'Vargas', 'Guzman', '66666666'),
        'hijo': ('Thiago', 'Vargas', 'Vargas', date(2021, 9, 12), 'Sala 2')
    }
]

registrador = Usuario.objects.filter(nombre_usuario='directora').first()

for f in familias:
    # 1. Crear Madre (Beneficiaria)
    m_ci, m_nom, m_ap, m_am, m_tel = f['madre']
    ben, _ = Beneficiario.objects.update_or_create(
        CI_beneficiario=m_ci,
        defaults={
            'nombres': m_nom, 'apellido_paterno': m_ap, 'apellido_materno': m_am,
            'contacto': m_tel, 'direccion': 'Zona Central, Calle 1'
        }
    )
    print(f"  [OK] Beneficiaria: {m_nom} {m_ap}")

    # 2. Crear Padre (Tutor Secundario)
    p_ci, p_nom, p_ap, p_am, p_tel = f['padre']
    TutorPadre.objects.update_or_create(
        CI_tutor=p_ci,
        defaults={
            'nombres': p_nom, 'apellido_paterno': p_ap, 'apellido_materno': p_am,
            'contacto': p_tel, 'beneficiario': ben
        }
    )
    print(f"  [OK] Tutor: {p_nom} {p_ap}")

    # 3. Crear Hijo/a
    h_nom, h_ap, h_am, h_fn, h_sala = f['hijo']
    h_full_ap = f"{h_ap} {h_am}"
    Nino.objects.update_or_create(
        nombres=h_nom, apellido_paterno=h_ap, apellido_materno=h_am,
        defaults={
            'apellidos': h_full_ap,
            'fecha_nacimiento': h_fn,
            'fecha_ingreso': date.today(),
            'CI_beneficiario': ben,
            'id_grupo': grupos[h_sala],
            'registrado_por': registrador
        }
    )
    print(f"  [OK] Niño/a: {h_nom} {h_ap}")

print("\n[FIN] Base de datos poblada con 6 familias completas y conectadas.")
