from dataclasses import dataclass, field

@dataclass
class ChecklistItem:
    field: str
    data_type: str
    required: bool = True
    allowed_values: list[str] | None = None
    description: str | None = None
    required_if: tuple[str, str] | None = None

def get_default_checklist() -> list[ChecklistItem]:
    return [
        ChecklistItem(
            field="company_name",
            data_type="string",
            required=True,
            description=(
                "The company whose shares are being sold. Not the broker, "
                "the fund, the SPV, or the counterparty to a contract."
            ),
        ),
        ChecklistItem(
            field="investment_minimum",
            data_type="currency",
            required=True,
            description=(
                "The smallest cheque one buyer may write into this offer. "
                "Not the size of the whole allocation."
            ),
        ),
        ChecklistItem(
            field="price_per_share",
            data_type="currency",
            required=True,
            description=(
                "The headline price per share the buyer pays, before any "
                "fee. On a forward or synthetic structure, the referenced "
                "or equivalent per-share price."
            ),
        ),
        ChecklistItem(
            field="implied_valuation",
            data_type="currency",
            required=True,
            description=(
                "The company valuation this offer's price implies. Not the "
                "valuation of a past financing round."
            ),
        ),
        ChecklistItem(
            field="total_available",
            data_type="currency_or_shares",
            required=True,
            description=(
                "The size of the whole allocation on offer, as an amount "
                "or a share count. Not one buyer's minimum, and not a "
                "vehicle's layering -- \"1L\" in a broker's shorthand is a "
                "single-layer SPV, not one lakh and not one large."
            ),
        ),
        ChecklistItem(
            field="transfer_type",
            data_type="enum",
            required=True,
            description=(
                "How the buyer comes to hold the exposure: shares "
                "transferred directly, an interest in a pooled vehicle, or "
                "a contract for future delivery."
            ),
            allowed_values=[
                "direct_transfer",
                "spv",
                "forward_contract",
                "other",
            ]
        ),
        ChecklistItem(
            field="spv_layers",
            data_type="enum",
            required=True,
            required_if=("transfer_type", "spv"),
            description=(
                "How many pooled vehicles the money passes through before "
                "it reaches the shares. Each layer charges its own fees."
            ),
            allowed_values=[
                "n/a",
                "single_layer",
                "double_layer",
                "unknown",
            ]
        ),
        ChecklistItem(
            field="security_type",
            data_type="enum",
            required=True,
            description=(
                "What the buyer ends up owning: a class of stock, or a "
                "contractual claim on shares."
            ),
            allowed_values=[
                "preferred",
                "common",
                "forward_contract",
                "other",
            ],
        ),
        ChecklistItem(
            field="counterparty",
            data_type="string",
            required=True,
            required_if=("transfer_type", "forward_contract"),
            description=(
                "The named entity on the other side of a forward or "
                "similar contract -- who the buyer is contracting with, "
                "and whose credit the buyer is taking. Not the broker "
                "arranging the deal, and not the company whose shares are "
                "referenced. A statement that the counterparty is subject "
                "to final documentation names nobody, and does not answer "
                "this."
            ),
        ),
        ChecklistItem(
            field="broker_fee",
            data_type="percentage_or_currency",
            required=True,
            description=(
                "What the broker or intermediary charges for arranging "
                "this transaction. Not a fee charged by a vehicle, and "
                "never one of the three numbers in a vehicle's "
                "setup / management / carry fee schedule -- a broker's "
                "fee is stated separately, on any structure."
            ),
        ),
        ChecklistItem(
            field="spv_setup_fee",
            data_type="percentage_or_currency",
            required=True,
            required_if=("transfer_type", "spv"),
            description=(
                "The vehicle's one-off charge for forming and setting up "
                "the SPV, paid once at close -- what brokers call the "
                "one-time fee. Not the broker's commission "
                "for arranging the trade, and not the recurring "
                "management fee the manager charges every year."
            ),
        ),
        ChecklistItem(
            field="spv_management_fee",
            data_type="percentage",
            required=True,
            required_if=("transfer_type", "spv"),
            description=(
                "The recurring fee a vehicle's manager charges for running "
                "it. Not the broker's one-off commission, not the "
                "vehicle's one-off setup charge, and not a share of the "
                "profit."
            ),
        ),
        ChecklistItem(
            field="spv_management_fee_term",
            data_type="date_or_duration",
            # Optional, deliberately. The row exists to hold an answer, not to
            # chase one: `consistency.management_fee_term_unclear` already asks
            # the broker, and making this required would drop every SPV deal's
            # completeness score for a field the client never asked to score.
            required=False,
            description=(
                "How long the management fee is charged for -- \"3 years\", "
                "\"one-time\", \"annual with no stated end\". The period only: "
                "the rate itself belongs in spv_management_fee, and a reply "
                "naming the period does not restate the rate."
            ),
        ),
        ChecklistItem(
            field="carry",
            data_type="percentage_plus_hurdle",
            required=True,
            required_if=("transfer_type", "spv"),
            description=(
                "The manager's share of the profit, taken at exit. Include "
                "any hurdle or preferred return it is charged above."
            ),
        ),
        ChecklistItem(
            field="other_fees",
            data_type="currency",
            # Optional at the client's instruction -- see "Two rows the
            # client made optional" in CLAUDE.md. A residual nobody
            # affirmatively answers is a permanent gap, and stage 4 already
            # treats its silence as undisclosed rather than as zero.
            required=False,
            description=(
                "Any cost to the buyer none of the fee fields above "
                "captures -- legal, administration, wire, escrow or "
                "closing costs -- each one labelled with what the email "
                "calls it. Not the broker's commission, and not the "
                "vehicle's own setup charge, both of which have their own "
                "field."
            ),
        ),
        ChecklistItem(
            field="closing_timeline",
            data_type="date_or_duration",
            required=True,
            description=(
                "How long the transaction takes to complete once terms are "
                "agreed, or the date it completes. On a forward contract "
                "that is when the contract is signed and funded -- the "
                "delivery of the shares is settlement_date, not this. Not "
                "the date the offer expires."
            ),
        ),
        ChecklistItem(
            field="settlement_date",
            data_type="date_or_duration",
            required=True,
            required_if=("transfer_type", "forward_contract"),
            description=(
                "When the referenced shares are actually delivered under a "
                "forward or similar contract, as a date or as a period "
                "after execution. Not the date the contract itself is "
                "signed and funded, which is the closing timeline."
            ),
        ),
        ChecklistItem(
            field="rofr_status",
            data_type="text",
            required=True,
            required_if=("transfer_type", "direct_transfer"),
            description=(
                "Whether the company or its existing holders have a right "
                "of first refusal over this sale, and where that process "
                "stands."
            ),
        ),
        ChecklistItem(
            field="transfer_restrictions",
            data_type="text",
            # Optional at the client's instruction -- see "Two rows the
            # client made optional" in CLAUDE.md. The blocking half of the
            # question is `rofr_status`, which stays required of a direct
            # transfer.
            required=False,
            description=(
                "The stated limits on transferring the shares -- company "
                "or board approval, lockups, share class restrictions, "
                "consent requirements. A statement that terms are still to "
                "be documented is not a restriction; it says the terms are "
                "not yet known."
            ),
        ),
        ChecklistItem(
            field="seller_type",
            data_type="enum",
            required=False,
            description=(
                "Who is selling: a founder, an employee, a fund, or "
                "someone else."
            ),
            allowed_values=[
                "founder",
                "employee",
                "fund",
                "other",
            ],
        ),
        ChecklistItem(
            field="last_round_price_and_date",
            data_type="currency_and_date",
            required=False,
            description=(
                "The price and date of the company's most recent primary "
                "financing. Not this offer's price."
            ),
        ),
        ChecklistItem(
            field="information_rights",
            data_type="text",
            required=False,
            description=(
                "What financial or corporate information the buyer will "
                "receive after closing, and how often."
            ),
        ),
    ]
