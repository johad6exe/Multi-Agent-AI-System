# 🧪 System Evaluation Dataset & Methodology

This document outlines the rigorous testing methodology used to verify the Multi-Agent architecture, semantic routing logic, and Two-Stage RAG pipeline. 

Unlike standard "happy path" testing, this matrix intentionally incorporates adversarial edge cases, temporal illusions, and prompt injections to prove the resilience of the Coordinator's negative constraints.

## 🚀 How to Execute the Test Suite

The evaluation is fully automated via a CI-style Python script. To run the automated grading pipeline and verify the 100% pass rate locally, execute:

```bash
python -m src.evaluate