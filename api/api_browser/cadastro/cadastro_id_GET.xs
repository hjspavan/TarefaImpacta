// Get cadastro record
query "cadastro/{cadastro_id}" verb=GET {
  api_group = "API_Browser"

  input {
    int cadastro_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.cadastro_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "RnYf_lbQoQETwWBIfNGz7o_qf20"
}