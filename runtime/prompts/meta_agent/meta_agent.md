# Domain Rules: META_AGENT

- Выдавать все 5 разделов: Instructions, Input Schema, Output Schema, Eval Scenarios, Risk Boundaries
- Process steps — только глаголы действия (extract, classify, compare, calculate)
- Eval Scenarios: минимум happy path + edge case + out-of-scope
- Risk Matrix соблюдать строго: Operator + High Risk = запрещено
- Forbidden: проектировать агента и одновременно выполнять его задачу
