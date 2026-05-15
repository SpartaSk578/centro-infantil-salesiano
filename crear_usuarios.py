import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centro_infantil_config.settings')
django.setup()

from usuarios.models import Usuario, Rol

admin_rol, _ = Rol.objects.get_or_create(nombre_rol='Administrador')
dir_rol, _ = Rol.objects.get_or_create(nombre_rol='Directora')
edu_rol, _ = Rol.objects.get_or_create(nombre_rol='Educadora')

usuarios = [
    ('admin', 'Admin123!', 'admin@centro.com', admin_rol),
    ('directora', 'Directora123!', 'directora@centro.com', dir_rol),
    ('educadora1', 'Educa123!', 'educadora1@centro.com', edu_rol),
    ('educadora2', 'Educa123!', 'educadora2@centro.com', edu_rol),
]

for nombre, password, email, rol in usuarios:
    if not Usuario.objects.filter(nombre_usuario=nombre).exists():
        u = Usuario(nombre_usuario=nombre, email=email, id_rol=rol)
        u.set_password(password)
        u.save()
        print(f"Creado: {nombre}")
    else:
        print(f"Ya existe: {nombre}")

print("Listo!")