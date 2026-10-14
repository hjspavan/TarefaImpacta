// Add cadastro record
query cadastro verb=POST {
  api_group = "decadastro"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        nome      : $input.nome
        endeco    : $input.endeco
      }
    } as $model
  }

  response = $model
  guid = "y8S9KIgcxELpI3HzbyE7vtTue2I"
}