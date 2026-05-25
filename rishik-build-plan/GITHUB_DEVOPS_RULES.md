# GITHUB DEVOPS RULES — STRICT (Apply to ALL Projects)

> These rules are NON-NEGOTIABLE. Every AI agent or builder working on any project
> in this workspace MUST follow these rules exactly. No exceptions.

---

## 1. REPOSITORY INITIALIZATION

```bash
# Step 1: Create repo on GitHub (public)
gh repo create <project-name> --public --description "<desc>"

# Step 2: Clone and set up
git clone https://github.com/rishikkumar84a/<project-name>
cd <project-name>

# Step 3: Create initial structure and commit to main
echo "# <Project Name>" > README.md
git add . && git commit -m "chore: initial project scaffold"
git push origin main

# Step 4: Create develop branch
git checkout -b develop
git push origin develop
```

---

## 2. BRANCH PROTECTION RULES (Set on GitHub)

After creating the repo, go to **Settings → Branches → Add Rule** and apply:

### For `main` branch:
- ✅ Require a pull request before merging
- ✅ Require at least 1 approval (from Copilot or reviewer)
- ✅ Require status checks to pass (CI tests)
- ✅ Do not allow bypassing the above settings
- ❌ Never push directly to main

### For `develop` branch:
- ✅ Require a pull request before merging
- ✅ Require CI tests to pass

---

## 3. BRANCH NAMING CONVENTION

```
feature/<short-description>      → New feature
fix/<short-description>          → Bug fix
test/<short-description>         → Adding or fixing tests
docs/<short-description>         → Documentation only
chore/<short-description>        → Setup, config, tooling
refactor/<short-description>     → Code improvement, no new feature
```

**Examples:**
```
feature/user-authentication
feature/research-agent-integration
fix/api-timeout-handling
test/unit-tests-for-agent-module
docs/readme-update
```

---

## 4. COMMIT MESSAGE CONVENTION (Conventional Commits)

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `test` — Adding tests
- `docs` — Documentation
- `chore` — Build process, tooling
- `refactor` — Refactoring
- `style` — Formatting only
- `ci` — CI/CD changes

**Examples:**
```
feat(agent): add research agent with web search capability
fix(api): handle empty response from LLM gracefully
test(agent): add unit tests for curriculum generation module
chore(docker): add Dockerfile and docker-compose setup
docs(readme): add setup instructions and environment variables
```

---

## 5. FEATURE DEVELOPMENT WORKFLOW (Every single feature)

```
STEP 1 → Create feature branch from develop
  git checkout develop
  git pull origin develop
  git checkout -b feature/<name>

STEP 2 → Write the feature code

STEP 3 → Write unit tests for the feature
  - Every function/module must have at least one test
  - Tests must pass before PR creation
  - Run: pytest (Python) or npm test (Node/React)

STEP 4 → Commit with conventional commit message
  git add .
  git commit -m "feat(<scope>): <description>"

STEP 5 → Push branch to GitHub
  git push origin feature/<name>

STEP 6 → Create Pull Request (feature → develop)
  gh pr create \
    --title "feat: <description>" \
    --body "## Summary\n<what this PR does>\n\n## Test Plan\n<how it was tested>" \
    --base develop \
    --head feature/<name>

STEP 7 → Request GitHub Copilot Review
  - In the PR, comment: @github-copilot review
  - OR go to PR → Reviewers → Add "Copilot"
  - Wait for Copilot to post its review

STEP 8 → Fix any issues Copilot flags
  git add . && git commit -m "fix: address Copilot review comments"
  git push origin feature/<name>

STEP 9 → Merge ONLY after Copilot review is complete
  gh pr merge --squash --delete-branch

STEP 10 → Repeat from STEP 1 for next feature
```

---

## 6. CI/CD WITH GITHUB ACTIONS

Create `.github/workflows/ci.yml` in every project:

```yaml
name: CI Pipeline

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up environment
        uses: actions/setup-python@v4   # or setup-node@v3 for MERN
        with:
          python-version: '3.11'        # or node-version: '20'

      - name: Install dependencies
        run: pip install -r requirements.txt   # or npm install

      - name: Run tests
        run: pytest --cov=./ --cov-report=xml  # or npm test

      - name: Lint check
        run: flake8 . --max-line-length=100    # or npm run lint
```

---

## 7. FINAL MERGE TO MAIN

Only done when the full project is ready for submission:

```bash
# Create PR from develop → main
gh pr create \
  --title "release: v1.0.0 final submission" \
  --body "Final project ready for submission" \
  --base main \
  --head develop

# Request Copilot review on this PR too
# Merge only after review
gh pr merge --merge
```

---

## 8. README.md REQUIREMENTS (Every project)

Every README must contain:
```markdown
# Project Name
Short description

## Tech Stack
## Features
## Architecture Diagram (text/ASCII is fine)
## Prerequisites
## Environment Variables (.env.example with all keys listed, no values)
## Installation & Local Setup
## Running Tests
## API Documentation (if backend)
## Demo Video Link
## Live Deployment URL (if any)
```

---

## 9. ENVIRONMENT VARIABLES

- Never commit `.env` files
- Always include `.env.example` with keys but no values
- Add `.env` to `.gitignore` from day one

```bash
# .gitignore must always include:
.env
.env.local
node_modules/
__pycache__/
*.pyc
.DS_Store
```

---

---

## 10. STRICT FILE-BY-FILE COMMIT RULE (Critical — Most agents fail this)

> This is the most commonly violated rule by AI agents. Read carefully and follow exactly.

