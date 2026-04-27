# Tool Usage Guide — ElectionGuide AI

## Overview

ElectionGuide AI uses **6 custom FunctionTools** registered with the Google ADK framework. Each tool provides structured, factual data about a specific election domain. All data is sourced from the Election Commission of India (ECI).

## Tool Descriptions

### 1. `get_election_timeline`
- **Domain**: Election calendar and scheduling
- **Parameters**: `election_type` (str: "general" | "state", default: "general")
- **Trigger phrases**: "timeline", "schedule", "when", "phases", "dates", "stages"
- **Returns**: 9-stage election process with descriptions, durations, and MCC details

### 2. `get_voter_registration_guide`
- **Domain**: Voter enrollment and ID management
- **Parameters**: `method` (str: "online" | "offline" | "both", default: "both")
- **Trigger phrases**: "register", "voter ID", "EPIC", "enrollment", "Form 6"
- **Returns**: Step-by-step registration guide, required documents, and forms list

### 3. `get_nomination_process`
- **Domain**: Candidate filing procedures
- **Parameters**: None
- **Trigger phrases**: "nominate", "candidate", "file", "stand for election"
- **Returns**: Eligibility criteria, deposit amounts, affidavit requirements, scrutiny process

### 4. `get_polling_day_guide`
- **Domain**: Election day procedures
- **Parameters**: None
- **Trigger phrases**: "polling day", "voting", "EVM", "VVPAT", "booth"
- **Returns**: 9-step voting guide, EVM/VVPAT info, do's and don'ts

### 5. `get_counting_process`
- **Domain**: Results and counting process
- **Parameters**: None
- **Trigger phrases**: "counting", "results", "tally", "winner", "NOTA"
- **Returns**: 5-stage counting process, key facts, roles, VVPAT verification

### 6. `check_eligibility`
- **Domain**: Eligibility verification
- **Parameters**: `age` (int), `citizenship` (str, default: "indian"), `purpose` (str: "voting" | "lok_sabha" | "state_assembly" | "local_body", default: "voting")
- **Trigger phrases**: "eligible", "can I vote", "qualifications", "age"
- **Returns**: Eligibility assessment with reasoning, requirements, and next steps

## Tool Selection Flow

```
User Query → Gemini 2.5 Flash analyzes intent
    → Selects 0-2 tools based on query semantics
    → Executes tool(s) to get structured data
    → Synthesizes response using tool output + prompt constraints
    → Returns formatted markdown response
```

## Multi-Tool Scenarios

The agent can chain multiple tools for complex queries:
- "I'm 19, how do I register and what's the timeline?" → `check_eligibility` + `get_voter_registration_guide` + `get_election_timeline`
- "What happens after nomination and before polling?" → `get_nomination_process` + `get_polling_day_guide`
