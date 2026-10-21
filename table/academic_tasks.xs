// Tabela de tarefas acadêmicas vinculada às disciplinas
table academic_tasks {
  auth = false

  schema {
    // Identificador único auto-incremental
    int id
  
    // Título da tarefa ou obrigação acadêmica
    text title
  
    // Descrição detalhada da tarefa
    text description?
  
    // Data de entrega ou realização da tarefa
    timestamp due_date?
  
    // Status da tarefa (ex: pendente, em andamento, concluída)
    text status
  
    // Referência para a tabela subjects
    int subject_id {
      table = "subjects"
    }
  }

  index = [{type: "primary", field: [{name: "id"}]}]
  guid = "Zbfmd22N7DYQUK0mLOOXa7BzU1w"
}