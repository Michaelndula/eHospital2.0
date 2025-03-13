def generate_prompt(patient_data):
    """
    Generates a structured prompt for LLM based on patient data.
    """

    diagnoses = patient_data.get('diagnosis', [])
    if isinstance(diagnoses, str):
        try:
            diagnoses = eval(diagnoses)
        except:
            diagnoses = [diagnoses]

    formatted_diagnosis = ", ".join(diagnoses)

    prompt: str = f""" 
Hello, I need you to create a concise, patient-friendly explanation of the following medical 
encounter. Provided with the patient's details and the diagnosis, 
act as a medical assistant explaining the diagnosis and treatment to the patient. 

General guidelines for the explanation include:
- Keep messages concise in a brief paragraph 200 characters for SMS.
- Use simple, non-technical language.
- Provide actionable advice or reminders.
- Use a friendly and respectful tone.

The message should include: 
1. Summary of the basic patient information e.g vitals, Compare the provided patient vitals against these normal ranges: 
   - Blood pressure: 90/60 - 120/80 mmHg
   - Heart rate: 60-100 bpm
   - Temperature: 36.1 - 37.2°C (97 - 99°F)
   - Oxygen saturation (SpO₂): 95-100%
   - Respiratory rate: 12-20 breaths per minute
2. Diagnosis - **all** diagnoses provided in a list.
3. More information about the diagnosis - simple (layman's) explanation about each diagnosis.
4. Tests ordered and results and what they mean (if any).
5. Treatment plan - instead of listing the drugs given to the patient, figure out what drug class they belong to and explain the purpose of the drug class.
6. Provide lifestyle recommendations on what to do to prevent re-occurrence of the disease (if any) or alleviate the disease in cases of chronic illnesses.
7. Inform the patient of emergency signs to look out for the particular diagnosis (if any).

### **Patient Details**
- **Age**: {patient_data.get('age', 'N/A')}
- **Gender**: {patient_data.get('gender', 'N/A')}
- **Vitals**: BP: {patient_data.get('blood_pressure', 'N/A')}, Heart Rate: {patient_data.get('heart_rate', 'N/A')}, Temperature: {patient_data.get('temperature', 'N/A')}

### **Diagnoses**
The patient has been diagnosed with **{formatted_diagnosis}**.

### **Tests Ordered & Results**
{format_tests(patient_data.get('tests', []))}

### **Treatment**
- **Medications**: {", ".join(patient_data.get('medications', ['No medications prescribed.']))}
"""
    return prompt


def format_tests(tests):
    """
    Converts a list of test dictionaries into a formatted string dynamically.
    """
    if not tests:
        return "No tests ordered."

    test_summary = ""
    for test in tests:
        test_name = test.get("name", "Unknown Test")
        reason = test.get("reason", "No reason provided")

        if "results" in test and isinstance(test["results"], list):
            results_list = [f"{r['parameter']}: {r['value']}" for r in test["results"]]
            results_text = "; ".join(results_list)
        else:
            results_text = "No result data available."

        test_summary += f"- **{test_name}**: {results_text} (Reason: {reason})\n"
    
    return test_summary