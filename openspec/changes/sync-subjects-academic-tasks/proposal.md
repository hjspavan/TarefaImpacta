# Change: sync-subjects-academic-tasks

## Why
The Disciplines and Tasks screens currently use mock data instead of synchronizing with Xano. This change will connect both screens to the existing `subjects` and `academic_tasks` API endpoints.

## What Changes
- Synchronize the Disciplines screen with the `subjects` table.
- Synchronize the Tasks screen with the `academic_tasks` table.
- Use the existing authentication session when calling protected endpoints.
- Handle loading, empty results, and API errors in the Streamlit interface.

## Impact
- Affected screens: `pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py`.
- Data source: existing Xano endpoints for `subjects` and `academic_tasks`.
- Existing authentication and profile behavior must remain unchanged.

## Existing Endpoint Contracts

### Subjects
- `GET /subjects`: retrieves subjects belonging to the authenticated user.
- `POST /subjects`: creates a subject for the authenticated user, with `name`, `teacher`, and `hours` fields.

### Academic Tasks
- `GET /academic_tasks`: retrieves academic tasks for the authenticated user and optionally filters by `subject_id`.
- `POST /academic_tasks`: creates an academic task with `title`, `description`, `due_date`, `status`, and `subject_id`, validating the subject association.

These endpoints use the existing Xano API groups:
- `api/subjects/subjects_GET.xs`
- `api/subjects/subjects_POST.xs`
- `api/academic_tasks/academic_tasks_GET.xs`
- `api/academic_tasks/academic_tasks_POST.xs`
