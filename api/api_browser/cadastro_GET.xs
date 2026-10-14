// Query all cadastro records
query cadastro verb=GET {
  api_group = "API_Browser"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $model
  }

  response = $model
  guid = "TOPV_AYfGP5S3brUBDyxtS6pGFU"
}