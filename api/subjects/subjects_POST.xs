// Create a new subject for the authenticated user
query subjects verb=POST {
  api_group = "subjects"
  auth = "User"

  input {
    text name
    text teacher?
    int hours
  }

  stack {
    db.add subjects {
      enforce_hidden_fields = false
      data = {
        name    : $input.name
        teacher : $input.teacher
        hours   : $input.hours
        user_id : $auth.id
      }
    } as $subject
  }

  response = $subject
  guid = "subjects_POST_endpoint_002"
}

