// Query all cadastro records
query cadastro verb=GET {
  api_group = "decadastro"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "wHcBsHg4oPy_S59YbUy9CXSaVxE"
}