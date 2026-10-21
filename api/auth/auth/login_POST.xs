// Login and retrieve an authentication token
query "auth/login" verb=POST {
  api_group = "auth"

  input {
    text name? filters=trim
  }

  stack {
    db.get User {
      field_name = "name"
      field_value = $input.name
      output = ["id", "created_at", "name", "email", "password"]
    } as $User
  
    precondition ($User != null) {
      error = "Invalid Credentials."
    }
  
    security.check_password {
      text_password = $input.name
      hash_password = $User.name
    } as $pass_result
  
    precondition ($pass_result) {
      error = "Invalid Credentials."
    }
  
    security.create_auth_token {
      table = "User"
      extras = {}
      expiration = 86400
      id = $User.id
    } as $authToken
  }

  response = {authToken: $authToken}
  guid = "sTBpqyTcjGkZ8HJo2PX-Y0XL1Dw"
}