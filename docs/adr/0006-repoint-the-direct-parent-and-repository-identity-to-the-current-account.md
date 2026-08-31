---
id: adr-0006
title: ADR-0006 — Repoint the direct parent and repository identity to the current account
status: proposed
updated: 2026-09-01
---

# ADR-0006: Repoint the direct parent and repository identity to the current account

| Field | Value |
|-------|-------|
| Status | proposed |
| Date | 2026-09-01 |
| Deciders | repository owner |
| Author | Claude Code (AI agent) |
| Supersedes / Superseded by | Refines ADR-0005 for the current account |

## Context

This repository has moved to the `ea-Mitsuoka` GitHub account. `git remote get-url
origin` is `https://github.com/ea-Mitsuoka/nextjs-saas-template.git`. Its inheritance
metadata still names the former `Yukihide-Mitsuoka` account, both as its direct parent
and as its own identity.

`ea-Mitsuoka/ai-dev-foundation` and `Yukihide-Mitsuoka/ai-dev-foundation` are distinct
repositories under distinct accounts, so the recorded parent is not reachable from the
maintained foundation through GitHub rename redirection.

Three effects follow, one of which is specific to this repository:

- Scheduled Template Sync reads a foundation the owner no longer updates. A stale parent
  produces no error, only an absence of incoming changes.
- `make doctor` reported `Root README ownership is invalid (ADR-0011)`, because
  `scripts/readme_ownership.py` compares the marker against `remote.origin.url`.
- The ADR-0005 size exception is unreachable. `scripts/pr-size-policy.sh` grants the
  GR-020 hard-limit exception only when the target repository equals
  `Yukihide-Mitsuoka/nextjs-saas-template` *and* the PR body matches
  `^Direct-parent-source: https://github\.com/Yukihide-Mitsuoka/ai-dev-foundation@[0-9a-f]{40}$`.
  Both operands are wrong now: the target repository will never match, and the sync
  workflow will write the new source URL into the body. A mechanical foundation sync PR
  above the hard limit is therefore blocked with no way to pass.

This repository is also a parent. It exports the Next.js SaaS family contract from
`.ai/contracts/templates/yukihide-mitsuoka/nextjs-saas-template/`. Foundation ADR-0014
derives that path from the exporting repository's owner, and
`scripts/template_inheritance.py` enforces the derivation: a `template` agent-profile
input must live under `.ai/contracts/templates/<owner>/<repository>/`, lowercased. The
directory name is part of the contract, not a naming preference. This repository has no
child in the fleet configuration today, so the rename has no downstream coordination
cost.

## Options considered

### Option 1: Do nothing

Leave every owner-qualified reference on the former account. Nothing breaks immediately,
and the recorded parent still exists.

It leaves `make doctor` failing, leaves the ADR-0005 exception unreachable, leaves review
routing pointed at a non-owner, and lets this repository drift from the maintained
foundation indefinitely.

### Option 2: Repoint the direct parent only

Change `.github/inheritance/manifest.json`, `lock.json`, `agent-profile.json`, and the
Template Sync source, and leave this repository's own identity on the former account.

This restores synchronization with a small diff, but it does not fix the ADR-0005 size
exception, whose *target* operand is this repository's own name, and it leaves the
exported contract root claiming an owner that no longer holds this repository.

### Option 3: Repoint the parent and this repository's identity together

Additionally rename the exported contract root to
`.ai/contracts/templates/ea-mitsuoka/nextjs-saas-template/`, update the manifest
ownership entry and `.templatesyncignore` that must cover it, and update the size-policy
operands, CODEOWNERS, the README ownership marker, the repository-facts overlay, and the
protected tests that pin these values.

The diff is larger, but it leaves no half-migrated state and requires no follow-up in
another repository.

## Decision

Adopt Option 3.

This repository MUST name `ea-Mitsuoka/ai-dev-foundation` as its direct parent, and MUST
publish its Next.js SaaS family contract from
`.ai/contracts/templates/ea-mitsuoka/nextjs-saas-template/`.

The ADR-0005 exception is unchanged in substance and MUST keep all four of its
conditions: same-repository, GitHub Actions bot author, `chore/template_sync_` branch
into `main`, and a full 40-character direct-parent source commit. Only the two
owner-qualified operands move to `ea-Mitsuoka`. This decision does not widen the
exception.

The accepted lock commit is unchanged.
`53fadbe8d8dc5dd97a7dfb11d4ab17b2ba308d65` exists in `ea-Mitsuoka/ai-dev-foundation`, so
the repoint advances no inheritance state and re-verifies no blob.

An owner-qualified reference that records history MUST NOT be rewritten. `CHANGELOG.md`,
existing `.ai/decision-log.md` rows, and accepted ADR bodies keep the account that hosted
them.

The deploy pipeline reference `Yukihide-Mitsuoka/gcp-cicd-workflows@v1` in `README.md`
and `CLAUDE.md` is outside this decision. It is a tag-pinned reusable workflow, not an
inheritance edge, and repointing it requires first verifying that `@v1` exists under the
new account.

## Consequences

**Positive:**

- Scheduled Template Sync reads the foundation the owner maintains.
- `make doctor` passes: `readme ownership: OK: ea-Mitsuoka/nextjs-saas-template`.
- The ADR-0005 size exception can match again, so a mechanical foundation sync PR is not
  blocked by GR-020.
- Review routing resolves, because CODEOWNERS names the account that owns the repository.
- A child bootstrapped from the exported contract receives the correct owner-qualified
  path.

**Negative:**

- The repository now contains both spellings, and a reader must distinguish a current
  reference from a historical link.
- The deploy pipeline reference still names the former account, so `README.md` mixes a
  migrated inheritance reference with an unmigrated artifact reference.
- Rollback is a reviewed revert of this PR. It is mechanical and needs no coordination,
  because this repository has no child in the fleet.

**Follow-ups:**

- Verify the `gcp-cicd-workflows` `@v1` tag under the new account, then repoint that
  reference in a separate PR.
