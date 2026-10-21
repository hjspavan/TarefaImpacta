// Delete User record.
query "user/{user_id}" verb=DELETE {
  api_group = "API_Browser"

  input {
    int user_id? filters=min:1
  }

  stack {
    db.del User {
      field_name = "id"
      field_value = $input.user_id
    }
  }

  response = null
  guid = "3tIrHsbvx46-KqHONejxDiPP0fI"
}