### THE RULE: One File = One Commit = One Push. Immediately.

```
CORRECT WORKFLOW:
  Write file_1.py
  → git add file_1.py
  → git commit -m "feat(scope): add file_1"
  → git push origin feature/<branch>
  → PAUSE
  → Write file_2.py
  → git add file_2.py
  → git commit -m "feat(scope): add file_2"
  → git push origin feature/<branch>
  → PAUSE
  → Write file_3.py
  → git add file_3.py
  → git commit -m "feat(scope): add file_3"
  → git push origin feature/<branch>

WRONG WORKFLOW (FORBIDDEN):
  Write file_1.py, file_2.py, file_3.py
  → git add .
  → git commit -m "feat: add all files"  ← NEVER DO THIS
  → git push
```

### THE MODIFICATION RULE: Every Edit = Immediate Commit + Push

If after writing file_3 you realize file_1 or file_2 needs a change:

```
CORRECT:
  Modify file_1.py
  → IMMEDIATELY: git add file_1.py
  → git commit -m "fix(scope): update file_1 to support file_3 requirement"
  → git push origin feature/<branch>
  → ONLY THEN continue to next task

WRONG (FORBIDDEN):
  Modify file_1.py and file_2.py
  → wait until later to push  ← NEVER
  → bundle with unrelated changes  ← NEVER
```

### WHY THIS MATTERS
- Every push = one green square on GitHub contribution graph
- Granular commits = easier for Copilot to review
- If something breaks, it is immediately traceable to the exact file
- Bundled commits make it impossible to track what caused a bug

### ENFORCEMENT (Agent must follow this checklist after every single file):
```
After writing or modifying ANY file:
  [ ] git add <that specific file only>
  [ ] git commit -m "<type>(<scope>): <what changed in this file>"
  [ ] git push origin feature/<current-branch>
  [ ] ONLY THEN start the next file
```

---

## 11. PULL REQUEST SIZE LIMIT (Maximum 10 Files Per PR)

### RULE: No PR may contain more than 10 files changed.

```
If a feature requires more than 10 files:
  → Split it into sub-features
  → Create separate branches for each sub-feature
  → Each sub-feature gets its own PR
  → Each PR reviewed separately by GitHub Copilot

Example — "research-agent" feature has 12 files:
  Branch 1: feature/research-agent-core     (files 1–6)  → PR → Copilot review → merge
  Branch 2: feature/research-agent-tools    (files 7–12) → PR → Copilot review → merge
```

### WHY 10 FILES MAX?
- GitHub Copilot review quality drops significantly above 10 files
- Large PRs cause Copilot to miss bugs and logic errors
- Smaller PRs = faster review = faster merge = more contributions
- If Copilot takes too long, the whole pipeline slows down

### PR CHECKLIST BEFORE CREATING:
```
[ ] Count the files changed: git diff --name-only develop
[ ] If count > 10 → split into multiple branches NOW
[ ] If count ≤ 10 → proceed to create PR
```

---

## 12. GITHUB COPILOT REVIEW — ONLY COPILOT, NO EXCEPTIONS

### RULE: PRs are reviewed by GitHub Copilot only. No self-merge. No bypassing.

```
HOW TO REQUEST COPILOT REVIEW:

Option A (Recommended — in PR description):
  Add this line in the PR body:
  "@github-copilot Please review this PR for bugs, logic errors,
   and code quality issues."

Option B (In PR comments after creation):
  Comment: @github-copilot review

Option C (GitHub UI):
  PR page → Reviewers (right panel) → Search "Copilot" → Add
```

### COPILOT REVIEW RESPONSE RULES:
```
After Copilot reviews:
  IF Copilot flags issues:
    → Fix every flagged issue, one file at a time (follow Rule 10 above)
    → Each fix = separate commit + push
    → Re-request review if major changes made

  IF Copilot approves or has no blocking issues:
    → Merge the PR: gh pr merge --squash --delete-branch
    → NEVER merge before Copilot has posted its review
    → NEVER self-approve and merge
```

### MERGE IS BLOCKED UNTIL:
```
  [ ] Copilot has posted a review comment on the PR
  [ ] All Copilot-flagged issues are addressed
  [ ] CI tests are passing (green checkmark)
```

---

## AGENT RULE SUMMARY (Read this before any action)

```
BEFORE WRITING ANY CODE:
  ✅ Create GitHub repo
  ✅ Set up main + develop branches
  ✅ Add branch protection rules

FOR EVERY SINGLE FILE:
  ✅ Write ONE file
  ✅ git add <that file only>
  ✅ git commit -m "type(scope): description"
  ✅ git push immediately
  ✅ PAUSE — only then start next file
  ✅ Any modification to any file = immediate commit + push

FOR EVERY FEATURE BRANCH:
  ✅ Maximum 10 files per PR — split if more
  ✅ New branch from develop
  ✅ Write + push files one by one
  ✅ Write unit tests (also one file at a time)
  ✅ Open PR → develop
  ✅ Tag @github-copilot for review (ONLY Copilot reviews)
  ✅ Wait for Copilot review to post
  ✅ Fix every Copilot issue — each fix = separate commit + push
  ✅ Merge only after Copilot review complete + CI passing

NEVER:
  ❌ Push directly to main
  ❌ Write 2+ files before pushing
  ❌ Bundle modifications with unrelated files
  ❌ Create PR with more than 10 files
  ❌ Merge without Copilot review
  ❌ Self-approve or bypass Copilot
  ❌ Merge without tests passing
  ❌ Commit .env files
```
