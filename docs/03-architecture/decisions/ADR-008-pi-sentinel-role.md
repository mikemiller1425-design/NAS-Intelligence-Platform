# ADR 008: Raspberry Pi Sentinel role

Status: Accepted (foundation candidate)

## Context
A lightweight always-on device is useful for monitoring and alerting, but it should not become a hidden authority for destructive work.

## Decision
The Raspberry Pi is assigned a Sentinel role only: watch, alert, report, and stay out of destructive authorization.

## Consequences
This gives continuous visibility without risking unsafe autonomy. The Pi remains operationally useful even if the primary worker is offline.

## Alternatives considered
Using the Pi as the main worker or as a failover executor for destructive actions.
