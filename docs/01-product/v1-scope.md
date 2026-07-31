# V1 Scope

## V1 objective

Version 1 establishes the safe blueprint and the minimum operational surface needed to inventory, classify, plan, review, verify, and document NAS organization without relying on live destructive behavior.

## In scope

- read-only discovery of selected Synology shares;
- file and directory inventory;
- provenance capture and stable identities;
- timestamp, size, extension, MIME, and available media/document metadata extraction;
- cryptographic hashing and exact duplicate grouping;
- configurable rule-based classification;
- optional AI-assisted suggestions with confidence thresholds;
- destination preview and conflict detection;
- dry-run plans that never mutate the filesystem;
- manual review queue support;
- copied-data pilot design and documentation;
- approved copy/move batches with verification;
- append-only journals and checkpointing;
- pre/post reconciliation reports;
- continuous ingestion design;
- Raspberry Pi health monitoring and alerts.

## Out of scope for V1

- permanent deletion;
- automated near-duplicate deletion;
- unreviewed face or identity recognition;
- live broad reorganization on the first run;
- destructive renaming based only on AI guesses;
- modification of photo or video payloads;
- autonomous cloud uploads or external publishing;
- storing credentials in Git;
- direct filesystem mutation from the Raspberry Pi sentinel;
- training models on private media without explicit privacy approval.

## V1 operating gates

V1 must be designed around the following gates:

1. readiness;
2. read-only inventory;
3. dry run;
4. fixture tests;
5. copied pilot;
6. limited live pilot;
7. staged production;
8. reconciliation and steady state.

No gate authorizes the next one automatically. Each gate needs evidence, review, and explicit approval where appropriate.

## V1 deliverables

- source inventory and traceability records;
- versioned rule definitions;
- dry-run plan artifacts;
- review queue outputs;
- operation plan and batch records;
- execution and verification logs;
- reconciliation reports;
- rollback readiness evidence;
- monitoring and alerting expectations.

## V1 non-goals

V1 is not trying to:

- solve every possible taxonomy disagreement;
- infer private identity automatically;
- implement a general-purpose digital asset management product;
- optimize for full autonomy;
- replace human review with AI convenience;
- prove permanent cleanup or deletion workflows.

## V1 acceptance shape

The first release is acceptable only if it can demonstrate:

- source immutability during discovery and dry run;
- deterministic repeated scans;
- exact duplicate detection by hash;
- low-confidence and conflicting classifications going to review;
- immutable approved plans;
- collision safety;
- hash-verified execution;
- restart safety and reconciliation;
- total accountability for every in-scope item.

## Open decisions for V1

- exact pilot dataset selection;
- batch-size and stop-threshold calibration;
- copy-first versus move-first behavior in each rollout stage;
- quarantine retention and cleanup authorization;
- snapshot and rollback readiness requirements for the specific deployment;
- how much extracted text or thumbnail data, if any, the Mac mini may retain.
