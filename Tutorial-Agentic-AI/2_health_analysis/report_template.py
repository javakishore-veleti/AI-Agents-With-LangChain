LAB_SECTIONS = [
    {
        "title": "COMPLETE BLOOD COUNT (CBC)",
        "divider": "######################################",
        "tests": [
            ("Hemoglobin", "e.g. 14.2 g/dL"),
            ("Hematocrit", "e.g. 42 %"),
            ("WBC", "e.g. 6.5 K/uL"),
            ("Platelets", "e.g. 250 K/uL"),
        ],
    },
    {
        "title": "LIPID PANEL",
        "divider": "###################",
        "tests": [
            ("Total Cholestrol", "e.g. 180 mg/dL"),
            ("LDL Cholestrol", "e.g. 100 mg/dL"),
            ("HDL Cholestrol", "e.g. 55 mg/dL"),
            ("Triglycerides", "e.g. 120 mg/dL"),
        ],
    },
    {
        "title": "METABOLIC PANEL",
        "divider": "###################",
        "tests": [
            ("Glucose (Fasting)", "e.g. 95 mg/dL"),
            ("HbA1c", "e.g. 5.4 %"),
            ("Creatinine", "e.g. 1.0 mg/dL"),
            ("eGFR", "e.g. 90 mL/min"),
        ],
    },
    {
        "title": "LIVER FUNCTION",
        "divider": "###################",
        "tests": [
            ("ALT", "e.g. 33 U/L"),
            ("AST", "e.g. 21 U/L"),
            ("Bilirubin Total", "e.g. 0.9 mg/dL"),
        ],
    },
]

DEFAULT_FORM_VALUES = {
    "patient_name": "John Smith",
    "age": "76",
    "gender": "Male",
    "report_date": "Dec 11, 2019",
    "physician": "Dr. Smith J",
    "Hemoglobin": "13.8 g/dL",
    "Hematocrit": "41 %",
    "WBC": "6.2 K/uL",
    "Platelets": "245 K/uL",
    "Total Cholestrol": "185 mg/dL",
    "LDL Cholestrol": "102 mg/dL",
    "HDL Cholestrol": "54 mg/dL",
    "Triglycerides": "118 mg/dL",
    "Glucose (Fasting)": "94 mg/dL",
    "HbA1c": "5.6 %",
    "Creatinine": "1.0 mg/dL",
    "eGFR": "88 mL/min",
    "ALT": "33 U/L",
    "AST": "21 U/L",
    "Bilirubin Total": "0.9 mg/dL",
}

# Backwards-compatible alias used by the app.
SAMPLE_FORM_VALUES = DEFAULT_FORM_VALUES


def all_test_names() -> list[str]:
    return [test for section in LAB_SECTIONS for test, _ in section["tests"]]


def build_report_text(
    patient_name: str,
    age: str,
    gender: str,
    report_date: str,
    physician: str,
    test_values: dict[str, str],
) -> str:
    lines = [
        f"Patient Name: {patient_name}, Age {age}, {gender}",
        f"Date: {report_date}",
        "",
    ]

    for section in LAB_SECTIONS:
        lines.extend(
            [
                section["divider"],
                f"{section['title']}:::",
                section["divider"],
            ]
        )
        for test_name, _ in section["tests"]:
            value = test_values.get(test_name, "").strip()
            lines.append(f"{test_name:<20}: {value}")
        lines.append("")

    lines.append(f"Reviewing Physician: {physician}")
    lines.append("")
    return "\n".join(lines)


def build_default_report_text() -> str:
    test_values = {
        test_name: DEFAULT_FORM_VALUES[test_name]
        for section in LAB_SECTIONS
        for test_name, _ in section["tests"]
    }
    return build_report_text(
        patient_name=DEFAULT_FORM_VALUES["patient_name"],
        age=DEFAULT_FORM_VALUES["age"],
        gender=DEFAULT_FORM_VALUES["gender"],
        report_date=DEFAULT_FORM_VALUES["report_date"],
        physician=DEFAULT_FORM_VALUES["physician"],
        test_values=test_values,
    )


DEFAULT_PASTE_REPORT = build_default_report_text()
