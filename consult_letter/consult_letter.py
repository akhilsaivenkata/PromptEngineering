"""
Your task is to implement `create_consult_letter` function to generate a consult letter based on the SOAP note.

The input parameters are:
- user_info: a dictionary contains the bio of the doctor, such as
    {
        "name": "Dr. John Doe", # the name of the doctor
        "email": "drjohndoe@clinic.com", # the email of the doctor
    }
- specialty: a string represents the specialty of the doctor, such as "Obstetrics and Gynecology"
- note_content: a dictionary contains the content of the SOAP note, where the key is the section name and the value is the content of the section, such as
    {
        "Chief Complaint": "The patient is a 34-year-old G2P1 at 38 weeks gestation who presents for a routine prenatal visit.",
        "History of Present Illness": "The patient is a 34-year-old G2P1 at 38 weeks gestation who presents for a routine prenatal visit.",
        ...
    }
- note_date: a string represents the date of the SOAP note, such as "2022-01-01"
"""

import json
from typing import Optional
from openai import OpenAI
import openai
from datetime import datetime

client = OpenAI(
    # This is the default and can be omitted
    api_key="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",
)

def create_consult_letter(user_info, specialty, note_content, note_date):
    patient_details_formatted = json.dumps(note_content, indent=4)

    doctor_info_formatted = f"Doctor Name: {user_info['name']}\nDoctor Email: {user_info['email']}\nSpecialty: {specialty}\nConsultation Date: {note_date}"
    
    example_output = """Thank you for your referral of Betty, for Otolaryngology Consultation. She was examined on January 1, 2022.

    Betty presented with a chief complaint of left-sided ear pain, which worsens with chewing and is relieved when lying on the contralateral side. She reports intermittent hearing loss and has a history of inconsistent use of a mouthpiece for teeth clenching. There is no past medical or surgical history reported. Betty has an allergy to salt and occasionally uses Reactive for allergies. Her social history includes occasional use of Reactive for allergies.

    Upon examination, the ear canals and tympanic membranes were found to be clear and normal, with no signs of fluid or infection. There was pain along the pterygoid muscles, but the heart and lungs were clear, and there was no neck tenderness or lymphadenopathy. No investigations have been recorded at this time.

    The assessment suggests a likely diagnosis of temporomandibular joint disorder, given the jaw pain, history of teeth clenching, and normal ear examination. The plan includes ordering an audiogram to check her hearing, advising a visit to the dentist for temporomandibular joint evaluation, recommending ibuprofen for pain, and suggesting a soft foods diet. She has been advised to avoid chewing gum, hard candies, hard fruits, ice, and nuts, and to follow up if symptoms persist.

    Please note that there is no obstetric history, test results, estimated date of confinement, or past surgical history provided in the SOAP note. Therefore, these details are not included in this consultation letter.

    If you have any further questions or require additional information, please do not hesitate to contact me at drjohndoe@clinic.com.

    Sincerely,

    Dr. John Doe
    Otolaryngology
    drjohndoe@clinic.com"""
    # Prepare the chat messages for the API call
    messages = [
        {"role": "system", "content": "You are a professional medical assistant of Obstetrics & Gynecology (ObGyn), \
your job is to generate a consult letter "},
        {"role": "user", "content": f"Generate a medical consultation letter based on the following details:\n{doctor_info_formatted}\nPatient Details:\n{patient_details_formatted}"},
        {"role": "user", "content": f"consulation letter must only adhere to this specific format {example_output}"},

    ]

    # Call the chat completion API
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        temperature = 0.2,
        seed = 1
    )

    # Extract the generated consultation letter from the response
    consult_letter = response.choices[0].message.content

    return consult_letter

