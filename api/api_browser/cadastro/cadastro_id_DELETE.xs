// Delete cadastro record
query "cadastro/{cadastro_id}" verb=DELETE {
  api_group = "API_Browser"

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
  guid = "WWP0Edz_QOjh1H8x-2pPvQUgNDs"
}