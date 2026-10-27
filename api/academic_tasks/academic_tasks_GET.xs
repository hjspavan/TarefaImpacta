// Query academic tasks belonging to authenticated user's subjects
query academic_tasks verb=GET {
  api_group = "academic_tasks"
  auth = "User"

  input {
    int subject_id? filters=min:1
  }

  stack {
    conditional ($input.subject_id != null) {
      db.get subjects {
        field_name = "id"
        field_value = $input.subject_id
      } as $target_subject

      precondition ($target_subject != null && $target_subject.user_id == $auth.id) {
        error_type = "notfound"
        error = "Subject not found or access denied."
      }

      db.query academic_tasks {
        where = $db.academic_tasks.subject_id == $input.subject_id
        return = {type: "list"}
      } as $tasks_result
    }
    else {
      db.query subjects {
        where = $db.subjects.user_id == $auth.id
        return = {type: "list"}
      } as $user_subjects

      db.query academic_tasks {
        where = $db.academic_tasks.subject_id in ($user_subjects|pluck:"id")
        return = {type: "list"}
      } as $tasks_result
    }
  }

  response = $tasks_result
  guid = "academic_tasks_GET_endpoint_003"
}

