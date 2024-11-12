## Integrantes do Grupo
- **Guilherme de Abreu** - Matrícula: 22.222.028-7

## Projeto do semestre passado

- [Projeto](https://github.com/GuizinhoAB/Modelo-de-Banco-de-Dados/tree/main)

## Descrição do Projeto
Este projeto faz a migração de dados de um banco de dados PostgreSQL para um banco de dados NoSQL, o MongoDB. Ele pega as informações de alunos, professores, cursos, departamentos, disciplinas e grupos de TCC e as insere em coleções no MongoDB.


## Como Executar o Código

1. **Instalar Dependências:**
   - Para este projeto, recomendo usar a versão do Python 3.12, pois o `psycopg2` pode apresentar problemas com o Python 3.13.
   - Antes de executar o código, instale as bibliotecas necessárias com o seguinte comando:
     ```bash
     pip install psycopg2 pymongo
     ```

2. **Configurar o PostgreSQL e o MongoDB:**
   - **PostgreSQL**: Certifique-se de que o seu banco de dados PostgreSQL está funcionando corretamente. O uso do pgAdmin (instalado com o PostgreSQL) é recomendado para gerenciar o banco de dados.
   - **MongoDB**: Garanta que o MongoDB esteja instalado e em execução na porta padrão (`localhost:27017`). O MongoDB Compass é uma boa opção para visualizar os dados.
   - Para iniciar o MongoDB, use o comando:
     ```bash
     mongod
     ```

3. **Rodar o Script:**
   - Se quiser limpar as coleções no MongoDB, execute:
     ```bash
     python limpeza.py
     ```

   - Primeiro, popule o banco de dados relacional PostgreSQL:
     ```bash
     python criacao_tabela.py
     python data_generator.py
     ```

   - Em seguida, execute os scripts no terminal para criar, migrar e realizar as queries:
     ```bash
     python criacao_colecao.py
     python migracao.py
     python queries.py
     ```

## Queries para a Criação das Coleções Necessárias

- As queries estão no arquivo **criacao_colecao.py**.

## Código Desenvolvido para Extrair os Dados do Banco Relacional

- O script de migração está no arquivo **migracao.py**.

## Queries que Resolvem os 5 Itens

- As queries necessárias para resolver os itens especificados estão no arquivo **queries.py**.

## Validação das Queries

- Para garantir que os dados foram migrados corretamente, recomendo usar um cliente do MongoDB, como o MongoDB Compass, para verificar as coleções criadas.


### Coleções Criadas
1. **alunos**: Armazena as informações dos alunos, como nome, email, data de nascimento, data de matrícula, situação de graduação, histórico escolar e informações de TCC.
2. **professores**: Guarda os dados dos professores, como nome, email, data de nascimento, data de contratação, histórico de disciplinas ministradas e informações sobre o departamento que chefiam (se for o caso).
3. **cursos**: Contém os cursos disponíveis e suas respectivas matrizes curriculares.
4. **departamentos**: Registra os departamentos da instituição, incluindo informações sobre o chefe do departamento.
5. **disciplinas**: Lista as disciplinas disponíveis.
6. **grupos_tcc**: Registra os grupos de TCC, com o orientador e os alunos que fazem parte do grupo.


## Descrição das Coleções

1. alunos
```json
{
  "_id": 1,
  "nome": "Olívia Silveira",
  "email": "vitoria82@example.org",
  "data_nascimento": "2001-08-20",
  "data_matricula": "2021-10-22",
  "situacao_graduacao": false,
  "historico_escolar": [
    {
      "disciplina_id": 1,
      "nome_disciplina": "Físico nuclear",
      "semestre": 5,
      "ano": 2024,
      "nota_final": 2.78
    },
    // ...
    {
      "disciplina_id": 100,
      "nome_disciplina": "Oceanógrafo",
      "semestre": 6,
      "ano": 2022,
      "nota_final": 1.01
    }
  ],
  "tcc_grupo": {
    "grupo_numero": 8,
    "orientador_id": 41,
    "orientador_nome": "Hellena Cavalcanti"
  }
}
```

2. professores
``` json
{
  "nome": "Giovanna Moreira",
  "email": "caleb26@example.net",
  "data_nascimento": "1992-07-08",
  "data_contratacao": "2018-07-28",
  "disciplinas_ministradas": [
    {
      "disciplina_id": 63,
      "nome_disciplina": "Radialista",
      "semestre": 2,
      "ano": 2023
    },
    {
      "disciplina_id": 99,
      "nome_disciplina": "Escritor",
      "semestre": 2,
      "ano": 2019
    }
  ],
  "departamento": {
    "departamento_id": 1,
    "nome": "Matemática e Estatística",
    "chefe": false
  }
}

```

3. cursos
``` json
{
  "nome": "Pneumologista",
  "matriz_curricular": [
    {
      "disciplina_id": 1,
      "nome_disciplina": "Físico nuclear"
    },
    {
      "disciplina_id": 2,
      "nome_disciplina": "Cartazeiro"
    }
    // ...
  
  ]
}
```

4. departamentos
``` json
{
  "_id": 1,
  "nome": "Matemática e Estatística",
  "chefe_departamento": {
    "chefe_departamento_id": 45,
    "chefe_departamento_nome": "Larissa Santos"
  }
}
```

5. disciplinas
``` json
{
  "nome": "Físico nuclear"
}
```



6. grupos_tcc
``` json
{
  "_id": 9,
  "grupo_numero": 9,
  "orientador": {
    "orientador_id": 36,
    "orientador_nome": "Cauã Aparecida"
  },
  "alunos": [
    {
      "aluno_id": 20,
      "nome": "João Vitor Montenegro"
    },
    {
      "aluno_id": 38,
      "nome": "Pietra da Cunha"
    },
    // ...
  ]
}
```

