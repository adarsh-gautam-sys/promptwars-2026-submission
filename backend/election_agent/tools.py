"""
ElectionGuide AI — Custom Tools Module
Six FunctionTools providing structured election data for the agent.
All data sourced from Election Commission of India (ECI) official guidelines.
"""


def get_election_timeline(election_type: str = "general") -> dict:
    """Returns the complete Indian election timeline with all stages from announcement to results.

    Args:
        election_type: Type of election - 'general' for Lok Sabha, 'state' for State Assembly.

    Returns:
        Dictionary with election stages, descriptions, and typical durations.
    """
    stages = [
        {"stage": 1, "name": "Announcement of Schedule", "duration": "Day 0",
         "description": "The Election Commission of India (ECI) announces the election dates, including polling and counting dates. The Model Code of Conduct (MCC) comes into immediate effect."},
        {"stage": 2, "name": "Issue of Notification", "duration": "Day 1-7",
         "description": "Formal gazette notification is issued calling upon the constituency to elect a member. This officially starts the election process."},
        {"stage": 3, "name": "Filing of Nominations", "duration": "Day 7-14",
         "description": "Candidates file their nomination papers with the Returning Officer (RO). They must submit affidavits declaring assets, liabilities, criminal cases, and educational qualifications."},
        {"stage": 4, "name": "Scrutiny of Nominations", "duration": "Day 15",
         "description": "The Returning Officer examines all nomination papers for validity. Papers with substantial defects (wrong constituency, incomplete forms) are rejected."},
        {"stage": 5, "name": "Withdrawal of Candidature", "duration": "Day 17",
         "description": "Last date for candidates to withdraw their nominations. After this, the final list of contesting candidates is published."},
        {"stage": 6, "name": "Election Campaigning", "duration": "Day 17 to Day T-2",
         "description": "Candidates and parties campaign to persuade voters. Campaigning must stop 48 hours before polling ends (silence period). MCC governs all campaign conduct."},
        {"stage": 7, "name": "Polling Day (Voting)", "duration": "Day T",
         "description": "Voters cast their ballots at designated polling stations using Electronic Voting Machines (EVMs) with VVPAT verification. Polling typically runs 7 AM to 6 PM."},
        {"stage": 8, "name": "Vote Counting", "duration": "Day T + 2-3",
         "description": "Votes are counted at designated counting centers. Postal ballots are counted first, followed by EVM tallies round by round. Counting is done under supervision of the RO and observers."},
        {"stage": 9, "name": "Declaration of Results", "duration": "Same day as counting",
         "description": "The candidate with the highest votes in a constituency is declared winner by the RO. Results are published on the ECI website in real-time."},
    ]

    return {
        "status": "success",
        "election_type": "Lok Sabha (General)" if election_type == "general" else "State Assembly",
        "total_stages": 9,
        "stages": stages,
        "note": "The entire process typically spans 6-8 weeks from announcement to results.",
        "source": "Election Commission of India (eci.gov.in)",
    }


def get_voter_registration_guide(method: str = "both") -> dict:
    """Returns step-by-step voter registration guide for Indian elections.

    Args:
        method: Registration method - 'online', 'offline', or 'both'.

    Returns:
        Dictionary with registration steps, required documents, and form details.
    """
    online_steps = [
        {"step": 1, "action": "Visit the National Voters' Service Portal", "url": "https://voters.eci.gov.in"},
        {"step": 2, "action": "Click on 'Register as a New Voter' and select Form 6"},
        {"step": 3, "action": "Fill in personal details: name, date of birth, address, and family member details"},
        {"step": 4, "action": "Upload required documents: passport-size photo and age proof"},
        {"step": 5, "action": "Submit the form and note your reference number"},
        {"step": 6, "action": "Track status online or via the Voter Helpline App"},
        {"step": 7, "action": "After verification by BLO, your name appears in the electoral roll"},
    ]

    offline_steps = [
        {"step": 1, "action": "Obtain Form 6 from the local Electoral Registration Office or download from eci.gov.in"},
        {"step": 2, "action": "Fill in the form completely with correct details"},
        {"step": 3, "action": "Attach passport-size photographs and self-attested copies of documents"},
        {"step": 4, "action": "Submit to the Electoral Registration Officer (ERO) or Booth Level Officer (BLO)"},
        {"step": 5, "action": "A BLO will visit your residence to verify your details"},
        {"step": 6, "action": "After verification, your name is added to the electoral roll and EPIC (Voter ID) is issued"},
    ]

    forms = [
        {"form": "Form 6", "purpose": "New voter registration"},
        {"form": "Form 6A", "purpose": "Overseas (NRI) voter registration"},
        {"form": "Form 8", "purpose": "Correction of entries or shifting residence"},
        {"form": "Form 7", "purpose": "Objection to inclusion of a name in the electoral roll"},
    ]

    documents = [
        "Age proof: Birth certificate, School leaving certificate, or Passport",
        "Address proof: Aadhaar card, Utility bill, Bank passbook, or Ration card",
        "Passport-size photograph (recent)",
        "Identity proof: Aadhaar, PAN card, or Driving license",
    ]

    result = {"status": "success", "forms": forms, "required_documents": documents, "source": "ECI - voters.eci.gov.in"}
    if method in ("online", "both"):
        result["online_steps"] = online_steps
    if method in ("offline", "both"):
        result["offline_steps"] = offline_steps
    result["eligibility"] = "Indian citizen, aged 18+ as on qualifying date (Jan 1 / Apr 1 / Jul 1 / Oct 1)"
    result["helpline"] = "Call 1950 or use the Voter Helpline App"
    return result


