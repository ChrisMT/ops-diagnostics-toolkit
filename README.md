# Ops Diagnostics Toolkit

A lightweight Python toolkit designed for quick triage of network connectivity and SSL certificate health across hybrid infrastructure.

## Context
In my role as a Senior Support Engineer, I frequently encounter incidents involving:
* Sudden API reachability failures.
* Unexpected SSL certificate expirations.
* Cross-region connectivity issues.

I built this tool to automate the initial "sanity check" phase of incident response, reducing the time spent manually running `curl` commands or checking browser locks.

## Features
* **Zero-Dependency:** Uses Python standard libraries (`ssl`, `socket`, `urllib`) for maximum portability on constrained Linux servers.
* **SSL validation:** specific checks for certificate expiration days.
* **HTTP Status:** Fast reporting on 200 vs 4xx/5xx errors.

## Usage
```bash
python3 monitor.py
