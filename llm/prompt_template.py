def generate_prompt(patient_data):
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
1. Summary of the basic patient information e.g vitals, 
2. Diagnosis - the name of the diagnosis
3. More information about the diagnosis - simple (layman's) explanation about the diagnosis
4. Tests ordered and results and what they mean (if any)
5. Treatment plan - instead of listing the drugs given to the patient, figure out what drug class they belong to and explain the purpose of the drug class.
6. Provide lifestyle recommendations on what to do to prevent re-occurrence of the disease (if any) or alleviate the disease in cases of chronic illnesses
7. Inform the patient of emergency signs to look out for the particular diagnosis (if any)

### **Patient Details**
- **Age**: {patient_data.get('age', 'N/A')}
- **Gender**: {patient_data.get('gender', 'N/A')}
- **Vitals**: BP: {patient_data.get('blood_pressure', 'N/A')}, Heart Rate: {patient_data.get('heart_rate', 'N/A')}, Temperature: {patient_data.get('temperature', 'N/A')}

### **Diagnosis**
The patient has been diagnosed with **{patient_data.get('diagnosis', 'N/A')}**.

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