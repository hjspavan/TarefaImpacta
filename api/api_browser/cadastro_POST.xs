// Add cadastro record
query cadastro verb=POST {
  api_group = "API_Browser"

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
        email     : $input.email
        CPF       : $input.CPF
        celular   : $input.celular
        senha     : $input.senha
      }
    } as $model
  }

  response = $model
  guid = "bAypjlxyG9PWgFY8z4ibrKc6EBw"
}