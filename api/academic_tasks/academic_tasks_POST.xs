// Create a new academic task verifying subject ownership
query academic_tasks verb=POST {
  api_group = "academic_tasks"
  auth = "User"

  input {
    text title
    text description?
    timestamp due_date?
    text status
    int subject_id filters=min:1
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Subject not found or does not belong to authenticated user."
    }

    db.add academic_tasks {
      enforce_hidden_fields = false
      data = {
        title       : $input.title
        description : $input.description
        due_date    : $input.due_date
        status      : $input.status
        subject_id  : $input.subject_id
      }
    } as $academic_task
  }

  response = $academic_task
  guid = "academic_tasks_POST_endpoint_002"
}

