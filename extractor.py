def extract_sections(note):

    data = {
        "admission_date": "",
        "discharge_date": "",
        "principal_diagnosis": [],
        "secondary_diagnosis": [],
        "pending_results": [],
        "allergies": "",
        "requires_review": False
    }

    lines = note.split("\n")

    for line in lines:

        line = line.strip()

        if "Admission Date:" in line:
            data["admission_date"] = line.replace(
                "Admission Date:", ""
            ).strip()

        elif "Discharge Date:" in line:
            data["discharge_date"] = line.replace(
                "Discharge Date:", ""
            ).strip()

        elif "Acute Gastroenteritis" in line:
            data["principal_diagnosis"].append(
                line.replace("-", "").strip()
            )

        elif "Urinary Tract Infection" in line:
            data["secondary_diagnosis"].append(
                line.replace("-", "").strip()
            )

        elif "Type 2 Diabetes Mellitus" in line:
            data["secondary_diagnosis"].append(
                line.replace("-", "").strip()
            )

        elif "awaited" in line.lower():
            data["pending_results"].append(line)

        elif "Allergies:" in line:
            data["allergies"] = line.replace(
                "Allergies:", ""
            ).strip()

    if data["allergies"] == "Not documented":
        data["requires_review"] = True

    return data
