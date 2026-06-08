"""
evaluate_system.py
──────────────────
End-to-end evaluation harness for the Research Multi-Agent System.

Checks:
  1. Routing accuracy   - did the Coordinator send the query to the right agent?
  2. Answer relevancy   - does the answer address the question using key expected terms?
  3. Hallucination guard - are known-wrong figures / claims absent from the answer?

Scoring:
  Each test case is worth a maximum of 10 points:
    • Routing correct  → +4 pts
    • Relevancy pass   → +4 pts
    • No hallucination → +2 pts
  Final score is reported as X / 100 (10 cases x 10 pts each).

Usage:
  python evaluate_system.py

Requirements:
  All the same dependencies as the main project (agno, lancedb, etc.).
  The knowledge base must already be ingested before running this script
  (i.e. `python -m RAG.ingest` must have been run at least once).
"""

import time
import textwrap
from dataclasses import dataclass, field
from typing import Optional

# ── project imports ────────────────────────────────────────────────────────────
from Agents.orchestrator import coordinator
from tracing.logger import setup_logger

logger = setup_logger("Evaluator")


# ══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class TestCase:
    id: int
    category: str                       # "RAG – NVIDIA" | "RAG – MSFT" | "GENERAL"
    query: str
    expected_agent: str                 # "Retriever_Agent" | "General_Agent"
    expected_keywords: list[str]        # ≥1 must appear in the answer (case-insensitive)
    forbidden_keywords: list[str] = field(default_factory=list)  # must NOT appear
    notes: str = ""                     # human-readable explanation of the test


@dataclass
class Result:
    case: TestCase
    raw_response: str
    agent_detected: Optional[str]
    routing_correct: bool
    relevancy_pass: bool
    hallucination_free: bool
    matched_keywords: list[str]
    forbidden_found: list[str]
    score: int                          # out of 10
    latency_s: float


