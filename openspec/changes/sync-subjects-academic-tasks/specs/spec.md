# Specification: Synchronize Subjects and Academic Tasks

## Requirements

### Requirement: Synchronize subjects
The Disciplines screen MUST retrieve subjects from the existing Xano endpoints and display the returned records instead of hardcoded mock data.

The screen MUST use the existing authenticated session when the endpoint requires authentication.

#### Scenario: Subjects are available
- WHEN the user opens the Disciplines screen
- THEN the application retrieves subjects from Xano and displays the returned records.

#### Scenario: Subjects request fails
- WHEN the Xano request fails
- THEN the application displays a clear error message.

### Requirement: Synchronize academic tasks
The Tasks screen MUST retrieve academic tasks from the existing Xano endpoints and display the returned records instead of mock data.

Tasks MUST preserve their relationship with the corresponding subject through `subject_id`.

#### Scenario: Tasks are available
- WHEN the user opens the Tasks screen
- THEN the application retrieves tasks from Xano and displays the returned records.

#### Scenario: Tasks request fails
- WHEN the Xano request fails
- THEN the application displays a clear error message.

### Requirement: Preserve authentication
The integration MUST reuse the application's existing authentication session and MUST NOT expose the authentication token to the user.
