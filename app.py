import streamlit as st

def main():
    st.title("Lower GI 2WW Triage Pathway")
    st.write("Answer all the questions below based on the patient's condition. The results will be displayed at the end.")

    # Initialize results
    results = []

    # Q1: Initial Presentation (Symptoms Check)
    st.header("Q1: Initial Presentation (Symptoms Check)")
    symptoms = st.multiselect(
        "Which of the following symptom(s) does the patient have? (Select all that apply)",
        [
            "Abdominal mass",
            "Change of bowel habit",
            "Unexplained weight loss",
            "Unexplained rectal bleeding",
            "Unexplained abdominal pain",
            "Iron-deficiency anaemia (IDA)",
            "Anaemia (in the absence of IDA)",
            "Incidental finding",
            "Rectal mass (FIT not required)",
            "Unexplained anal mass (FIT not required)",
            "Unexplained anal ulceration (FIT not required)"
        ]
    )

    # Add symptom-related notes to results
    if "Abdominal mass" in symptoms:
        results.append("CT required at PTL (if no index CT) after colonic investigation.")
    if "Iron-deficiency anaemia (IDA)" in symptoms:
        results.append("OGD required at PTL after colonic investigation.")
    if any(s in symptoms for s in ["Rectal mass (FIT not required)", "Unexplained anal mass (FIT not required)", "Unexplained anal ulceration (FIT not required)"]):
        results.append("Proceed to Rectal/Anal Mass Pathway.")
        handle_rectal_anal_mass_pathway(results)
        display_results(results)
        return

    # Q2: FIT Test Check
    st.header("Q2: Has the patient had a FIT test done?")
    fit_test = st.radio(
        "Has a FIT (Faecal Immunochemical Test) been performed and is there a ferritin level?",
        ["Yes (FIT result available and ferritin done)", "No (FIT <10 or not done at all)"]
    )

    if fit_test == "No (FIT <10 or not done at all)":
        handle_fit_less_than_10(results)
    else:
        handle_fit_greater_than_10(results)

    # Q6: Additional Must-Do Checks
    st.header("Q6: Additional Checks")
    if "Abdominal mass" in symptoms:
        results.append("Ensure CT at PTL (if no index CT).")
    if "Iron-deficiency anaemia (IDA)" in symptoms:
        results.append("Ensure OGD at PTL.")
    if fit_test == "No (FIT <10 or not done at all)":
        results.append("Primary Care can consider repeat FIT or NSS pathway. If symptoms persist, consider referral via routine pathway.")

    # Display Results
    display_results(results)

# Q2A: Rectal/Anal Mass Pathway
def handle_rectal_anal_mass_pathway(results):
    st.subheader("Q2A: Rectal/Anal Mass Pathway")
    suitable_fos = st.radio(
        "The patient has a rectal or anal mass, or anal ulceration. Are they suitable for urgent Flexible Sigmoidoscopy (FOS)?",
        ["Yes", "No"]
    )
    if suitable_fos == "Yes":
        results.append("Perform urgent FOS. If NAD, refer back to Primary Care.")
    else:
        results.append("Arrange Clinical Endoscopist Telephone Triage or urgent CR OPA.")

# Q2B: FIT <10 or No Ferritin Pathway
def handle_fit_less_than_10(results):
    st.subheader("Q2B: FIT <10 or No Ferritin Pathway")
    return_to_referrer = st.radio(
        "FIT <10 (or missing ferritin). Do you want to return to the referrer?",
        ["Yes", "No"]
    )
    if return_to_referrer == "Yes":
        results.append("Send template letter to Primary Care advising repeat FIT test or NSS pathway.")
    else:
        results.append("Proceed based on local exceptions or clinical judgment.")

# Q3 & Beyond: FIT ≥10 Pathway
def handle_fit_greater_than_10(results):
    st.subheader("Q3: Patient with FIT ≥10")
    high_risk = st.radio(
        "Does the patient have a WHO performance status of 3 or 4, significant comorbidities/dementia, or are they ≥80 years old?",
        ["Yes", "No"]
    )

    if high_risk == "Yes":
        results.append("Perform Telephone Triage for high-risk patients. Arrange CTC or CTAP if not suitable for endoscopy.")
    else:
        handle_fit_value_branching(results)

# Q4: FIT Value Branching
def handle_fit_value_branching(results):
    st.subheader("Q4: FIT Value Branching")
    fit_value = st.radio(
        "What is the patient’s FIT result range?",
        ["FIT 10–99", "FIT ≥100"]
    )
    if fit_value == "FIT 10–99":
        handle_fit_10_to_99(results)
    else:
        results.append("For FIT ≥100, book Colonoscopy. If not suitable, arrange alternative imaging.")

# Q4A: FIT 10–99 & Age/Symptom Sub‑Pathway
def handle_fit_10_to_99(results):
    st.subheader("Q4A: FIT 10–99 & Age/Symptom Sub‑Pathway")
    age_group = st.radio(
        "Select the patient’s age group and symptoms:",
        [
            "18–39 years old with NO rectal bleeding",
            "40–59 years old with rectal bleeding ± other symptoms",
            "≥60 years old with rectal bleeding ± other symptoms",
            "≥60 years old with NO rectal bleeding but other symptoms"
        ]
    )
    if age_group == "18–39 years old with NO rectal bleeding":
        results.append("Refer for Colon Capsule (max 7/week). If not suitable, proceed to Colonoscopy.")
    elif age_group == "40–59 years old with rectal bleeding ± other symptoms":
        results.append("Refer for Colonoscopy.")
    elif age_group == "≥60 years old with rectal bleeding ± other symptoms":
        results.append("Refer for CTC or Colonoscopy based on clinical judgment.")
    elif age_group == "≥60 years old with NO rectal bleeding but other symptoms":
        results.append("Colonoscopy is first choice. If not suitable, refer for CTC.")

# Display Results
def display_results(results):
    st.header("Results Summary")
    if results:
        st.write("### Based on your inputs:")
        for result in results:
            st.write(f"- {result}")
    else:
        st.write("No specific recommendations based on the provided answers.")

# Run the app
if __name__ == "__main__":
    main()
