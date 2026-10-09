# Normal Normalization:
#   Example: " Stripe " -> "stripe"
#   using def normalize_value(value):

# Field-Aware normalization.
# company_name
#     " Erebor Bank " → "erebor bank"

# percentage
#     "0" → "0%"

# enum
#     "single-layer" → "single_layer"

# currency
#     "$500k" → "$500K"   # if we decide this is canonical

# null
#     None / "" → None

import re


def normalize_value(field: str, value):

    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return None

    if field == "spv_layers":
        value = normalize_enum(value)

        if value == "n/a":
            return None

        return value

    if field in {
        "transfer_type",
        "spv_layers",
        "security_type",
        "seller_type",
    }:
        return normalize_enum(value)

    if field == "price_per_share":
        return normalize_price_per_share(value)

    if field in {
        "broker_fee",
        "spv_setup_fee",
        "spv_management_fee",
        "carry",
    }:
        return normalize_percentage(value)

    if field in {
        "investment_minimum",
        "implied_valuation",
        "total_available",
        "other_fees",
    }:
        return normalize_amount(value)

    return normalize_text(value)


def normalize_text(value):
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip().lower()
        value = re.sub(r"\s+", " ", value)

        return value or None

    return value


def normalize_enum(value):
    value = normalize_text(value)

    if value is None:
        return None

    aliases = {
        "single-layer": "single_layer",
        "single layer": "single_layer",
        "double-layer": "double_layer",
        "double layer": "double_layer",
        "direct transfer": "direct_transfer",
        "forward contract": "forward_contract",
    }

    return aliases.get(value, value)


def normalize_percentage(value):
    value = normalize_text(value)

    if value is None:
        return None

    value = re.sub(r"\s*(pts?|points?)$", "%", value)

    # "0" and "0%" represent the same percentage.
    if value == "0":
        return "0%"

    if re.fullmatch(r"\d+(\.\d+)?", value):
        return f"{value}%"

    return value


def normalize_amount(value):
    value = normalize_text(value)

    if value is None:
        return None

    # Remove commas from numeric amounts
    value = value.replace(",", "")

    # Normalize "mm" as million shorthand
    value = re.sub(
        r"(\d+(?:\.\d+)?)\s*[mM][mM]\b",
        r"\1M",
        value,
    )

    # Normalize K / M / B spacing and casing
    value = re.sub(r"(\d)\s*[kK]\b", r"\1K", value)
    value = re.sub(r"(\d)\s*[mM]\b", r"\1M", value)
    value = re.sub(r"(\d)\s*[bB]\b", r"\1B", value)

    # Convert shorthand amounts to a canonical full amount
    match = re.fullmatch(
        r"(\$?)(\d+(?:\.\d+)?)([KMB])",
        value,
        re.IGNORECASE,
    )

    if match:
        currency, number, suffix = match.groups()

        multiplier = {
            "K": 1_000,
            "M": 1_000_000,
            "B": 1_000_000_000,
        }[suffix.upper()]

        amount = float(number) * multiplier

        if amount.is_integer():
            amount = int(amount)

        return f"{currency}{amount:,}"

    # Normalize plain numeric amounts
    match = re.fullmatch(r"(\$?)(\d+(?:\.\d+)?)", value)

    if match:
        currency, number = match.groups()
        amount = float(number)

        if amount.is_integer():
            amount = int(amount)

        return f"{currency}{amount:,}"

    return value

def normalize_price_per_share(value):
    value = normalize_text(value)

    if value is None:
        return None

    value = re.sub(r"/\s*(share|shares)\b", "", value, flags=re.IGNORECASE )

    value = re.sub(r"\s+per\s+share\b", "", value, flags=re.IGNORECASE )

    value = re.sub(r"/\s*(share|shares|sh)\b", "", value, flags=re.IGNORECASE )

    return value