def get_nomination_process() -> dict:
    """Returns detailed information about the candidate nomination process in Indian elections.

    Returns:
        Dictionary with eligibility, steps, security deposits, and scrutiny process.
    """
    return {
        "status": "success",
        "eligibility": {
            "lok_sabha": {"min_age": 25, "citizenship": "Indian citizen", "registered_voter": "Must be a registered voter in any constituency in India"},
            "state_assembly": {"min_age": 25, "citizenship": "Indian citizen", "registered_voter": "Must be a registered voter in any constituency in the state"},
            "disqualifications": [
                "Convicted with imprisonment of 2+ years",
                "Undischarged insolvent",
                "Not a citizen of India or acquired foreign citizenship",
                "Holds an office of profit under the government",
                "Dismissed from government service for corruption or disloyalty",
            ],
        },
        "steps": [
            {"step": 1, "action": "Obtain nomination form from the Returning Officer (RO)"},
            {"step": 2, "action": "Fill in details including name, address, party affiliation, and symbol"},
            {"step": 3, "action": "Get the nomination form signed by a proposer (registered voter in the constituency)"},
            {"step": 4, "action": "Submit mandatory affidavit declaring: criminal cases, assets & liabilities, educational qualifications"},
            {"step": 5, "action": "Pay the security deposit"},
            {"step": 6, "action": "File the nomination with the RO before the deadline"},
        ],
        "security_deposit": {
            "general_candidate": "₹25,000",
            "sc_st_candidate": "₹12,500",
            "refund_condition": "Deposit is refunded if the candidate secures more than 1/6th of total valid votes polled",
        },
        "scrutiny": "The RO examines all papers the day after the last date of filing. Papers with substantial defects are rejected. Candidates can present arguments during scrutiny.",
        "source": "ECI & Representation of the People Act, 1951",
    }


def get_polling_day_guide() -> dict:
    """Returns a complete guide for what happens on polling day, including EVM/VVPAT procedures.

    Returns:
        Dictionary with voting steps, do's and don'ts, and EVM/VVPAT information.
    """
    return {
        "status": "success",
        "voting_steps": [
            {"step": 1, "action": "Locate your polling station", "detail": "Check on voters.eci.gov.in or Voter Helpline App using your EPIC number"},
            {"step": 2, "action": "Carry valid ID", "detail": "EPIC (Voter ID), Aadhaar, Passport, DL, PAN card, or other ECI-approved photo ID"},
            {"step": 3, "action": "Queue at the polling station", "detail": "Polling hours are typically 7:00 AM to 6:00 PM. Anyone in queue by 6 PM can vote."},
            {"step": 4, "action": "Identity verification", "detail": "Polling officer checks your name on the electoral roll and verifies your identity"},
            {"step": 5, "action": "Indelible ink application", "detail": "Ink is applied to your left index finger to prevent double voting. The ink lasts ~4 weeks."},
            {"step": 6, "action": "Receive ballot slip", "detail": "You receive a voter slip and proceed to the voting compartment"},
            {"step": 7, "action": "Cast your vote on the EVM", "detail": "Press the button next to your chosen candidate's name and symbol on the Ballot Unit"},
            {"step": 8, "action": "Verify via VVPAT", "detail": "A printed slip appears in the VVPAT machine for 7 seconds showing your chosen candidate — verify it"},
            {"step": 9, "action": "Exit the polling station", "detail": "After voting, leave the polling station. Do not loiter or try to influence other voters."},
        ],
        "evm_info": {
            "full_form": "Electronic Voting Machine",
            "components": ["Control Unit (with Presiding Officer)", "Ballot Unit (in voting compartment)", "VVPAT (Voter Verifiable Paper Audit Trail)"],
            "capacity": "Up to 384 candidates per EVM",
            "tamper_proof": "EVMs are standalone, non-networked machines. They cannot be connected to the internet or hacked remotely.",
        },
        "dos": ["Carry valid photo ID", "Check your polling station in advance", "Vote in your designated booth only", "Verify your vote on the VVPAT slip"],
        "donts": ["Don't carry phones or cameras into the voting compartment", "Don't share whom you voted for inside the station", "Don't attempt to vote more than once", "Don't campaign near the polling station (within 100m)"],
        "source": "Election Commission of India",
    }


