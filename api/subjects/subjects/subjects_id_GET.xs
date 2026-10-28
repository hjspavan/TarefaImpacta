// Get single subjects record belonging to authenticated user
query "subjects/{subjects_id}" verb=GET {
  api_group = "subjects"
  auth = "User"

  input {
    int subjects_id filters=min:1
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.subjects_id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "notfound"
      error = "Subject not found."
    }
  }

  response = $subject
  guid = "subjects_id_GET_endpoint_004"
}