# Example usage of the function
if __name__ == "__main__":
    user_info = {
        "name": "Dr. John Doe",
        "email": "drjohndoe@clinic.com",
    }
    specialty = "Otolaryngology"
    note_date = "2024-01-01"
    note_content = {
    "Patient Name": "James",
    "Chief Complaint": "Recurrent headaches",
    "History of Present Illness": "\n• Recurrent tension-type headaches\n• Episodes last from 30 minutes to several hours\n• Typically bilateral with a pressing/tightening quality\n• No nausea or vomiting\n• Photophobia or phonophobia may be present\n• Frequency has increased over the past 2 months",
    "Social History": "\n• Works as a software developer\n• Reports high levels of work-related stress\n• Non-smoker\n• Exercises regularly",
    "The Review of Systems": "\n• No recent weight loss\n• Sleep patterns normal\n• No changes in vision\n• No history of seizures",
    "Current Medications": "\n• Occasional ibuprofen for pain relief",
    "Allergies": "\n• No known drug allergies",
    "Physical Examination": "\n• Blood pressure within normal range\n• No neck stiffness\n• Cranial nerves intact\n• No focal neurological deficits\n• Tenderness observed in the pericranial muscles\n• Examination of the eyes, ears, nose, throat, and teeth revealed no abnormalities",
    "Assessment and Plan": "Problem 1:\nRecurrent tension-type headaches\nDDx:\n• Stress-related tension headaches\n• Migraine without aura (less likely due to absence of nausea/vomiting)\nPlan:\n- Continue monitoring headache frequency and severity\n- Recommended stress management techniques and regular exercise\n- Consider starting a headache diary\n- Scheduled follow-up in 6 weeks to reevaluate\n- May consider referral to neurology if no improvement or if headaches worsen\n- Educated patient on the importance of maintaining a regular sleep schedule and proper hydration\n- Advised against overuse of pain medication to avoid medication-overuse headaches"
    }

    '''note_content =  {
        "Patient Name": "Betty",
        "Chief Complaint": "Ear pain",
        "History of Present Illness": "\n• Left-sided ear pain\n• No drainage noted\n• Intermittent hearing loss reported\n• Pain worsens with chewing\n• Inconsistent use of mouthpiece for teeth clenching\n• Pain relief when lying on contralateral side",
        "Social History": "\n• Occasional Reactive use for allergies\n• Allergy to salt",
        "The Review of Systems": "\n• Intermittent hearing loss\n• No swallowing issues\n• No nasal congestion\n• Allergies present, takes Reactive occasionally",
        "Current Medications": "\n• Reactive for allergies",
        "Allergies": "\n• Allergic to salt",
        "Physical Examination": "\n• Right ear canal clear\n• Right tympanic membrane intact\n• Right ear space aerated\n• Left ear canal normal\n• Left eardrum normal, no fluid or infection\n• Nose patent\n• Paranasal sinuses normal\n• Oral cavity clear\n• Tonsils absent\n• Good dentition\n• Pain along pterygoid muscles\n• Heart and lungs clear\n• No neck tenderness or lymphadenopathy",
        "Assessment and Plan": "Problem 1:\nEar pain\nDDx:\n• Temporomandibular joint disorder: Likely given the jaw pain, history of teeth clenching, and normal ear examination.\nPlan:\n- Ordered audiogram to check hearing\n- Advised to see dentist for temporomandibular joint evaluation\n- Recommended ibuprofen for pain\n- Suggested soft foods diet\n- Avoid chewing gum, hard candies, hard fruits, ice, and nuts\n- Follow-up if symptoms persist"
    }'''
    '''note_content = {
    "Patient Name": "Sophia",
    "Chief Complaint": "Persistent lower back pain",
    "History of Present Illness": "\n• Persistent lower back pain for the last 6 months\n• Pain described as constant, aching, with intermittent sharp episodes\n• Pain exacerbated by sitting for long periods and by bending\n• Minimal relief from over-the-counter painkillers\n• No history of trauma or injury to the area\n• Pain interferes with daily activities and sleep",
    "Social History": "\n• High school teacher\n• Recently started working from home, leading to increased sedentary lifestyle\n• Non-smoker\n• Minimal physical activity due to pain",
    "The Review of Systems": "\n• No bladder or bowel incontinence\n• No fever, weight loss, or other systemic symptoms\n• No history of cancer",
    "Current Medications": "\n• Over-the-counter ibuprofen, as needed for pain",
    "Allergies": "\n• Penicillin - rash",
    "Physical Examination": "\n• Normal gait observed\n• Tenderness localized to the lower lumbar region\n• No visible deformities or swelling\n• Range of motion of the lumbar spine reduced due to pain\n• Straight leg raise test negative\n• Neurological examination of the lower extremities normal, with intact reflexes, sensation, and strength",
    "Assessment and Plan": "Problem 1:\nPersistent lower back pain\nDDx:\n• Mechanical lower back pain possibly due to poor ergonomics and sedentary lifestyle\n• Discogenic pain\n• Exclusion of serious pathology such as malignancy, infection, or significant neurological compromise\nPlan:\n- Recommend physical therapy focused on lumbar stabilization exercises and posture correction\n- Consider ergonomic assessment of work environment\n- Schedule MRI of the lumbar spine to rule out discogenic or other structural causes\n- Prescribe muscle relaxants for short-term relief\n- Advise on the importance of regular breaks and movement during the workday\n- Follow-up appointment in 4 weeks to assess response to treatment\n- Discuss potential referral to a pain specialist if no improvement"
    }'''
    
    #MODEL = "gpt-4-1106-preview"

    # Generate the consultation letter
    consult_letter = create_consult_letter(user_info, specialty, note_content, note_date)

    # Print the generated consultation letter
    print(consult_letter)


'''
def create_consult_letter(
    user_info: dict, specialty: str, note_content: dict[str, Optional[str]], note_date: str
) -> str:
    """
    Your prompts here
    """
'''