// Download or retrieve student academic performance report
query "reports/performance" verb=GET {
  api_group = "reports"
  auth = "User"

  input {
  }

  stack {
    db.get User {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "created_at", "name", "email"]
    } as $user

    precondition ($user != null) {
      error_type = "notfound"
      error = "User not found."
    }

    db.query subjects {
      where = ($db.subjects.user_id == $auth.id || $db.subjects.user2_id == $auth.id)
      return = {type: "list"}
    } as $subjects

    db.query academic_tasks {
      where = $db.academic_tasks.subject_id in ($subjects|pluck:"id")
      return = {type: "list"}
    } as $all_tasks

    var $report_data {
      value = {
        generated_at : "now"
        student      : $user
        subjects     : $subjects
        tasks        : $all_tasks
      }
    }
  }

  response = $report_data
  guid = "reports_performance_GET_001"
}
