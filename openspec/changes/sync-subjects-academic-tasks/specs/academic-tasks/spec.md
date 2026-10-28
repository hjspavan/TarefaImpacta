## ADDED Requirements

### Requirement: Synchronize academic tasks

The Tasks screen MUST retrieve academic tasks from the existing Xano endpoints and display the returned records instead of mock data.

Tasks MUST preserve their relationship with the corresponding subject through subject_id.

#### Scenario: Tasks are available

- WHEN the user opens the Tasks screen
- THEN the application retrieves tasks from Xano and displays the returned records.

#### Scenario: Tasks request fails

- WHEN the Xano request fails
- THEN the application displays a clear error message.

#### Scenario: Tasks are associated with subjects

- WHEN the application displays an academic task
- THEN it preserves the task's subject_id relationship with the corresponding subject.
