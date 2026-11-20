# Security Policy

## Reporting a vulnerability

Please do not open a public issue for a security problem.

Report it privately using GitHub's **Report a vulnerability** button on the
repository's **Security** tab. Include what you found, how to reproduce it,
and what you think the impact is.

## What to expect

This is a small open-source project maintained by one person, so there is no
guaranteed response time. Reports will be read, and confirmed problems will be
fixed as soon as practical.

## Scope

SkillProof's tools run in the browser, and nothing you paste is uploaded.
The main areas of concern are:

- Unsafe handling of pasted content in the web tools (for example script injection).
- Problems in the validator scripts or GitHub Actions workflows.

## Skills are untrusted content

Skills are instructions that an agent follows. Read any skill before you install it,
including the ones in this repository.
