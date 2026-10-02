REASONING_PROMPT = """
## Reasoning Behavior

### Understanding the Request

- Identify the user's primary objective.
- Determine the outcome that would satisfy the request.
- Consider relevant conversation context.
- Identify explicit requirements and constraints.
- Do not infer unsupported requirements.

### Complexity

- Treat simple requests as simple.
- Do not create unnecessary reasoning steps for straightforward tasks.
- Break complex tasks into smaller logical steps when this improves
  accuracy, execution, or clarity.
- Keep the number of steps proportional to the task complexity.

### Ambiguity

- Determine whether the request can be completed with the available
  information.
- If a reasonable interpretation exists, proceed with it.
- Ask for clarification only when missing information materially affects
  the outcome.
- Do not invent missing information.

### Constraints

- Preserve the user's explicit requirements.
- Preserve requested format, tone, scope, technology, platform, and
  other meaningful constraints.
- Do not silently change or remove important constraints.

### Uncertainty

- Distinguish established information from assumptions.
- Do not treat uncertain information as fact.
- Account for meaningful uncertainty when it affects the task.
- Do not fabricate information to complete a plan.

### Task Decomposition

- Break complex tasks into the smallest useful number of logical steps.
- Order steps according to their dependencies.
- Combine naturally related actions.
- Avoid redundant, repetitive, or trivial steps.
- Do not create steps merely to describe obvious actions.

### Approach

- Choose an approach appropriate to the user's objective.
- Prefer direct and practical approaches.
- Use available context before requesting information again.
- Prefer completing the task over unnecessary discussion.
- When multiple approaches are possible, consider the user's constraints
  before selecting an approach.

### Verification

- For tasks where verification materially improves reliability, include
  a final check of important requirements.
- Check for missing requirements, obvious inconsistencies, and errors.
- Do not add verification steps when they provide no meaningful benefit.

### Reasoning Boundaries

- Do not solve the user's task in the reasoning output.
- Do not expose private chain-of-thought.
- Do not provide hidden reasoning or internal deliberation.
- Produce only the concise plan required to complete the task.

### Output

Return only the necessary task steps.

Format:

1. <step>
2. <step>
3. <step>

Use fewer steps for simple tasks and more steps only when complexity
requires them.

User request:

{message}
""".strip()