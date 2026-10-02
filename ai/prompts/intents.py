INTENT_CATEGORIES = {
    "QUESTION": (
        "The user wants a specific fact, answer, value, definition, "
        "or piece of information."
    ),
    "EXPLANATION": (
        "The user wants to understand a concept, topic, idea, system, "
        "relationship, or process, especially how or why something works."
    ),
    "INSTRUCTION": (
        "The user wants guidance, steps, procedures, or a method for "
        "performing a task or accomplishing a goal."
    ),
    "CREATION": (
        "The user wants something produced, written, designed, generated, "
        "rewritten, transformed, or otherwise created."
    ),
    "CODING": (
        "The user wants programming or software engineering assistance, "
        "including implementation, architecture, code generation, APIs, "
        "frameworks, or technical design."
    ),
    "ANALYSIS": (
        "The user wants information, content, data, evidence, or an idea "
        "examined, interpreted, evaluated, diagnosed, or broken down."
    ),
    "COMPARISON": (
        "The user wants two or more options, concepts, products, approaches, "
        "technologies, or ideas compared to understand their differences "
        "or trade-offs."
    ),
    "TROUBLESHOOTING": (
        "The user is experiencing an error, failure, unexpected behavior, "
        "or technical problem and wants help identifying the cause or "
        "finding a solution."
    ),
    "CASUAL_CONVERSATION": (
        "The user is engaging in general conversation without a clear "
        "informational, analytical, or task-oriented objective."
    ),
    "CLARIFICATION": (
        "The user wants something previously discussed clarified, "
        "simplified, corrected, refined, expanded, or explained differently."
    ),
}


INTENT_DETECTION_PROMPT = """
## Intent Detection

Determine the primary intent of the user's latest message.

Your goal is to identify what the user is actually trying to accomplish,
not merely the surface wording of the message.

### Available Intents

{intent_categories}

### Core Rules

- Select exactly one intent.
- The selected intent must represent the user's primary objective.
- Treat the latest user message as the strongest signal of current intent.
- Use relevant conversation history to interpret the latest message.
- Do not classify a message in isolation when previous messages materially
  change its meaning.
- Resolve references such as "it", "that", "this", "the previous one",
  or "what about this" using relevant conversation context.
- Do not infer an intent that is not supported by the user's message.
- Do not choose an intent merely because a particular word appears in
  the message.
- Classify based on the user's goal rather than individual keywords.

### Intent Boundaries

#### QUESTION

Use QUESTION when the user primarily wants a specific answer or fact.

Examples:
- "What is Django?"
- "How many parameters does Gemma 3 12B have?"
- "What does this error mean?"

Do not use QUESTION when the user primarily wants a detailed explanation,
instructions, or troubleshooting.

#### EXPLANATION

Use EXPLANATION when the user primarily wants to understand how or why
something works.

Examples:
- "Explain how transformers work."
- "Why does Django use migrations?"
- "How does a SIM card work in a car?"

Use this when understanding is the primary objective rather than simply
receiving a short factual answer.

#### INSTRUCTION

Use INSTRUCTION when the user wants to know how to perform a task.

Examples:
- "How do I deploy my Django app?"
- "Show me how to create a React component."
- "What are the steps to set up Ollama?"

If the user is already experiencing a failure and wants to resolve it,
prefer TROUBLESHOOTING.

#### CREATION

Use CREATION when the user wants Aria to produce or transform something.

Examples:
- "Write a LinkedIn post."
- "Create a product description."
- "Rewrite this paragraph."
- "Generate a prompt for an image."

The primary objective must be producing or transforming an artifact.

#### CODING

Use CODING when programming or software engineering is the primary goal.

Examples:
- "Convert this JavaScript component to TypeScript."
- "Create a Django API endpoint."
- "How should I structure this Python project?"
- "Write the code for authentication."

Use TROUBLESHOOTING instead when the primary objective is fixing an
existing technical problem.

#### ANALYSIS

Use ANALYSIS when the user wants something examined or interpreted.

Examples:
- "Analyze this dataset."
- "What are the main problems in this architecture?"
- "Break down this research finding."
- "Review this product strategy."

Analysis may involve evaluation, but the primary objective is examination
rather than direct comparison between explicitly identified alternatives.

#### COMPARISON

Use COMPARISON when the user explicitly wants multiple things compared.

Examples:
- "Compare Gemma 3 and Llama 3."
- "What's the difference between Django and FastAPI?"
- "Compare these two architectures."

Use COMPARISON when understanding differences or trade-offs between
alternatives is the central goal.

#### TROUBLESHOOTING

Use TROUBLESHOOTING when something is not working as expected and the user
wants to diagnose or fix it.

Signals may include:
- errors
- failures
- unexpected behavior
- broken functionality
- incorrect output
- configuration problems
- deployment failures

Examples:
- "Why am I getting a 503 error?"
- "My Django migrations aren't working."
- "This code crashes when I run it."

Do not use TROUBLESHOOTING merely because the message contains an error
message. The user's actual goal must be diagnosing or resolving the problem.

#### CLARIFICATION

Use CLARIFICATION when the user is asking to modify their understanding
of something already discussed.

This includes requests to:
- clarify
- simplify
- explain differently
- correct
- refine
- expand
- rephrase
- make something shorter or more detailed

Examples:
- "What do you mean by that?"
- "Explain that more simply."
- "Can you clarify the second point?"
- "Make that shorter."

Use the preceding conversation to determine what "that" refers to.

#### CASUAL_CONVERSATION

Use CASUAL_CONVERSATION when the user is primarily engaging socially or
conversationally without a meaningful task or information-seeking goal.

Examples:
- "Hey."
- "How are you?"
- "That's interesting."
- "Good morning."

Do not use CASUAL_CONVERSATION simply because the message is short.

### Follow-Up Messages

For short follow-up messages, use the previous conversation to determine
the intent.

Examples:

Previous:
"Explain quantization."

User:
"What about 4-bit?"

Intent:
QUESTION or EXPLANATION depending on what the user is asking for.

Previous:
"Here's my Django error."

User:
"How do I fix it?"

Intent:
TROUBLESHOOTING.

Previous:
"Compare Gemma and Llama."

User:
"What about performance?"

Intent:
COMPARISON.

Previous:
"Explain React hooks."

User:
"Make that simpler."

Intent:
CLARIFICATION.

### Multiple Possible Intents

A message may contain signals for multiple intents.

When this happens:

1. Identify the user's primary objective.
2. Determine what outcome would satisfy the request.
3. Select the intent most directly associated with that outcome.
4. Do not select multiple intents.
5. Prefer the more specific intent when there is a clear distinction.

Examples:

"Explain this error and show me how to fix it."

Primary intent:
TROUBLESHOOTING

"Compare these frameworks and recommend how I should implement this."

Primary intent:
COMPARISON

"Explain this concept and give me an example."

Primary intent:
EXPLANATION

"Write the code and explain how it works."

Primary intent:
CODING

### Context and Intent

- Consider the current conversation when determining intent.
- Preserve the meaning of previous messages when the latest message is
  a follow-up.
- Do not allow older conversation context to override a clearly changed
  current request.
- If the user changes objectives, classify the new objective.
- If the user's intent cannot be reliably determined from the available
  context, choose the closest supported category rather than inventing
  information.

### Output

Return only the name of the selected intent.

Do not provide:
- explanations
- reasoning
- confidence scores
- additional text
- Markdown
- multiple intents

Valid output must be exactly one of the available intent names.
""".strip()