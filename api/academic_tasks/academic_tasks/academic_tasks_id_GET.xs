// Get single academic task belonging to authenticated user
query "academic_tasks/{academic_tasks_id}" verb=GET {
  api_group = "academic_tasks"
  auth = "User"

  input {
    int academic_tasks_id filters=min:1
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    } as $task

    precondition ($task != null) {
      error_type = "notfound"
      error = "Task not found."
    }

    db.get subjects {
      field_name = "id"
      field_value = $task.subject_id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "notfound"
      error = "Task not found or access denied."
    }
  }

  response = $task
  guid = "academic_tasks_id_GET_endpoint_004"
}

