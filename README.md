# 🏥 Dscribe AI Discharge Summary Agent

«Safety-focused Agentic AI Workflow for Structured Clinical Discharge Summaries»

---

# 🚀 Project Overview

This project simulates an agentic AI workflow for generating structured discharge summary drafts from unstructured clinical source notes.

The workflow is designed with a strong emphasis on:

- 🛡️ Clinical Safety
- 🔍 Conflict Detection
- 💊 Medication Reconciliation
- 🚨 Clinician Escalation
- 📄 Structured Summary Generation
- 📊 Traceable Agent Execution

Instead of hallucinating missing clinical facts, the system explicitly escalates uncertain cases for clinician review.

---

# 🧠 System Architecture

Clinical Notes

      ↓
Extraction Agent

      ↓
Validation Layer

      ↓
Conflict Detection

      ↓
Medication Reconciliation

      ↓
Clinician Escalation

      ↓
Discharge Summary Generator

      ↓
Trace Logger


---

# ✨ Core Features

📌 Structured Clinical Extraction

The extraction layer identifies:

- Admission date
- Discharge date
- Diagnoses
- Pending results
- Allergy information

---

# 💊 Medication Reconciliation

The workflow detects:

- Added medications
- Removed medications
- Medication inconsistencies

---

# 🚨 Safety Escalation

Unsafe or incomplete discharge cases are escalated for clinician review instead of automatically resolved.

---

# 🔍 Conflict Detection

The validation layer identifies:

- Missing allergy information
- Multiple active diagnoses
- Incomplete discharge details

---

# 📊 Trace Logging

Every execution step is logged for:

- Transparency
- Observability
- Debugging support

---

# 🛡️ Safety Guardrails

The workflow intentionally prioritizes safety over automation.

Key Safety Principles

- ❌ No hallucinated medical information
- ⚠️ Explicit handling of missing values
- 🚨 Mandatory escalation for risky cases
- 📋 Transparent execution traces

---

# 🧰 Tech Stack

- Python
- Rule-Based Parsing
- JSON Output Generation
- Modular Agent Workflow
- Git & GitHub
- Termux (Mobile Development Environment)

---

# 📂 Project Structure

dscribe-ai-discharge-agent/

│

├── app.py

├── extractor.py

├── validator.py

├── escalation_tool.py

├── summary_generator.py

├── trace_logger.py

├── README.md

│

├── outputs/

│   ├── discharge_summary.txt

│   └── discharge_data.json

│

├── traces/

│   └── agent_trace.txt


---

# ▶️ Run the Project

python app.py

---

## 📤 Generated Outputs

📄 Text Discharge Summary

outputs/discharge_summary.txt

📊 Structured JSON Output

outputs/discharge_data.json

🧾 Agent Execution Trace

traces/agent_trace.txt

---

# ⚠️ Current Limitations

- OCR support is limited in the mobile Termux environment
- Extraction currently uses rule-based parsing
- Real hospital PDFs may require stronger OCR pipelines

---

# 🔮 Future Improvements

- 🤖 LLM-based extraction workflows
- 📄 Full OCR pipeline
- 🧠 Advanced diagnosis conflict reasoning
- 💉 Drug interaction API integration
- 📚 Learning loop from clinician corrections
- 📑 Improved PDF ingestion

---

# 👨‍💻 Author

Mittapelly Akhileshwar
Aspiring AI Engineer | AWS | Python | Machine Learning

---
