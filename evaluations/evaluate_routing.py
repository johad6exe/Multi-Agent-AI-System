import time
#module imports
from Agents.orchestrator import coordinator
from tracing.logger import sys_logger

EVALUATION_DATASET = [
    {
        "id": "Q1", 
        "query": "What was Nvidia’s total revenue in fiscal year 2025?", 
        "expected_answer": "$130,497 million (or $130.5 billion).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q2", 
        "query": "What were Microsoft's R&D expenses in fiscal year 2025?", 
        "expected_answer": "Microsoft reported $32.5 billion in R&D expenses for FY2025.",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"

    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    },
    {
        "id": "Q3", 
        "query": "Which company, Microsoft or Nvidia, saw a higher percentage growth in revenue between FY2024 and FY2025?", 
        "expected_answer": "Nvidia (114 percent growth) grew faster than Microsoft (15 percent growth).",
        "Agent" : "RETRIEVER"
    }
]

def run_automated_evaluation():
    print("\n" + "="*50)
    print("🧪 INITIALIZING AUTOMATED ROUTING EVALUATION")
    print("="*50 + "\n")
    
    passed_tests = 0
    total_tests = len(EVALUATION_DATASET)
    
    for test in EVALUATION_DATASET:
        print(f"Running {test['id']}...")
        print(f"Query: '{test['query']}'")
        
        try:
            # Pass the query to the Coordinator
            response = coordinator.run(test['query'])
            actual_route = response.content.strip().upper()
            
            # Grade the response
            if test['expected_route'] in actual_route:
                print(f"✅ PASS -> Routed correctly to {actual_route}\n")
                passed_tests += 1
            else:
                print(f"❌ FAIL -> Expected {test['expected_route']}, but got {actual_route}\n")
                
            # Sleep for 2 seconds to avoid hitting OpenRouter's free-tier rate limits!
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️ ERROR during execution: {str(e)}\n")

    print("="*50)
    print(f"📊 EVALUATION SCORE: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Temporarily mute our standard system logger so the evaluation prints cleanly
    sys_logger.setLevel("CRITICAL")
    run_automated_evaluation()