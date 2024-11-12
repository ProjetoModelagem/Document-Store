from pymongo import MongoClient

# Conexão com o MongoDB
mongo_client = MongoClient("info")
mongo_db = mongo_client["info"]

# Função para remover todas as coleções
def clear_all_collections():
    collections = mongo_db.list_collection_names()
    for collection_name in collections:
        mongo_db[collection_name].drop()
        print(f"A coleção '{collection_name}' foi removida com sucesso.")

clear_all_collections()

print("Todas as coleções foram limpas com sucesso.")
