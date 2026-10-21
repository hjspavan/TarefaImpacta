// Get User record
query "user/{user_id}" verb=GET {
  api_group = "API_Browser"

  input {
    int user_id? filters=min:1
  }

  stack {
    db.get User {
      field_name = "id"
      field_value = $input.user_id
    } as $user
  
    precondition ($user != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $user
  guid = "sDPi1eFqTQxV5_Zfv749oaIVY0o"
}