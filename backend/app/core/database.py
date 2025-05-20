from supabase import create_client, Client
from dotenv import load_dotenv
import os 

load_dotenv()

KEY = os.getenv("SUPABASE_KEY")
URL = os.getenv("SUPABASE_URL")

Supabase: Client = create_client(URL, KEY)

def get_supabase_client() -> Client:
    return Supabase



# Supabase.table('roles').insert(({'name': 'admin', 'description':'idk xd'})).execute()




#para quemar datos a una base de datos es 
# Supabase.table('nombre_tabla').insert({'columna1': 'valor1', 'columna2': 'valor2'}).execute()

#para actualizar datos a una base de datos es
# Supabase.table('nombre_tabla').update({'columna1': 'valor1', 'columna2': 'valor2'}).eq('columna_id', 'id').execute()

#para eliminar datos a una base de datos es
# Supabase.table('nombre_tabla').delete().eq('columna_id', 'id').execute()

#para obtener datos a una base de datos es
# Supabase.table('nombre_tabla').select('*').execute()



