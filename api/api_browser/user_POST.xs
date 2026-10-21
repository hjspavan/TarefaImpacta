// Add User record
query user verb=POST {
  api_group = "API_Browser"

  input {
    dblink {
      table = "User"
    }
  }

  stack {
    db.add User {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $user
  }

  response = $user
  guid = "mumG-GGFCW2C0jQkRW4y88RXl_Y"
}