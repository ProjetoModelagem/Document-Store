from pymongo import MongoClient

# Conexão com o MongoDB
mongo_client = MongoClient("info")
mongo_db = mongo_client["info"]

# Criar as colecoes no MongoDB
mongo_db.create_collection("alunos")
mongo_db.create_collection("cursos")
mongo_db.create_collection("departamentos")
mongo_db.create_collection("disciplinas")
mongo_db.create_collection("grupos_tcc")
mongo_db.create_collection("professores")

print("Coleções criadas com sucesso!")

