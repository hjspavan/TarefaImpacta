// Update cadastro record
query "cadastro/{cadastro_id}" verb=PUT {
  api_group = "API_Browser"

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
      data = {
        nome   : $input.nome
        endeco : $input.endeco
        email  : $input.email
        CPF    : $input.CPF
        celular: $input.celular
        senha  : $input.senha
      }
    } as $model
  }

  response = $model
  guid = "oO-Wl2-OBbxPmawyyyKs7OPR4dw"
}