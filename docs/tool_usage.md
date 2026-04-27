# Tool Usage Guide — ElectionGuide AI

## Overview

ElectionGuide AI uses **6 custom FunctionTools** registered with the Google ADK framework. Each tool provides structured, factual data about a specific election domain.

## Tool Descriptions

### 1. `get_election_timeline`
- **Domain**: Election calendar and scheduling
- **Trigger phrases**: "timeline", "schedule", "when", "phases", "dates"
- **Returns**: 9-stage election process with descriptions, key actors, and MCC details

### 2. `get_voter_registration_info`
- **Domain**: Voter enrollment and ID management
- **Parameters**: `registration_type` (new/correction/transfer/overseas)
- **Trigger phrases**: "register", "voter ID", "EPIC", "enrollment", "Form 6"
- **Returns**: Step-by-step registration guide with required documents

### 3. `get_nomination_process`
- **Domain**: Candidate filing procedures
- **Trigger phrases**: "nominate", "candidate", "file", "stand for election"
- **Returns**: Eligibility criteria, deposit amounts, affidavit requirements

### 4. `get_polling_day_guide`
- **Domain**: Election day procedures
- **Trigger phrases**: "polling day", "voting", "EVM", "VVPAT", "booth"
- **Returns**: Hour-by-hour polling guide, voter rights, EVM operation

### 5. `get_vote_counting_info`
- **Domain**: Results and counting process
- **Trigger phrases**: "counting", "results", "tally", "winner", "NOTA"
- **Returns**: Counting day procedures, EVM verification, result declaration

### 6. `check_voter_eligibility`
- **Domain**: Eligibility verification
- **Parameters**: `age` (int), `is_citizen` (bool), `has_criminal_record` (bool), `is_nri` (bool)
- **Trigger phrases**: "eligible", "can I vote", "qualifications"
- **Returns**: Eligibility assessment with reasoning and next steps

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
- "I'm 19, how do I register and what's the timeline?" → `check_voter_eligibility` + `get_voter_registration_info` + `get_election_timeline`
