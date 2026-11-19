query academic_tasks verb=GET {
  api_group = "academic_tasks"
  auth = "User"

  input {
    int subject_id?
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $user_subjects

    db.query academic_tasks {
      where = $db.academic_tasks.subject_id in ($user_subjects.id)
      return = {type: "list"}
    } as $tasks_result
  }

  response = $tasks_result
}
