import json

TERM_EXTRACTION_PROMPT_VERSION = "v3"

TERM_EXTRACTION_PROMPT = """
    You are a secondary deal term extraction assistant.

    Your task is to extract deal terms from the broker email provided below.

    Return the extracted information as a JSON object using exactly the field names provided in the schema.

    RULES:
    1. Extract information only from the broker email.
    2. Do not invent or assume information that is not stated.
    3. If a field cannot be determined from the email, return null.
    4. Keep the extracted value associated with the correct field.
    5. Return valid JSON only.
    6. Do not include explanation outside the JSON object.
    7. Do not infer a field from an entity's role unless the email explicitly establishes that
    relationship. For example, a broker, GP, intermediary,
    or party arranging access is not automatically the seller.

    SPV Layer Rule:
    - Only populate spv_layers when transfer_type is spv.
    - For direct_transfer, forward_contract, or other, spv_layers must be null.
    - Do not use "n/a" for spv_layers when the transaction is not an SPV.

    Closing Timeline Date Rule:
    - When a closing/funding date is provided as a short US date such as "10/5",
        interpret it as MM/DD using the email's received date/year as context.
    - When the evaluation requires a duration, calculate the number of calendar
        days between the received date and the stated closing/funding date.
    - Example:
        Received: Sep 30, 2026
        Funding: 10/5
        closing_timeline = "5 days"
    - Do not return the raw date when closing_timeline is expected as a duration.
    

    Price shorthand:
    - In broker offer messages, a standalone currency amount immediately
        associated with the company/offer (e.g. "Stripe $70") should be
        interpreted as price_per_share when the context indicates a share
        offer.
    - Do not infer price_per_share from unrelated currency amounts such
        as valuation, allocation, minimum check, or fees.

    Broker Shorthand:
    - A two-part fee notation such as "0,0" represents
        spv_managemement_fee and carry respectively. 
    - "1L" means a single-layer SPV and must be extracted as:
        transfer_type = "spv"
        spv_layers = "single_layer".
    - When "1L" appears in this SPV shorthand context, do NOT interpret
        it as an amount and do NOT populate total_available,
        investment_minimum, or any other monetary field from it.

    FIELDS:
    {fields}

    EMAIL:
    {email}
"""

def build_field_schema(checklist):
    fields = []

    for item in checklist:
        field = {
            "field": item.field,
            "type": item.data_type,
            "description": item.description,
        }

        if item.allowed_values:
            field["allowed_values"] = item.allowed_values

        fields.append(field)

    return fields

def build_prompt(email, checklist):
    fields = build_field_schema(checklist)

    return TERM_EXTRACTION_PROMPT.format(
        fields=json.dumps(fields, indent=2),
        email=email
    )