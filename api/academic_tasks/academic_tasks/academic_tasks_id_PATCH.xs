// Edit academic task belonging to authenticated user
query "academic_tasks/{academic_tasks_id}" verb=PATCH {
  api_group = "academic_tasks"
  auth = "User"

  input {
    int academic_tasks_id filters=min:1
    text title?
    text description?
    timestamp due_date?
    text status?
    int subject_id? filters=min:1
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    } as $existing_task

    precondition ($existing_task != null) {
      error_type = "notfound"
      error = "Task not found."
    }

    db.get subjects {
      field_name = "id"
      field_value = $existing_task.subject_id
    } as $current_subject

    precondition ($current_subject != null && $current_subject.user_id == $auth.id) {
      error_type = "notfound"
      error = "Task not found or access denied."
    }

    conditional ($input.subject_id != null) {
      db.get subjects {
        field_name = "id"
        field_value = $input.subject_id
      } as $new_subject

      precondition ($new_subject != null && $new_subject.user_id == $auth.id) {
        error_type = "accessdenied"
        error = "Target subject not found or does not belong to authenticated user."
      }
    }

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $updated_task
  }

  response = $updated_task
  guid = "academic_tasks_id_PATCH_endpoint_005"
}

