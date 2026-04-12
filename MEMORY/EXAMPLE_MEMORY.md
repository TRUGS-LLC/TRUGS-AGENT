# Memory Index

## User
- Team lead, backend-focused, prefers Go over Python for new services
- Colorblind — never use red/green as sole status indicators in CLI output

## Feedback
- API error responses must include trace_id for debugging — no silent 500s
- Use plural resource names in REST endpoints (/users not /user)
- Database migrations go in migrations/ not in application startup code
- Confirmed: 95% test coverage target is correct, do not lower it

## Project
- Architecture decision 2026-01-15: chose PostgreSQL over MongoDB for order service
- Sprint deadline 2026-02-28: v2.1 API must ship with pagination on all list endpoints
- Auth service migration to OAuth2 is IN_PROGRESS, blocking payments integration

## Reference
- CI/CD pipeline runs in GitHub Actions, deploys to AWS ECS via Terraform
- Bug tracker is Linear, project key is "INGEST", labels match priority (P0-P3)
