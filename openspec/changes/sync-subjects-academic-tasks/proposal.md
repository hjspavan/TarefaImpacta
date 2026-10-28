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
