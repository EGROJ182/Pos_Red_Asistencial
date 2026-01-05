#!/usr/bin/env python
"""
Script para generar información automática del proyecto Django
Ejecuta: python generate_project_info.py
"""

import sys
import subprocess
import pkg_resources
import django
import json
from pathlib import Path

def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def get_django_version():
    return django.get_version()

def get_installed_packages():
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}

def get_npm_packages():
    try:
        package_json = Path('package.json')
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)
                return data.get('dependencies', {}), data.get('devDependencies', {})
    except:
        pass
    return {}, {}

def generate_readme_versions():
    print("🔍 Recopilando información del proyecto...\n")
    
    # Python y Django
    python_version = get_python_version()
    django_version = get_django_version()
    
    print(f"✅ Python: {python_version}")
    print(f"✅ Django: {django_version}")
    
    # Paquetes Python importantes
    packages = get_installed_packages()
    important_packages = [
        'djangorestframework',
        'psycopg2',
        'pillow',
        'celery',
        'redis',
        'gunicorn',
        'whitenoise',
        'django-cors-headers',
        'python-decouple',
        'django-allauth'
    ]
    
    print("\n📦 Paquetes Python detectados:")
    found_packages = {}
    for pkg in important_packages:
        if pkg in packages:
            found_packages[pkg] = packages[pkg]
            print(f"   • {pkg}: {packages[pkg]}")
    
    # Paquetes NPM
    npm_deps, npm_dev_deps = get_npm_packages()
    if npm_deps or npm_dev_deps:
        print("\n📦 Paquetes NPM detectados:")
        for pkg, version in npm_deps.items():
            print(f"   • {pkg}: {version}")
    
    # Generar sección de README
    readme_section = f"""
## 🛠️ Tecnologías y Versiones

### Backend
- **Python**: {python_version}
- **Django**: {django_version}
"""
    
    if found_packages:
        readme_section += "\n### Dependencias principales:\n"
        for pkg, version in found_packages.items():
            readme_section += f"- **{pkg}**: {version}\n"
    
    if npm_deps:
        readme_section += "\n### Frontend\n"
        for pkg, version in npm_deps.items():
            readme_section += f"- **{pkg}**: {version}\n"
    
    # Guardar en archivo
    with open('PROJECT_INFO.md', 'w', encoding='utf-8') as f:
        f.write(readme_section)
    
    print("\n✅ Información guardada en PROJECT_INFO.md")
    print("   Copia esta sección a tu README.md")
    
    return readme_section

if __name__ == "__main__":
    try:
        info = generate_readme_versions()
        print("\n" + "="*50)
        print(info)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)