# ══════════════════════════════════════════════════════════════════════════════
# TEST SUITE  (10 cases)
# ══════════════════════════════════════════════════════════════════════════════
#
# Ground-truth figures come directly from the uploaded 10-K filings:
#   NVIDIA  – FY2025 (fiscal year ended Jan 26, 2025)
#   Microsoft – FY2025 (fiscal year ended June 30, 2025)
#
TEST_CASES: list[TestCase] = [

    # ── RAG: NVIDIA ──────────────────────────────────────────────────────────

    TestCase(
        id=1,
        category="RAG - NVIDIA",
        query="What was NVIDIA's total revenue for fiscal year 2025?",
        expected_agent="Retriever_Agent",
        expected_keywords=["130", "497", "130,497", "130.5", "billion"],
        forbidden_keywords=["60,922", "26,974"],   # FY2024 / FY2023 – wrong year
        notes=(
            "FY2025 revenue = $130,497M (up 114% YoY). "
            "Tests whether the retriever pulls the correct year's figure."
        ),
    ),

    TestCase(
        id=2,
        category="RAG - NVIDIA",
        query="What was NVIDIA's gross margin percentage in fiscal year 2025 compared to fiscal year 2024?",
        expected_agent="Retriever_Agent",
        expected_keywords=["75", "72.7", "gross margin"],
        forbidden_keywords=[],
        notes=(
            "FY2025 GM = 75.0%, FY2024 GM = 72.7% (up 2.3 pts). "
            "Tests multi-year comparative retrieval and financial detail."
        ),
    ),

    TestCase(
        id=3,
        category="RAG - NVIDIA",
        query=(
            "What specific export control risks did NVIDIA disclose in their 10-K "
            "related to sales of chips like the H100 and A100 to China?"
        ),
        expected_agent="Retriever_Agent",
        expected_keywords=["export", "license", "china", "h100", "a100"],
        forbidden_keywords=[],
        notes=(
            "Risk factors section discusses USG licensing requirements for H100/A100 exports. "
            "Tests retrieval of qualitative risk disclosures, not just numbers."
        ),
    ),

    TestCase(
        id=4,
        category="RAG - NVIDIA",
        query="How much did NVIDIA spend on research and development in fiscal year 2025?",
        expected_agent="Retriever_Agent",
        expected_keywords=["12,914", "12.9", "research and development", "r&d"],
        forbidden_keywords=["8,675", "7,339"],   # FY2024 / FY2023 R&D figures
        notes=(
            "FY2025 R&D expense = $12,914M. "
            "Tests precise numeric retrieval from the income statement."
        ),
    ),

    TestCase(
        id=5,
        category="RAG - NVIDIA",
        query="What were NVIDIA's two reportable operating segments and their revenues in FY2025?",
        expected_agent="Retriever_Agent",
        expected_keywords=["compute", "networking", "graphics", "116,193", "14,304"],
        forbidden_keywords=[],
        notes=(
            "Compute & Networking = $116,193M; Graphics = $14,304M. "
            "Tests structured segment data retrieval."
        ),
    ),

    # ── RAG: Microsoft ────────────────────────────────────────────────────────

    TestCase(
        id=6,
        category="RAG - MSFT",
        query="What was Microsoft's total revenue and operating income for fiscal year 2025?",
        expected_agent="Retriever_Agent",
        expected_keywords=["281,724", "128,528", "operating income", "281"],
        forbidden_keywords=["245,122", "211,915"],   # FY2024 / FY2023 totals
        notes=(
            "FY2025 total revenue = $281,724M; operating income = $128,528M. "
            "Tests correct year selection across multi-year income statement."
        ),
    ),

    TestCase(
        id=7,
        category="RAG - MSFT",
        query=(
            "How much revenue did Microsoft's Intelligent Cloud segment generate in "
            "fiscal year 2025, and what drove the growth?"
        ),
        expected_agent="Retriever_Agent",
        expected_keywords=["106,265", "intelligent cloud", "azure", "21%", "34%"],
        forbidden_keywords=["87,464"],   # FY2024 Intelligent Cloud revenue
        notes=(
            "Intelligent Cloud FY2025 = $106,265M (+21% YoY); Azure grew 34%. "
            "Tests segment-level retrieval with growth drivers."
        ),
    ),

    TestCase(
        id=8,
        category="RAG - MSFT",
        query=(
            "What cybersecurity and AI-related risks did Microsoft disclose in its "
            "fiscal year 2025 10-K filing?"
        ),
        expected_agent="Retriever_Agent",
        expected_keywords=["security", "risk", "ai", "compliance", "cyber"],
        forbidden_keywords=[],
        notes=(
            "Risk Factors section (Item 1A) covers AI misuse, cybersecurity breaches, "
            "and regulatory risks. Tests retrieval of qualitative disclosures."
        ),
    ),

    # ── GENERAL: Out-of-domain (must NOT go to retriever) ────────────────────

    TestCase(
        id=9,
        category="GENERAL",
        query="What is the current stock price of NVIDIA today?",
        expected_agent="General_Agent",
        expected_keywords=["nvda", "nvidia", "stock", "price", "$"],
        forbidden_keywords=[],
        notes=(
            "Real-time price query → must route to General Agent (Tavily web search). "
            "Key routing boundary test: NVIDIA is in the RAG domain but this specific "
            "query requires live data."
        ),
    ),

    TestCase(
        id=10,
        category="GENERAL",
        query=(
            "If a company's revenue grows from $60.9 billion to $130.5 billion, "
            "what is the percentage growth? Show the working."
        ),
        expected_agent="General_Agent",
        expected_keywords=["114", "%", "growth", "calculation"],
        forbidden_keywords=[],
        notes=(
            "Pure math query → General Agent + CalculatorTools. "
            "Numbers deliberately mirror NVIDIA FY24→FY25 to test the router doesn't "
            "misfire toward Retriever just because the figures are familiar."
        ),
    ),
]


