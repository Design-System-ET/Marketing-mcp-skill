import os

def sanitizar_nombre(nombre):
    return nombre.strip().replace('  ', ' ')

def listar_clientes(docs_dir=None):
    if docs_dir and os.path.isdir(docs_dir):
        return sorted([d for d in os.listdir(docs_dir) if os.path.isdir(os.path.join(docs_dir, d))])
    return ["MG Joyas"]