def get_counting_process() -> dict:
    """Returns detailed information about the vote counting process and result declaration.

    Returns:
        Dictionary with counting stages, postal ballot process, and VVPAT verification.
    """
    return {
        "status": "success",
        "counting_stages": [
            {"stage": 1, "name": "Postal Ballots", "description": "Postal ballots (from service voters, senior citizens, PWD voters) are counted first at a separate table."},
            {"stage": 2, "name": "EVM Round-wise Counting", "description": "EVMs are opened and counted in rounds. Each round covers a set of polling stations. Totals are announced after each round."},
            {"stage": 3, "name": "VVPAT Verification", "description": "VVPAT slips from 5 randomly selected polling stations per constituency are matched with EVM totals for verification."},
            {"stage": 4, "name": "Tabulation", "description": "All round-wise totals are tabulated. The RO prepares the final result sheet (Form 20)."},
            {"stage": 5, "name": "Declaration", "description": "The candidate with the highest total valid votes is declared elected. The RO issues the certificate of election."},
        ],
        "key_facts": [
            "Counting typically starts at 8:00 AM on counting day",
            "Candidate agents (representatives) are present at every counting table",
            "Any candidate can request a recount if the margin is very thin",
            "Results are uploaded in real-time on the ECI Results portal (results.eci.gov.in)",
            "The entire counting for a constituency usually completes in 6-8 hours",
        ],
        "roles": {
            "returning_officer": "Overall in-charge of counting in the constituency",
            "counting_supervisor": "Manages individual counting tables",
            "counting_agents": "Appointed by candidates to observe the process",
            "observers": "Appointed by ECI for impartial oversight",
        },
        "source": "ECI Counting Guidelines & Handbook for Returning Officers",
    }


def check_eligibility(age: int, citizenship: str = "indian", purpose: str = "voting") -> dict:
    """Checks voter or candidate eligibility based on age, citizenship, and purpose.

    Args:
        age: The person's current age in years.
        citizenship: Citizenship status - 'indian' or 'other'.
        purpose: What eligibility to check - 'voting', 'lok_sabha', 'state_assembly', or 'local_body'.

    Returns:
        Dictionary with eligibility status, requirements, and next steps.
    """
    citizenship = citizenship.lower().strip()
    purpose = purpose.lower().strip()

    result = {"status": "success", "age": age, "citizenship": citizenship, "purpose": purpose}

    if citizenship != "indian":
        result["eligible"] = False
        result["reason"] = "Only Indian citizens are eligible to vote or contest elections in India."
        result["next_steps"] = ["If you are an NRI with Indian citizenship, you can register as an overseas voter using Form 6A."]
        return result

    requirements = {
        "voting": {"min_age": 18, "label": "Voter"},
        "lok_sabha": {"min_age": 25, "label": "Lok Sabha Candidate"},
        "state_assembly": {"min_age": 25, "label": "State Assembly Candidate"},
        "local_body": {"min_age": 21, "label": "Local Body Candidate"},
    }

    req = requirements.get(purpose, requirements["voting"])

    if age >= req["min_age"]:
        result["eligible"] = True
        result["reason"] = f"At age {age}, you meet the minimum age requirement of {req['min_age']} years for {req['label']}."
        if purpose == "voting":
            result["next_steps"] = [
                "Register online at voters.eci.gov.in using Form 6",
                "Or download the Voter Helpline App",
                "Or visit your local Electoral Registration Office",
                "Keep your Aadhaar and age proof documents ready",
            ]
        else:
            result["next_steps"] = [
                "Ensure you are a registered voter",
                "Obtain nomination papers from the Returning Officer",
                "Prepare the mandatory affidavit",
                f"Arrange the security deposit ({'₹25,000' if purpose == 'lok_sabha' else '₹10,000'})",
            ]
    else:
        years_remaining = req["min_age"] - age
        result["eligible"] = False
        result["reason"] = f"At age {age}, you are {years_remaining} year(s) short of the minimum age {req['min_age']} for {req['label']}."
        result["next_steps"] = [f"You will be eligible in {years_remaining} year(s) when you turn {req['min_age']}.", "In the meantime, learn about the election process to be a well-informed future participant!"]

    result["source"] = "Constitution of India & Representation of the People Act, 1950/1951"
    return result
