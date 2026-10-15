1. We need to navigate to Chapter 18 -> Src -> Activate Venv
PS C:\Personal_Development\TheTestingAcademy\AI3xBatch> cd chapter_18_LangGraph
PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph> cd src
PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> python -m venv .venv
PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> .venv\Scripts\activate

2. Install Lang Graph
(.venv) PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> pip install -U langgraph

3. Command to run the programs
(.venv) PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> python .\001_Hello_Graph.py
The graph as Mermaid (paste into mermaid.live):
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        greet(greet)
        __end__([<p>__end__</p>]):::last
        __start__ --> greet;
        greet --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc

(.venv) PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> python .\002_Linear_Pipeline.py
(.venv) PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> python .\003_Conditional_Edge.py
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        read_result(read_result)
        log_pass(log_pass)
        file_bug(file_bug)
        quarantine(quarantine)
        __end__([<p>__end__</p>]):::last
        __start__ --> read_result;
        read_result -.-> file_bug;
        read_result -.-> log_pass;
        read_result -.-> quarantine;
        file_bug --> __end__;
        log_pass --> __end__;
        quarantine --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc

(.venv) PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> python .\004_Loop_Retry.py

4. Now we create a dummy Playwright project and run the flaky finder
For this we need to install these initially and then execute the script
(.venv) PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> pip install pytest pytest-playwright
(.venv) PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> python -m playwright install chromium

(.venv) PS C:\Personal_Development\TheTestingAcademy\AI3xBatch\chapter_18_LangGraph\src> python Project_PW_FlakyFinder.py
-- attempt 1: pytest test_login.py
   PASS  test_valid_login[chromium]
   FAIL  test_invalid_login[chromium]

-- attempt 2: pytest test_login.py::test_invalid_login[chromium]
   FAIL  test_invalid_login[chromium]

============================================================
VERDICT after 2 attempt(s)
============================================================
REAL FAILURE  test_invalid_login[chromium]  (red in all 2 attempt(s))
STABLE PASS   test_valid_login[chromium]

The graph as Mermaid (paste into mermaid.live):
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        run_tests(run_tests)
        read_report(read_report)
        summarise(summarise)
        __end__([<p>__end__</p>]):::last
        __start__ --> run_tests;
        read_report -.-> run_tests;
        read_report -.-> summarise;
        run_tests --> read_report;
        summarise --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc