// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "auth"

  input {
    text name?
    text email?
    text senha?
  }

  stack {
    db.get User {
      field_name = "email"
      field_value = $input.name
    } as $User
  
    precondition ($User == null) {
      error_type = "accessdenied"
      error = "This account is already in use."
    }
  
    db.add User {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        name      : $input.name
        email     : $input.email
        senha     : $input.senha
      }
    } as $User
  
    security.create_auth_token {
      table = "User"
      extras = {}
      expiration = 86400
      id = $User.id
    } as $authToken
  }

  response = {authToken: $authToken}
  guid = "Wne1szQ5oiPb_uzPkb6gxs1vMRc"
}