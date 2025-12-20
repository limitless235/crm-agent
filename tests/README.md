# Testing Guide

This project uses an integration-first testing strategy. No core infrastructure is mocked.

## Prerequisites
- Docker and Docker Compose installed.
- All services running (`docker-compose up -d`).

## Running E2E Tests

1. **Install Test Dependencies**:
   ```bash
   pip install -r tests/requirements.txt
   ```

2. **Execute Tests**:
   ```bash
   pytest tests/e2e/test_system.py
   ```

## Test Coverage
- **User Authentication**: Validates registration and JWT login.
- **Ticket Lifecycle**: Validates ticket creation and message retrieval.
- **AI Worker Integration**: Ensures the AI worker consumes events and writes responses back to the DB.
- **WebSocket Updates**: Verifies that new messages (from users or AI) are broadcasted to connected clients.

## Important Notes
- Ensure the AI Worker has access to a local model (GGUF) at the path specified in `.env` for the generative tests to succeed.
- Tests use the live API endpoints; no direct database manipulation is performed.
