// Edit cadastro record
query "cadastro/{cadastro_id}" verb=PATCH {
  api_group = "API_Browser"

  input {
    int cadastro_id? filters=min:1
    dblink {
      table = ""
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "" {
      field_name = "id"
      field_value = $input.cadastro_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "TYJBwCOFJ34cg3B6ichLa5yhCu4"
}