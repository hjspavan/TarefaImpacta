## ADDED Requirements

### Requirement: Synchronize subjects

The Disciplines screen MUST retrieve subjects from the existing Xano endpoints and display the returned records instead of hardcoded mock data.

The screen MUST use the existing authenticated session when the endpoint requires authentication.

#### Scenario: Subjects are available

- WHEN the user opens the Disciplines screen
- THEN the application retrieves subjects from Xano and displays the returned records.

#### Scenario: Subjects request fails

- WHEN the Xano request fails
- THEN the application displays a clear error message.
