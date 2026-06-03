import json

from extractor import extract_sections
from validator import validate_data
from escalation_tool import escalate_to_clinician
from summary_generator import generate_summary
from trace_logger import save_trace

clinical_note = """
Admission Date: 12/05/2026
Discharge Date: 15/05/2026

Principal Diagnosis:
- Acute Gastroenteritis

Secondary Diagnosis:
- Urinary Tract Infection
- Type 2 Diabetes Mellitus

Admission Medications:
- Metformin

Discharge Medications:
- Metformin
- Oflox TZ

Pending Results:
- Urine culture awaited

Allergies:
- Not documented

Discharge Condition:
- Stable
"""

MAX_STEPS = 5
step_count = 0

trace = ""

print("STEP 1: Reading clinical note")
trace += "STEP 1: Reading clinical note\n"
step_count += 1

data = extract_sections(clinical_note)

print("\nSTEP 2: Structured extraction complete")
trace += "STEP 2: Structured extraction complete\n"
step_count += 1

validation = validate_data(data)

print("\nSTEP 3: Validation complete")
trace += "STEP 3: Validation complete\n"
step_count += 1

if validation["conflicts"]:
    escalate_to_clinician(
        validation["conflicts"]
    )

summary = generate_summary(
    data,
    validation
)

print("\nSTEP 4: Final discharge summary generated")
trace += "STEP 4: Final discharge summary generated\n"
step_count += 1

print(summary)

trace += "STEP 5: Agent terminated safely\n"
step_count += 1

if step_count >= MAX_STEPS:
    trace += "Agent step limit reached safely\n"

save_trace(trace)

with open(
    "outputs/discharge_summary.txt",
    "w"
) as file:

    file.write(summary)

with open(
    "outputs/discharge_data.json",
    "w"
) as file:

    json.dump(data, file, indent=4)

print("\nTrace saved successfully")
