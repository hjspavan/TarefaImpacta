// Update cadastro record
query "cadastro/{cadastro_id}" verb=PUT {
  api_group = "decadastro"

  input {
    int cadastro_id? filters=min:1
    dblink {
      table = ""
    }
  }

  stack {
    db.edit "" {
      field_name = "id"
      field_value = $input.cadastro_id
      enforce_hidden_fields = false
      data = {nome: $input.nome, endeco: $input.endeco}
    } as $model
  }

  response = $model
  guid = "giGsEI1tdwqPevOzN3FAs8wJmRI"
}