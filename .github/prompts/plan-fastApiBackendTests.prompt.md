## Plan: FastAPI Backend Tests

Separate backend tests under tests/ using pytest plus FastAPI's TestClient. Reuse the current single-app structure in /workspaces/skills-getting-started-with-github-copilot/src/app.py, isolate shared setup in fixtures, and explicitly manage the in-memory activities state so tests stay deterministic.

**Steps**
1. Add test tooling dependencies. Update /workspaces/skills-getting-started-with-github-copilot/requirements.txt to include pytest. Keep the dependency set minimal unless async test support is intentionally needed.
2. Create a dedicated tests directory. Add /workspaces/skills-getting-started-with-github-copilot/tests/ as the backend test root so tests are separate from /workspaces/skills-getting-started-with-github-copilot/src/.
3. Add shared fixtures in /workspaces/skills-getting-started-with-github-copilot/tests/conftest.py. Expose a FastAPI TestClient from src.app and reset the in-memory activities dictionary before each test so POST/DELETE tests do not leak state across runs. This step blocks endpoint test implementation.
4. Add coverage for the read endpoint in /workspaces/skills-getting-started-with-github-copilot/tests/test_activities.py. Verify GET /activities returns 200 and the expected activity shape: description, schedule, max_participants, participants.
5. Add signup tests in /workspaces/skills-getting-started-with-github-copilot/tests/test_signup.py. Cover successful signup, duplicate signup rejection, activity-not-found rejection, and full-activity rejection. This depends on step 3.
6. Add unregister tests in /workspaces/skills-getting-started-with-github-copilot/tests/test_signup.py or a separate /workspaces/skills-getting-started-with-github-copilot/tests/test_unregister.py if you want stricter separation. Cover successful removal, activity-not-found rejection, and participant-not-found rejection. This depends on step 3.
7. Run focused verification with pytest against the new tests directory and tighten any fixture/reset logic if state leaks appear.
8. Optionally document test execution in /workspaces/skills-getting-started-with-github-copilot/src/README.md or /workspaces/skills-getting-started-with-github-copilot/README.md if you want contributors to discover the test command easily. This is parallel with step 7 and not required for the test suite itself.

**Relevant files**
- /workspaces/skills-getting-started-with-github-copilot/requirements.txt — add pytest dependency for local test execution.
- /workspaces/skills-getting-started-with-github-copilot/pytest.ini — reuse existing pythonpath configuration; only expand if discovery/import patterns need it.
- /workspaces/skills-getting-started-with-github-copilot/src/app.py — import app and current in-memory activities store from here; fixture design should account for mutable global state.
- /workspaces/skills-getting-started-with-github-copilot/tests/conftest.py — central fixture setup for TestClient and activity-state reset.
- /workspaces/skills-getting-started-with-github-copilot/tests/test_activities.py — GET endpoint coverage.
- /workspaces/skills-getting-started-with-github-copilot/tests/test_signup.py — POST and DELETE endpoint coverage.

**Verification**
1. Run pytest from /workspaces/skills-getting-started-with-github-copilot and confirm the new tests under tests/ are discovered.
2. Verify state isolation by running the signup/delete tests repeatedly and confirming the order does not affect outcomes.
3. Confirm error-path assertions match the current API contract in /workspaces/skills-getting-started-with-github-copilot/src/app.py: 400 for duplicate/full signup, 404 for missing activity or missing participant.

**Decisions**
- Included: backend API tests only, in a separate tests directory.
- Excluded: frontend tests, refactoring app structure, and replacing the in-memory store with a database.
- Recommendation: keep tests synchronous with FastAPI TestClient because the current endpoints in /workspaces/skills-getting-started-with-github-copilot/src/app.py are synchronous.
- Recommendation: do not add pytest-asyncio unless the app actually introduces async-only test needs.

**Further Considerations**
1. Dependency placement: Option A is adding pytest to requirements.txt for simplicity in this small exercise; Option B is splitting dev dependencies later if the project grows. Recommendation: Option A for now.
2. Test file split: Option A is one file for all signup/unregister mutation tests; Option B is separate files for signup and unregister. Recommendation: Option A initially, split later only if the suite grows.
