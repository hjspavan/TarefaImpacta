// Query all User records
query user verb=GET {
  api_group = "API_Browser"

  input {
  }

  stack {
    db.query User {
      return = {type: "list"}
    } as $user
  }

  response = $user
  guid = "J9zpSO8BZQFkyj2wEriqoMAH6ws"
}