# ══════════════════════════════════════════════════════════════════════════════
# EVALUATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════

AGENT_SIGNATURES = {
    "Retriever_Agent": ["RETRIEVER AGENT", "📚 Evidence & Sources", "Document:"],
    "General_Agent":   ["GENERAL AGENT"],
}


def detect_agent(response_text: str) -> Optional[str]:
    """Heuristically identify which agent produced the response."""
    upper = response_text.upper()
    for agent, signatures in AGENT_SIGNATURES.items():
        if any(sig.upper() in upper for sig in signatures):
            return agent
    return None


def check_relevancy(response_text: str, keywords: list[str]) -> tuple[bool, list[str]]:
    """Return (passed, matched_keywords). At least one keyword must match."""
    lower = response_text.lower()
    matched = [kw for kw in keywords if kw.lower() in lower]
    return bool(matched), matched


def check_hallucination(response_text: str, forbidden: list[str]) -> tuple[bool, list[str]]:
    """Return (clean, found_forbidden). clean=True means no forbidden term appeared."""
    lower = response_text.lower()
    found = [kw for kw in forbidden if kw.lower() in lower]
    return not bool(found), found


def score_result(routing_correct: bool, relevancy_pass: bool, hallucination_free: bool) -> int:
    pts = 0
    if routing_correct:    pts += 4
    if relevancy_pass:     pts += 4
    if hallucination_free: pts += 2
    return pts


def run_query(query: str) -> tuple[str, float]:
    """Run a query through the coordinator and return (response_text, latency_seconds)."""
    t0 = time.perf_counter()
    # coordinator.run() returns an agno RunResponse object
    response = coordinator.run(query)
    latency = time.perf_counter() - t0

    # Extract plain text from the response
    if hasattr(response, "content") and response.content:
        text = str(response.content)
    elif hasattr(response, "messages") and response.messages:
        # fall back to last message content
        text = str(response.messages[-1].content)
    else:
        text = str(response)

    return text, latency


def evaluate_all() -> list[Result]:
    results: list[Result] = []

    for tc in TEST_CASES:
        logger.info(f"\n{'─'*60}")
        logger.info(f"Running Test {tc.id:02d} [{tc.category}]: {tc.query[:70]}...")

        try:
            raw, latency = run_query(tc.query)
        except Exception as exc:
            logger.error(f"  Query failed with exception: {exc}")
            raw = f"[ERROR: {exc}]"
            latency = 0.0

        agent_detected    = detect_agent(raw)
        routing_correct   = agent_detected == tc.expected_agent
        relevancy_pass, matched   = check_relevancy(raw, tc.expected_keywords)
        hallucination_free, found = check_hallucination(raw, tc.forbidden_keywords)
        pts               = score_result(routing_correct, relevancy_pass, hallucination_free)

        result = Result(
            case=tc,
            raw_response=raw,
            agent_detected=agent_detected,
            routing_correct=routing_correct,
            relevancy_pass=relevancy_pass,
            hallucination_free=hallucination_free,
            matched_keywords=matched,
            forbidden_found=found,
            score=pts,
            latency_s=latency,
        )
        results.append(result)

        # ── per-test summary ──────────────────────────────────────────────────
        routing_icon   = "✅" if routing_correct   else "❌"
        relevancy_icon = "✅" if relevancy_pass    else "❌"
        halluc_icon    = "✅" if hallucination_free else "❌"

        logger.info(f"  Routing   {routing_icon}  Expected={tc.expected_agent} | Got={agent_detected}")
        logger.info(f"  Relevancy {relevancy_icon}  Matched keywords: {matched or 'NONE'}")
        logger.info(f"  No halluc {halluc_icon}  Forbidden found: {found or 'none'}")
        logger.info(f"  Score: {pts}/10  |  Latency: {latency:.1f}s")

    return results


