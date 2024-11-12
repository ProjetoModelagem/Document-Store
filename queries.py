from pymongo import MongoClient

# Conexão com o MongoDB
mongo_client = MongoClient("info")
mongo_db = mongo_client["info"]

# Query que resolve o 1
def historico_escolar_aleatorio():
    aluno = mongo_db.alunos.aggregate([{"$sample": {"size": 1}}]).next()
    aluno_id = aluno["_id"]
    historico = aluno.get("historico_escolar", [])

    print(f"\nHistórico escolar de {aluno['nome']}:")
    for record in historico:
        disciplina = mongo_db.disciplinas.find_one({"_id": record["disciplina_id"]})
        if disciplina:
            print(f"Código: {record['disciplina_id']}, Nome: {disciplina['nome']}, Semestre: {record['semestre']}, Ano: {record['ano']}, Nota Final: {record['nota_final']}")
        else:
            print(f"Código: {record['disciplina_id']} - Disciplina não encontrada")

historico_escolar_aleatorio()


# Query que resolve o 2
def historico_professor_aleatorio():
    professor = mongo_db.professores.aggregate([{"$sample": {"size": 1}}]).next()
    professor_id = professor["_id"]
    historico = professor.get("disciplinas_ministradas", [])

    print(f"\nHistórico de disciplinas ministradas por {professor['nome']}:")
    for record in historico:
        disciplina = mongo_db.disciplinas.find_one({"_id": record["disciplina_id"]})
        if disciplina:
            print(f"Disciplina: {disciplina['nome']}, Semestre: {record['semestre']}, Ano: {record['ano']}")
        else:
            print(f"Código: {record['disciplina_id']} - Disciplina não encontrada")


historico_professor_aleatorio()


# Query que resolve o 3
def lista_alunos_graduados(semestre, ano):
    print(f"\nAlunos formados no semestre {semestre} do ano {ano}:")
    alunos = mongo_db.alunos.find({"situacao_graduacao": True})
    for aluno in alunos:
        historico = aluno.get("historico_escolar", [])

        #verifica se o aluno possui todas as disciplinas aprovadas no semestre e ano fornecidos
        disciplinas_aprovadas = [disciplina for disciplina in historico if disciplina["semestre"] == semestre and disciplina["ano"] == ano and disciplina["nota_final"] >= 6.0]
        if disciplinas_aprovadas:
            print(f"- {aluno['nome']}")


lista_alunos_graduados(1, 2024)

# Query que resolve o 4
def lista_chefe_departamento():
    departamentos = mongo_db.departamentos.find()
    print("\nProfessores que são chefes de departamento:")
    for departamento in departamentos:
        chefe = departamento.get("chefe_departamento")
        if chefe:
            print(f"Departamento: {departamento['nome']}, Chefe: {chefe['chefe_departamento_nome']}")


lista_chefe_departamento()

# Query que resolve o 5
def info_grupo_tcc(group_num):
    tcc_group = mongo_db.grupos_tcc.find_one({"grupo_numero": group_num})
    if not tcc_group:
        print("Grupo de TCC não encontrado.")
        return

    print(f"\nGrupo de TCC número {group_num}:\n")
    print(f"Orientador: {tcc_group['orientador']['orientador_nome']}")
    print("\nAlunos:")
    for aluno in tcc_group["alunos"]:
        print(f"- {aluno['nome']}")


info_grupo_tcc(1)
