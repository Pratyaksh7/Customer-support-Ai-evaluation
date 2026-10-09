class TermSchemaValidator:

    CONDITIONAL_FIELDS = {
        "spv": [
            "spv_layers",
        ],
        "forward_contract": [
            "counterparty",
            "settlement_date",
        ],
        "direct_transfer": [],
    }

    def validate(self, actual: dict) -> list[dict]:
        results = []

        transfer_type = actual.get("transfer_type")

        if transfer_type not in self.CONDITIONAL_FIELDS:
            return results

        required_fields = self.CONDITIONAL_FIELDS[transfer_type]

        for field in required_fields:
            value = actual.get(field)

            passed = value is not None

            results.append({
                "field": field,
                "rule": "required",
                "passed": passed,
                "actual": value,
                "reason": (
                    f"{field} is required when "
                    f"transfer_type is '{transfer_type}'."
                    if not passed
                    else
                    f"{field} is present for "
                    f"transfer_type '{transfer_type}'."
                ),
            })

        return results



# validator = TermSchemaValidator()


# actual = {
#     "transfer_type": "spv",
#     "spv_layers": "single_layer",
#     "spv_setup_fee": "5%",
#     "spv_management_fee": None,
#     "carry": "0%",
# }

# results = validator.validate(actual)

# for result in results:
#     print(result)