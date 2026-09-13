from pathlib import Path

import firebird.driver as fb

db_path = Path(__file__).resolve().parent.parent / 'DB_DEV.FDB'
user = "SYSDBA"
password = "147369"  # Pon la contraseña que configuraste

try:
    con = fb.create_database(
        f"127.0.0.1/3050:{db_path}", 
        user=user, 
        password=password, 
        charset="UTF8"
    )
    print(f"¡Base de datos creada exitosamente en: {db_path}!")
    con.close()
except Exception as e:
    print(f"Error al crear la base de datos: {e}")