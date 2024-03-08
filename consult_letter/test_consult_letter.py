import pytest
from consult_letter import create_consult_letter
from openai_chat import chat_content

# Example test cases with inputs and expected outputs or verification logic
test_cases = [
    (
        {
            "user_info": {"name": "Dr. John Doe", "email": "drjohndoe@clinic.com"},
            "specialty": "Obstetrics & Gynecology (ObGyn)",
            "note_date": "2024/03/01",
            "note_content": {
            "Patient Name": "Jane",
            "Patient Age": None,
            "Gender": "female",
            "Chief Complaint": "OB consultation for pregnancy management with planned repeat cesarean section.",
            "History of Present Illness": None,
            "Past Medical History": "The patient had COVID-19 in 2021, after which she experienced heart pain, but subsequent evaluations by her family doctor and hospital visits confirmed that everything was okay.",
            "Past Surgical History": "The patient had a cesarean section in 2019 and an abortion due to a fetal health issue.",
            "Family History": None,
            "Social History": "Jane is employed part-time as a banker, working two to three days per week. She and her spouse reside in a non-specified location without nearby family support. However, they have a local friend network. Postpartum, Jane's mother will assist, and they intend to employ a babysitter for two months.",
            "Obstetric History": "The patient is currently pregnant with her third child. She has had one previous live birth via cesarean section and one abortion due to fetal health issues. Her first child was born slightly premature at approximately 37 weeks, weighing 2.5 kilograms.",
            "The Review of Systems": "The patient reports no asthma, heart problems, seizures, or migraines. She has experienced chest pain post-COVID-19 but has been evaluated and found to be in good health. She is currently active, engaging in pregnancy yoga once a week and walking when she feels able.",
            "Current Medications": None,
            "Allergies": "The patient is allergic to minocycline.",
            "Vital Signs": None,
            "Physical Examination": None,
            "Investigations": None,
            "Problem": "1. Previous cesarean section (654.21)",
            "Differential Diagnosis": None,
            "Plan": "• Scheduled repeat cesarean section at 39 weeks gestation\n• Instructed patient to present to City Medical Center for emergency cesarean section if labor begins prior to scheduled date\n• Advised patient to walk daily for 20 to 30 minutes to improve blood pressure and baby's health\n• Arranged follow-up appointment in three weeks, with subsequent visits every two weeks, then weekly as due date nears",
            "Surgery Discussion": "• Purpose of the Surgery: The purpose of the repeat cesarean section is to safely deliver the baby, given the patient's previous cesarean delivery and her choice for a planned cesarean this time.\n• Risks and Complications: The risks of cesarean section include bleeding, infection, or injury to the bladder or bowel. These risks are small but not zero.\n• Anesthesia: Spinal anesthesia will be used during the procedure, which will prevent pain but allow the patient to be awake.\n• Alternatives: N/A",
            },
            "verification_points": f"""\
Follow these test points when verify the consult letter:
- The letter shall have doctor's name "John Doe"
- The letter shall mention patient name as Jane, and the encounter happened at 2024/03/01
- The Patient had COVID-19 in 2021 with subsequent heart pain but found okay.
- The patient had a cesarean section in 2019 and an abortion due to a fetal health issue.
- Allergic to minocycline.
"""
        },
        "PASS"  # Expected verification result
    ),
    # Add more test cases as needed
]

@pytest.mark.parametrize("input_data,expected_verification_result", test_cases)
def test_create_consult_letter_with_verification(input_data, expected_verification_result):
    # Unpack input data
    user_info = input_data["user_info"]
    specialty = input_data["specialty"]
    note_date = input_data["note_date"]
    note_content = input_data["note_content"]

    # Generate the consultation letter
    consult_letter = create_consult_letter(user_info, specialty, note_date, note_content)

    #this is just a debug log, you can also avoid it.
    print(consult_letter)

    result = chat_content(
        messages=[
            {
                "role": "system",
                "content": f"You are a professional medical assistant of Obstetrics & Gynecology (ObGyn), \
your job is to verify the content of consult letter",
            },
            {
                "role": "user",
                "content": f"""\
The consult letter is as following, delimited by ```:
```
{consult_letter}
```
""",
            },
            {
                "role": "user",
                "content": input_data["verification_points"],
            },
            {
                "role": "user",
                "content": "Write me PASS **ONLY** if the consult letter is correct, and FAIL with reason if not.",
            },
        ]
    )

    # Assert the expected verification result
    print(result)
    assert result.upper() == expected_verification_result
