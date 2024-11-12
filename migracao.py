from datetime import datetime
import psycopg2
from pymongo import MongoClient

# Conexão com o PostgreSQL
pg_conn = psycopg2.connect(
        database="info",
        user="info",
        password="info",
        host="info",
        port="info"
)
pg_cursor = pg_conn.cursor()

# Conexão com o MongoDB
mongo_client = MongoClient("info")
mongo_db = mongo_client["info"]


# Migrar alunos
def migrar_alunos():

    pg_cursor.execute("SELECT * FROM alunos;")
    alunos = pg_cursor.fetchall()
    for aluno in alunos:
        aluno_id = aluno[0]
        nome = aluno[1]
        email = aluno[2]
        data_nascimento = aluno[3].isoformat()
        data_matricula = aluno[4].isoformat()
        situacao_graduacao = aluno[5]

        # Obtem o historico escolar do aluno
        pg_cursor.execute("""
            SELECT he.disciplina_id, d.nome, he.semestre, he.ano, he.nota_final
            FROM historico_escolar he
            JOIN disciplinas d ON he.disciplina_id = d.id
            WHERE he.aluno_id = %s;
        """, (aluno_id,))

        historico = []

        for registro in pg_cursor.fetchall():

            historico.append({
                "disciplina_id": registro[0],
                "nome_disciplina": registro[1],
                "semestre": registro[2],
                "ano": registro[3],
                "nota_final": registro[4]
            })

        # Obtem informacoes do tcc, se tiver
        pg_cursor.execute("""
            SELECT grupo, professor_orientador_id
            FROM grupo_tcc
            WHERE aluno_id = %s;
        """, (aluno_id,))

        tcc_info = pg_cursor.fetchone()
        tcc_grupo = None
        if tcc_info:

            grupo_numero = tcc_info[0]
            orientador_id = tcc_info[1]

            # Obtem o nome do orientador
            pg_cursor.execute("SELECT nome FROM professores WHERE id = %s;", (orientador_id,))
            orientador_nome = pg_cursor.fetchone()[0]
            tcc_grupo = {
                "grupo_numero": grupo_numero,
                "orientador_id": orientador_id,
                "orientador_nome": orientador_nome
            }

        aluno_doc = {
            "_id": aluno_id,
            "nome": nome,
            "email": email,
            "data_nascimento": data_nascimento,
            "data_matricula": data_matricula,
            "situacao_graduacao": situacao_graduacao,
            "historico_escolar": historico,
            "tcc_grupo": tcc_grupo
        }

        # Insere no mongo
        mongo_db.alunos.insert_one(aluno_doc)

# migrar professores
def migrar_professores():

    pg_cursor.execute("SELECT * FROM professores;")
    professores = pg_cursor.fetchall()
    for professor in professores:
        professor_id = professor[0]
        nome = professor[1]
        email = professor[2]
        data_nascimento = professor[3].isoformat()
        data_contratacao = professor[4].isoformat()

        # Obtem o historico de disciplinas ministradas
        pg_cursor.execute("""
            SELECT hdp.disciplina_id, d.nome, hdp.semestre, hdp.ano
            FROM historico_disciplina_professores hdp
            JOIN disciplinas d ON hdp.disciplina_id = d.id
            WHERE hdp.professor_id = %s;
        """, (professor_id,))

        disciplinas_ministradas = []
        for registro in pg_cursor.fetchall():
            disciplinas_ministradas.append({
                "disciplina_id": registro[0],
                "nome_disciplina": registro[1],
                "semestre": registro[2],
                "ano": registro[3]
            })

        # Obtem o departamento e se o professor é chefe
        pg_cursor.execute("""
            SELECT d.id, d.nome, CASE WHEN pd.professor_id IS NOT NULL THEN true ELSE false END AS chefe
            FROM departamentos d
            LEFT JOIN professores_departamentos pd ON d.id = pd.departamento_id AND pd.professor_id = %s;
        """, (professor_id,))
        departamento = pg_cursor.fetchone()
        departamento_info = {
            "departamento_id": departamento[0],
            "nome": departamento[1],
            "chefe": departamento[2]
        }

        professor_doc = {
            "_id": professor_id,
            "nome": nome,
            "email": email,
            "data_nascimento": data_nascimento,
            "data_contratacao": data_contratacao,
            "disciplinas_ministradas": disciplinas_ministradas,
            "departamento": departamento_info
        }

        # Insere no Mongo
        mongo_db.professores.insert_one(professor_doc)

