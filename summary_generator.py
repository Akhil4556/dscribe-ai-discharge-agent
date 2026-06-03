def generate_summary(data, validation):

    summary = f"""
=============================
DISCHARGE SUMMARY DRAFT
=============================

Admission Date:
{data['admission_date']}

Discharge Date:
{data['discharge_date']}

Principal Diagnosis:
{', '.join(data['principal_diagnosis'])}

Secondary Diagnosis:
{', '.join(data['secondary_diagnosis'])}

Pending Results:
{', '.join(data['pending_results'])}

Allergies:
{data['allergies'] if data['allergies'] else 'MISSING'}

Medication Changes:
Added:
{validation['medication_review'][0]['added']}

Removed:
{validation['medication_review'][0]['removed']}

Conflicts / Safety Flags:
{validation['conflicts']}

FINAL STATUS:
REQUIRES CLINICIAN REVIEW
"""

    return summary
