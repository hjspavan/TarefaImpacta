// Delete subjects record belonging to authenticated user
query "subjects/{subjects_id}" verb=DELETE {
  api_group = "subjects"
  auth = "User"

  input {
    int subjects_id filters=min:1
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.subjects_id
    } as $existing_subject

    precondition ($existing_subject != null && $existing_subject.user_id == $auth.id) {
      error_type = "notfound"
      error = "Subject not found or access denied."
    }

    db.del subjects {
      field_name = "id"
      field_value = $input.subjects_id
    }
  }

  response = null
  guid = "subjects_id_DELETE_endpoint_006"
}