# Migrar cursos
def migrar_cursos():
    pg_cursor.execute("SELECT * FROM cursos;")

    cursos = pg_cursor.fetchall()
    for curso in cursos:
        curso_id = curso[0]
        nome = curso[1]

        # Busca todas as disciplinas
        pg_cursor.execute("SELECT id, nome FROM disciplinas;")
        matriz_curricular = []
        for registro in pg_cursor.fetchall():
            matriz_curricular.append({
                "disciplina_id": registro[0],
                "nome_disciplina": registro[1]
            })


        curso_doc = {
            "_id": curso_id,
            "nome": nome,
            "matriz_curricular": matriz_curricular
        }

        # Insere no Mongo
        mongo_db.cursos.insert_one(curso_doc)

# Migrar departamentos
def migrar_departamentos():
    pg_cursor.execute("SELECT * FROM departamentos;")
    departamentos = pg_cursor.fetchall()
    for departamento in departamentos:
        departamento_id = departamento[0]
        nome = departamento[1]

        # Obtem o chefe do departamento
        pg_cursor.execute("""
            SELECT p.id, p.nome
            FROM professores_departamentos pd
            JOIN professores p ON pd.professor_id = p.id
            WHERE pd.departamento_id = %s;
        """, (departamento_id,))

        chefe = pg_cursor.fetchone()
        chefe_info = {
            "chefe_departamento_id": chefe[0],
            "chefe_departamento_nome": chefe[1]
        } if chefe else None

        departamento_doc = {
            "_id": departamento_id,
            "nome": nome,
            "chefe_departamento": chefe_info
        }

        # Insere no Mongo
        mongo_db.departamentos.insert_one(departamento_doc)

# migrar disciplinas
def migrar_disciplinas():
    pg_cursor.execute("SELECT * FROM disciplinas;")
    disciplinas = pg_cursor.fetchall()
    for disciplina in disciplinas:
        disciplina_doc = {
            "_id": disciplina[0],
            "nome": disciplina[1]
        }
        # Insere no Mongo
        mongo_db.disciplinas.insert_one(disciplina_doc)

# Migrar grupos de TCC
def migrar_grupos_tcc():
    pg_cursor.execute("SELECT DISTINCT grupo FROM grupo_tcc;")
    grupos = pg_cursor.fetchall()
    for grupo in grupos:
        grupo_numero = grupo[0]

        # Obtem o orientador do grupo
        pg_cursor.execute("""
            SELECT DISTINCT p.id, p.nome
            FROM grupo_tcc gt
            JOIN professores p ON gt.professor_orientador_id = p.id
            WHERE gt.grupo = %s;
        """, (grupo_numero,))
        orientador = pg_cursor.fetchone()
        orientador_info = {
            "orientador_id": orientador[0],
            "orientador_nome": orientador[1]
        } if orientador else None

        # Obtem os alunos do grupo
        pg_cursor.execute("""
            SELECT a.id, a.nome
            FROM grupo_tcc gt
            JOIN alunos a ON gt.aluno_id = a.id
            WHERE gt.grupo = %s;
        """, (grupo_numero,))
        alunos = [{"aluno_id": aluno[0], "nome": aluno[1]} for aluno in pg_cursor.fetchall()]

        tcc_group_doc = {
            "_id": grupo_numero,
            "grupo_numero": grupo_numero,
            "orientador": orientador_info,
            "alunos": alunos
        }

        # Insere no Mongo
        mongo_db.grupos_tcc.insert_one(tcc_group_doc)

migrar_alunos()
migrar_professores()
migrar_cursos()
migrar_departamentos()
migrar_disciplinas()
migrar_grupos_tcc()

print("Migração concluída com sucesso!")
