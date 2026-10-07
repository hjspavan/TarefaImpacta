// Definição do esquema da tabela subjects no Xano
table subjects {
  description = "Tabela de disciplinas vinculada aos usuários autenticados"

  schema {
    int id {
      description = "Identificador único auto-incremental"
    }

    text name {
      description = "Nome da disciplina"
    }

    text teacher {
      description = "Nome do professor responsável"
    }

    int hours {
      description = "Carga horária da disciplina"
    }

    int user_id {
      dbtable = "user"
      description = "Chave estrangeira para a tabela de autenticação do Xano (user/users)"
    }
  }
}

