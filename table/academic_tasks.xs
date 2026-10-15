table academic_tasks {
  description = "Tabela de tarefas acadêmicas vinculada às disciplinas"
  auth = false

  schema {
    int id {
      description = "Identificador único auto-incremental"
    }

    text title {
      description = "Título da tarefa ou obrigação acadêmica"
    }

    text description? {
      description = "Descrição detalhada da tarefa"
    }

    timestamp due_date? {
      description = "Data de entrega ou realização da tarefa"
    }

    text status {
      description = "Status da tarefa (ex: pendente, em andamento, concluída)"
    }

    int subject_id {
      table = "subjects"
      description = "Referência para a tabela subjects"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
  guid = "Zbfmd22N7DYQUK0mLOOXa7BzU1w"
}
