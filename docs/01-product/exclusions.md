# Exclusions

This document lists what the NAS Intelligence Platform deliberately does not do in V1.

## Safety exclusions

- no permanent deletion;
- no silent overwrite;
- no silent removal of exact duplicates;
- no automatic near-duplicate cleanup;
- no live mutation without an approved immutable plan;
- no direct mutation from the Raspberry Pi sentinel;
- no authority bypass through dashboards or animations.

## Identity and privacy exclusions

- no unreviewed face recognition;
- no automatic sensitive identity assignment without explicit operator policy;
- no privacy-blind use of thumbnails, extracted text, GPS, or other sensitive metadata;
- no training on private media without an explicit privacy decision.

## Platform exclusions

- no live NAS access from the blueprinting process;
- no dependency installation as part of documentation work;
- no credentials, tokens, IP addresses, usernames, or private filenames in the repository;
- no cloud publishing or external upload automation unless separately approved later.

## Workflow exclusions

- no assumption that a successful dry run authorizes live rollout;
- no assumption that similarity equals duplication;
- no assumption that source discovery can skip unreadable or risky items;
- no assumption that a single successful batch validates the whole library.

## Architecture exclusions

- no design where the Raspberry Pi becomes the primary throughput engine;
- no design where the dashboard becomes the source of truth;
- no design where the plan can be changed after approval without creating a new version;
- no design where AI output alone can choose a live destination.

## Future-only items

The following are intentionally preserved for possible future consideration, not V1 activation:

- near-duplicate visual clustering;
- advanced face or identity recognition;
- semantic search and knowledge extraction;
- richer AI media understanding;
- remote mobile approvals;
- distributed workers;
- automated lifecycle policies;
- predictive capacity planning;
- cloud archive integration;
- broader household or business data governance.
