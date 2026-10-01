Agent
  ↓
EvaluationRunner
  ↓
├── Deterministic Evaluators
├── LLM Evaluator
  ↓
EvaluationResult[]
  ↓
Aggregator
  ↓
Quality Gate


#camparing agents
                   Agent
                     │
                     ▼
              Evaluation Dataset
                     │
                     ▼
                 Run #001
                     │
                     ▼
                 runs/*.json
                     │
             Change agent
                     │
                     ▼
                 Run #002
                     │
                     ▼
                 runs/*.json
                     │
                     ▼
               COMPARATOR
                 /       \
                /         \
               ▼           ▼
         Metric-level    Case-level
          comparison      comparison
               │              │
               ▼              ▼
          "Overall +5%"   "case_017 -20%"


# Our AI EVALUATION SYSTEM
                    AI Evaluation System
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   Evaluation          Scoring           Persistence
     Engine             Engine               │
        │                  │                  ▼
        │                  │             Evaluation
        │                  │                Runs
        │                  │                  │
        └──────────────┬───┴──────────────────┘
                       ▼
                  Comparison
                       │
              ┌────────┴────────┐
              ▼                 ▼
          Aggregate          Case-level
          regression         regression