# ══════════════════════════════════════════════════════════════════════════════
# REPORT PRINTER
# ══════════════════════════════════════════════════════════════════════════════

def print_report(results: list[Result]) -> None:
    total_score = sum(r.score for r in results)
    max_score   = len(results) * 10

    routing_correct_count   = sum(1 for r in results if r.routing_correct)
    relevancy_correct_count = sum(1 for r in results if r.relevancy_pass)
    clean_count             = sum(1 for r in results if r.hallucination_free)
    avg_latency             = sum(r.latency_s for r in results) / len(results)

    divider = "═" * 70

    print(f"\n{divider}")
    print("  RESEARCH MULTI-AGENT SYSTEM — EVALUATION REPORT")
    print(divider)

    print(f"\n{'ID':<4} {'Category':<18} {'Routing':<10} {'Relevancy':<12} {'No Halluc':<12} {'Score':<8} {'Latency'}")
    print("─" * 70)
    for r in results:
        r_icon = "✅" if r.routing_correct   else "❌"
        v_icon = "✅" if r.relevancy_pass    else "❌"
        h_icon = "✅" if r.hallucination_free else "❌"
        print(
            f"{r.case.id:<4} {r.case.category:<18} {r_icon:<10} {v_icon:<12} "
            f"{h_icon:<12} {r.score}/10    {r.latency_s:.1f}s"
        )

    print(f"\n{divider}")
    print("  AGGREGATE SCORES")
    print(divider)
    print(f"  Overall Score      : {total_score} / {max_score}  ({100*total_score/max_score:.1f}%)")
    print(f"  Routing Accuracy   : {routing_correct_count}/{len(results)}  ({100*routing_correct_count/len(results):.0f}%)")
    print(f"  Answer Relevancy   : {relevancy_correct_count}/{len(results)}  ({100*relevancy_correct_count/len(results):.0f}%)")
    print(f"  Hallucination-Free : {clean_count}/{len(results)}  ({100*clean_count/len(results):.0f}%)")
    print(f"  Avg Latency        : {avg_latency:.1f}s")

    # ── failed cases detail ───────────────────────────────────────────────────
    failed = [r for r in results if r.score < 10]
    if failed:
        print(f"\n{divider}")
        print("  FAILED / PARTIAL CASES — DETAIL")
        print(divider)
        for r in failed:
            print(f"\n  [{r.case.id:02d}] {r.case.query[:80]}")
            print(f"       Category   : {r.case.category}")
            print(f"       Notes      : {r.case.notes}")
            if not r.routing_correct:
                print(f"       ❌ Routing  : expected={r.case.expected_agent} | got={r.agent_detected}")
            if not r.relevancy_pass:
                print(f"       ❌ Relevancy: none of {r.case.expected_keywords} matched")
            if not r.hallucination_free:
                print(f"       ❌ Hallucin : forbidden terms found → {r.forbidden_found}")
            print(f"       Score: {r.score}/10")
            # print first 400 chars of the response for quick inspection
            snippet = textwrap.fill(r.raw_response[:400].replace("\n", " "), width=66, initial_indent="       │ ", subsequent_indent="       │ ")
            print(f"       Response snippet:\n{snippet}")

    # ── grade ─────────────────────────────────────────────────────────────────
    pct = 100 * total_score / max_score
    if   pct >= 90: grade = "A  — Production-ready"
    elif pct >= 75: grade = "B  — Strong; minor gaps"
    elif pct >= 60: grade = "C  — Functional; routing or retrieval needs tuning"
    elif pct >= 40: grade = "D  — Partial; significant issues"
    else:           grade = "F  — System not working as expected"

    print(f"\n  Grade : {grade}")
    print(f"{divider}\n")


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info("Starting evaluation — running 10 test cases against the live system...")
    logger.info("Make sure the knowledge base has been ingested (`python -m RAG.ingest`).\n")

    results = evaluate_all()
    print_report(results)