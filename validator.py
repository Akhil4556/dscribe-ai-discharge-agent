def validate_data(data):

    conflicts = []

    medication_review = []

    # Conflict detection
    if (
        "Acute Gastroenteritis"
        in data["principal_diagnosis"]

        and

        "Urinary Tract Infection"
        in data["secondary_diagnosis"]
    ):

        conflicts.append(
            "Multiple active diagnoses detected"
        )

    # Allergy safety
    if data["allergies"] == "":
        conflicts.append(
            "Allergy information missing"
        )

    # Medication reconciliation
    admission_meds = ["Metformin"]

    discharge_meds = [
        "Metformin",
        "Oflox TZ"
    ]

    added = []

    removed = []

    for med in discharge_meds:

        if med not in admission_meds:
            added.append(med)

    for med in admission_meds:

        if med not in discharge_meds:
            removed.append(med)

    medication_review.append({
        "added": added,
        "removed": removed
    })

    return {
        "conflicts": conflicts,
        "medication_review": medication_review
    }
