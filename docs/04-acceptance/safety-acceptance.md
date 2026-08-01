# Safety Acceptance

Safety acceptance focuses on the non-negotiable protections that keep the NAS protected while the blueprint is developed.

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| SAF-001 | Inventory is read-only. | Confirm no mutation commands are present in inventory flow. | Workflow review, inventory manifest. | BLOCKER | Required invariant |
| SAF-002 | Copy-before-delete is the default for every phase. | Review operation playbooks and live-data policy. | Playbooks, policy docs. | BLOCKER | Live data policy |
| SAF-003 | Source retirement requires hash verification, a passing preservation comparison, and explicit bound approval. | Inspect live migration and rollback docs, and the preservation model. | Approval record template, verification steps, comparison report schema. | BLOCKER | Live migration playbook, preservation-model |
| SAF-004 | Protected vaults are not overwritten by default. | Validate collision policy and destination rules. | Taxonomy and collision policy. | BLOCKER | Change control |
| SAF-005 | No secret material is committed. | Search repository for secrets patterns and real credentials. | Git policy, repo scan results. | BLOCKER | Git policy |
| SAF-006 | No live NAS mutation is authorized at any gate before G6, and no gate before G7 authorizes source retirement. | Read status, playbooks, and handoff docs. | Acceptance docs, project status. | BLOCKER | Governance docs |
| SAF-007 | Path traversal outside approved roots is rejected. | Test hostile paths in fixture requirements. | Security test requirements. | BLOCKER | Security policy |
| SAF-008 | AI output remains untrusted until validated. | Confirm validation requirement in prompts and policies. | Prompt specs, evidence standard. | MAJOR | Prompt set |
| SAF-009 | The sentinel cannot classify, approve, or mutate. | Audit sentinel playbook and authority order. | Sentinel playbook, authority-order. | BLOCKER | Sentinel playbook |
| SAF-010 | Permanent deletion remains disabled in V1. | Review all policy and acceptance files. | Governance docs, operations docs. | BLOCKER | Live data policy |
