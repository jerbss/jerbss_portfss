import json
from django.core.management import call_command

def export_data():
    """Exporta os dados do SQLite para JSON"""
    call_command('dumpdata', '--natural-foreign', '--indent=2', output='data_dump.json')

def import_data():
    """Importa os dados do JSON para o Supabase"""
    call_command('loaddata', 'data_dump.json')

if __name__ == "__main__":
    export_data()
    # Após configurar o Supabase em settings.py, execute:
    # import_data()
