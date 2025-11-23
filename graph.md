```
flowchart TD

    A[User Query] --> B[Router Node\n(Task + Relevance Check)]

    B -->|Needs Retrieval| C[RAG Agent\n(Search + Retrieve)]
    B -->|Direct Processing| D[Reasoning Agent]
    B -->|Irrelevant / Low Quality| K[Clarification Request]

    C --> D
    D --> E[Evaluation / Critic Node]

    E -->|Negative\nNeeds Revision| B
    E -->|Positive| F[Report Generator]

    F --> G[Final Output]

    %% Optional domain agents
    D --> H[Medical Agent Consultant]
    D --> I[Reasoning Sub-Agent]
    C --> J[Knowledge Tools]

```