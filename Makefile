# Agents Blog task runner for macOS and Linux.
# Windows uses make.ps1 with the same target names.

.PHONY: setup dev lint format typecheck test test-e2e test-bdd coverage build preview audit sync-agents release clean

setup:
	@echo "setup: will install project dependencies once the stack is chosen"

dev:
	@echo "dev: will start the local development server once the stack is chosen"

lint:
	@echo "lint: no-op until the stack lands; will enforce zero lint warnings"

format:
	@echo "format: will format sources with Prettier and ruff once the stack is chosen"

typecheck:
	@echo "typecheck: no-op until the stack lands; will run the strict type checker"

test:
	@if [ -d tests ]; then python3 -m unittest discover -s tests -v; else echo "test: no tests directory; nothing to run"; fi

test-e2e:
	@echo "test-e2e: will run end-to-end tests once the stack is chosen"

test-bdd:
	@echo "test-bdd: will run Gherkin journeys (subscribe, read post, search) once the stack is chosen"

coverage:
	@echo "coverage: no-op until the stack lands; core logic target is 100 percent and the CI gate is 80 percent"

build:
	python3 -m compileall -q scripts tests

preview:
	@echo "preview: will serve the production build once the stack is chosen"

audit:
	@echo "audit: will audit dependencies once the stack is chosen"

sync-agents:
	@if [ -f scripts/sync-agents.ps1 ]; then pwsh -NoProfile -File scripts/sync-agents.ps1; else echo "sync-agents: scripts/sync-agents.ps1 not found; nothing to sync"; fi

release:
	@echo "release: will cut a versioned release once the stack is chosen"

clean:
	@echo "clean: will remove local build artifacts once the stack is chosen"
