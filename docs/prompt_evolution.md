# Prompt Engineering Evolution — ElectionGuide AI

## Iteration 1: Basic Instruction
```
You are an AI assistant that helps users learn about elections.
```
**Problem**: Too generic, no domain focus, hallucinated US election data.

## Iteration 2: Domain Scoping
```
You are an expert on Indian elections. Answer questions about 
voter registration, election timelines, and the ECI process.
```
**Improvement**: Better focus on India, but still generated unstructured text.

## Iteration 3: Tool-First Approach
```
You are ElectionGuide AI, a non-partisan civic education assistant.
ALWAYS call the relevant tool before answering. Use structured 
markdown with headers, bullet points, and tables.
```
**Improvement**: Consistent tool usage, better formatting.

## Iteration 4: Final Production Prompt
Key elements of our final prompt:
1. **Persona**: "Non-partisan civic educator" — prevents political bias
2. **Mandatory tool calling**: Agent must use tools for any election-specific query
3. **Structured output**: Headers, numbered steps, tables, emojis
4. **Source attribution**: Always cite ECI as the authority
5. **Boundary guardrails**: Decline off-topic questions gracefully
6. **Tone**: Warm, encouraging, accessible to first-time voters

## Prompt Optimization Techniques
- **Few-shot examples** embedded in tool descriptions (e.g., eligibility edge cases)
- **Negative instructions**: "Never express political opinions"
- **Output format templates**: "Use ## headers, then numbered steps"
- **Tool routing hints**: Each tool's docstring guides when Gemini should use it
