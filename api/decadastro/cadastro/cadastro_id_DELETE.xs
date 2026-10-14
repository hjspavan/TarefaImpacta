// Delete cadastro record
query "cadastro/{cadastro_id}" verb=DELETE {
  api_group = "decadastro"

  input {
    int cadastro_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.cadastro_id
    }
  }

  response = null
  guid = "1U0B1LmH8VKze9fDx8yhNd-EJhU"
}