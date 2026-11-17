---
name: genpark-outreach-warmer
description: B2B Cold Email Reputation and Domain Warm-up automation.
version: 1.0.0
---

# genpark-outreach-warmer

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.

## Overview
Email deliverability is the lifeblood of cold outbound marketing. This skill coordinates a swarm of GenPark agents to emulate human conversational behavior across hundreds of email inboxes. By writing personalized emails, marking them as 'Not Spam', and replying organically, it artificially builds domain reputation to guarantee high primary inbox placement rates.

## Core Capabilities
- **Peer-to-Peer Sending**: Distribute emails among a controlled network of inboxes to build sending history safely.
- **Spam Trap Recovery**: Monitor if emails land in the spam folder, move them to the inbox, and mark them as important.
- **Natural Language Replies**: Read incoming warm-up emails and generate contextual, unique replies to mimic organic human communication.

## Usage Guide
When starting a warm-up campaign:
1. Ensure IMAP/SMTP details are provided for the target inbox.
2. Determine the daily ramp-up limit (e.g., Day 1: 5 emails, Day 2: 10 emails).
3. Draft dynamic, conversational strings (no direct selling) for the warm-up cycle.
4. Provide the user with a weekly deliverability health score metric.
