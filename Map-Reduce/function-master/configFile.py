FORMAT = "utf-8"
CREDENTIALS = 'aniruddho-chatterjee-fall2023-f967fa2ed4a5.json'
AUTH = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjBhZDFmZWM3ODUwNGY0NDdiYWU2NWJjZjVhZmFlZGI2NWVlYzllODEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAxMTEyMjA3MjkwOTM2MTY2Mjc3IiwiaGQiOiJpdS5lZHUiLCJlbWFpbCI6ImNhc3dhcGFuQGl1LmVkdSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiemhCcm9UUV91dFV5MnJTTUxIS3l4dyIsImlhdCI6MTcwMjE2MDg5OCwiZXhwIjoxNzAyMTY0NDk4fQ.pWijzaa5jKULVEehI8YR7NjaVI6yuNdj7nPYMh7S6f2oDiKQbJnaGl9Ds1o5NWL6MmQ552NCr_fq-V21GaiEOpa8x6oN2O8qEZPR5hKJWqhG4RR1Eov1sAFrvYNsUQ7XdDjKo9KkgseXYrVtqbSJZIvrNxXHXJQsNNFtGDcifszRY07HUT__z_eGwEv95WuebyWUjsPCoCbjd5hq0qQPebfrEWT5e26W2cmzRf9TJsScWLL9qEFuP110UM-qziq281DlViVMwil7UB1CX3EG1Z8d8d7aYoDrc7bEUq_dtQpOduwPiMYOm7-JZZpQ-HQEixUonghg24V4JBwGsiPNkQ'
PROJECTID = 'aniruddho-chatterjee-fall2023'
INPUT_BUCKET_NAME = 'books-dataset'
NUMBER_OF_MAPPERS = 5
NUMBER_OF_REDUCERS = 5
CREATE_CHUNKS='https://us-central1-aniruddho-chatterjee-fall2023.cloudfunctions.net/create-chunks'
MAPPERURL = 'https://us-central1-aniruddho-chatterjee-fall2023.cloudfunctions.net/mapper'
SHUFFLEURL = 'https://us-central1-aniruddho-chatterjee-fall2023.cloudfunctions.net/shuffle-sort'
REDUCERURL='https://us-central1-aniruddho-chatterjee-fall2023.cloudfunctions.net/reducer'
INDEXING_INPUT='books-reducer'
INDEXING_OUTPUT = 'books-indexing'
OUTPUT_FILENAME = 'search'
CLEANUP='["books-chunks","books-mapper","books-shufflesort","books-reducer"]'