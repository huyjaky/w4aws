**Tool Name**: Think
**Description**: Use this tool ONLY as a preliminary reasoning step for highly complex, ambiguous, or multi-step problems that require deep analysis before generating a final answer. 

**CRITICAL ROUTING RULES (When to use vs. When NOT to use):**

- **USE `Think` WHEN:** 1. The user asks for a complex root-cause analysis involving multiple systems (e.g., "Analyze how the database lock cascaded into the PaymentGW outage").
  2. The query requires evaluating architectural trade-offs or designing a new solution.
  3. The request involves synthesizing heavily conflicting data where you need a "scratchpad" to map out the logic first.
  4. The user explicitly asks you to "think step-by-step" or "plan".

- **DO NOT USE `Think` WHEN:**
  1. The user asks a direct, straightforward factual question (e.g., "What is the authentication method?", "Who is the team responsible?"). Route these directly to `RAG`.
  2. The user asks for a simple metric or status (e.g., "What is the current latency?", "What was the total cost in March?"). Route these directly to `Live HTTP APIs` or `Postgresql tool`.

**Input**: A detailed string outlining the specific problem statement, the known variables, and the goal of the reasoning process.
