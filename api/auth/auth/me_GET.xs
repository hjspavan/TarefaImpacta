// Get the record belonging to the authentication token
query "auth/me" verb=GET {
  api_group = "auth"
  auth = "User"

  input {
  }

  stack {
    db.get User {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "created_at", "name", "email", "senha"]
    } as $User
  }

  response = $User
  guid = "gCDuEplAOBoqdIXdUqIausIxExo"
}