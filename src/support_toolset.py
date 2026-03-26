from typing import Any
from pydantic import BaseModel
import re
import uuid


class PolicySearchRequest(BaseModel):
    """Request model for policy search"""

    query: str


class TicketCreationRequest(BaseModel):
    """Request model for ticket creation"""

    issue_type: str
    user_message: str
    priority: str = "normal"


class EscalationRequest(BaseModel):
    """Request model for escalation"""

    reason: str
    conversation_summary: str


class OrderStatusRequest(BaseModel):
    """Request model for order status"""

    order_id: str


class SupportToolset:
    """Florence Beauty India customer support toolset"""

    def __init__(self):
        # Florence Beauty India knowledge base policies
        self.policies = [
            {
                "title": "Account Access and Password Reset",
                "keywords": [
                    "password",
                    "reset password",
                    "forgot password",
                    "login",
                    "otp",
                    "sign in",
                    "cannot access account",
                    "account locked",
                ],
                "content": (
                    "Customers can reset their password using the Forgot Password option. "
                    "Password reset links or OTPs expire after 10 minutes. "
                    "If the customer reports unrecognized account activity, advise them to reset "
                    "their password immediately and escalate the case for account-security review."
                ),
            },
            {
                "title": "Account Deletion",
                "keywords": [
                    "delete account",
                    "remove account",
                    "close account",
                    "account deletion",
                ],
                "content": (
                    "Account deletion requests may take up to 15 days to complete. "
                    "Active or pending orders must be completed or cancelled before account deletion can be processed."
                ),
            },
            {
                "title": "Shipping and Delivery Policy",
                "keywords": [
                    "shipping",
                    "delivery",
                    "dispatch",
                    "where is my order",
                    "track",
                    "tracking",
                    "order status",
                    "standard shipping",
                    "express shipping",
                    "same day delivery",
                ],
                "content": (
                    "Standard shipping typically takes 4 to 6 business days. "
                    "Express shipping takes 2 to 3 business days. "
                    "Same-day delivery is available only in select metro cities. "
                    "Tracking details are shared after dispatch."
                ),
            },
            {
                "title": "Address Change Policy",
                "keywords": [
                    "change address",
                    "shipping address",
                    "wrong address",
                    "update address",
                    "address correction",
                ],
                "content": (
                    "Shipping address changes are allowed only within 1 hour of placing the order. "
                    "After that window, changes usually cannot be guaranteed."
                ),
            },
            {
                "title": "Return Eligibility Policy",
                "keywords": [
                    "return",
                    "return policy",
                    "refund",
                    "money back",
                    "eligible return",
                    "can i return",
                ],
                "content": (
                    "Eligible products can be returned within 7 days of delivery. "
                    "Returned items must generally be unused, unopened, and in original sealed packaging. "
                    "Opened or used makeup and skincare products are generally non-returnable for hygiene reasons."
                ),
            },
            {
                "title": "Refund Processing Policy",
                "keywords": [
                    "refund status",
                    "refund time",
                    "when will i get refund",
                    "refund processed",
                    "refund pending",
                ],
                "content": (
                    "Approved refunds are typically processed within 3 to 5 business days. "
                    "After processing, banks or payment providers may take an additional 5 to 7 business days "
                    "to reflect the amount."
                ),
            },
            {
                "title": "Exchange Policy",
                "keywords": [
                    "exchange",
                    "replace with another shade",
                    "swap product",
                    "exchange item",
                ],
                "content": (
                    "Florence Beauty India does not offer direct exchanges. "
                    "Customers must return an eligible product for a refund and place a new order separately."
                ),
            },
            {
                "title": "Shade Mismatch Policy",
                "keywords": [
                    "wrong shade",
                    "shade mismatch",
                    "shade return",
                    "foundation shade",
                    "concealer shade",
                    "lipstick shade",
                ],
                "content": (
                    "Shade mismatch returns are generally only accepted if the product is unopened and unused. "
                    "For shade guidance, collect the customer's skin tone category, undertone, and current shade "
                    "in another brand if available."
                ),
            },
            {
                "title": "Damaged, Leaked, Defective, or Wrong Item Policy",
                "keywords": [
                    "damaged",
                    "broken",
                    "defective",
                    "faulty",
                    "leaked",
                    "wrong item",
                    "received wrong product",
                    "replacement",
                    "missing item",
                ],
                "content": (
                    "If a customer receives a damaged, leaked, defective, or wrong item, "
                    "request photos of the product, outer packaging, shipping label, and invoice if available. "
                    "Create a support ticket for review. In cases where policy requires it, ask for an unboxing video."
                ),
            },
            {
                "title": "Billing and Payment Policy",
                "keywords": [
                    "billing",
                    "payment",
                    "charged",
                    "invoice",
                    "card",
                    "upi",
                    "double charge",
                    "duplicate charge",
                    "charged twice",
                    "payment failed",
                ],
                "content": (
                    "Customers should provide the order ID, payment method, and charge details for billing issues. "
                    "Duplicate posted charges must be escalated to Tier 2 immediately. "
                    "Payment disputes that cannot be resolved in chat should be ticketed for manual review."
                ),
            },
            {
                "title": "Allergic Reaction and Product Safety Policy",
                "keywords": [
                    "allergy",
                    "allergic reaction",
                    "irritation",
                    "rash",
                    "burning",
                    "swelling",
                    "skin reaction",
                    "reaction",
                    "ingredient safety",
                ],
                "content": (
                    "If a customer reports irritation or an allergic reaction, advise them to stop using the product immediately. "
                    "If applicable, they should wash the product off and consult a dermatologist or medical professional "
                    "if symptoms continue or worsen. Severe symptoms such as swelling, burning, bleeding, or medical emergency "
                    "must be escalated immediately."
                ),
            },
            {
                "title": "Human Escalation Policy",
                "keywords": [
                    "human",
                    "agent",
                    "manager",
                    "specialist",
                    "escalate",
                    "complaint",
                    "unresolved",
                ],
                "content": (
                    "Cases should be escalated to a human specialist when they are high-risk, unresolved, security-related, "
                    "legally sensitive, medically sensitive, or when the customer explicitly asks for a human agent or manager."
                ),
            },
            {
                "title": "Security and Fraud Policy",
                "keywords": [
                    "fraud",
                    "fraudulent charge",
                    "unauthorized access",
                    "hacked account",
                    "security issue",
                    "unknown login",
                ],
                "content": (
                    "If a customer reports unauthorized account access or fraudulent charges, "
                    "advise immediate password reset where relevant, create a support ticket, "
                    "and escalate the case to a human specialist."
                ),
            },
        ]

        # Demo order database
        self.orders = {
            "ORD123": {
                "status": "shipped",
                "eta": "2 business days",
                "tracking_note": "Package is in transit at the regional hub.",
            },
            "ORD456": {
                "status": "processing",
                "eta": "Dispatch expected within 24 hours",
                "tracking_note": "Order is being packed.",
            },
            "ORD789": {
                "status": "delivered",
                "eta": "Delivered",
                "tracking_note": "Delivered to customer address.",
            },
        }

        self.ticket_counter = 1000

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.strip().lower())

    def _tokenize(self, text: str) -> set[str]:
        cleaned = re.sub(r"[^a-z0-9\s]", " ", self._normalize(text))
        return {token for token in cleaned.split() if token}

    def _score_policy(self, query: str, policy: dict[str, Any]) -> int:
        query_norm = self._normalize(query)
        query_tokens = self._tokenize(query)

        score = 0

        if self._normalize(policy["title"]) in query_norm:
            score += 8

        for keyword in policy["keywords"]:
            keyword_norm = self._normalize(keyword)
            if keyword_norm in query_norm:
                score += 5
            else:
                keyword_tokens = self._tokenize(keyword_norm)
                score += len(query_tokens.intersection(keyword_tokens))

        content_tokens = self._tokenize(policy["content"])
        score += len(query_tokens.intersection(content_tokens))

        return score

    def _detect_priority(self, text: str) -> str:
        query = self._normalize(text)

        urgent_terms = [
            "severe allergic reaction",
            "swelling",
            "burning",
            "bleeding",
            "medical emergency",
            "fraudulent charge",
            "unauthorized access",
            "lawyer",
            "legal action",
            "consumer court",
            "regulatory complaint",
            "manager",
            "human agent",
        ]
        high_terms = [
            "damaged",
            "defective",
            "wrong item",
            "charged twice",
            "duplicate charge",
            "allergic reaction",
            "irritation",
            "rash",
            "security issue",
        ]

        if any(term in query for term in urgent_terms):
            return "high"

        if any(term in query for term in high_terms):
            return "high"

        return "normal"

    def search_policy(self, query: str) -> str:
        """Search the Florence Beauty India knowledge base for the most relevant policy"""
        try:
            if not query.strip():
                return "Error: Empty query provided"

            scored = []
            for policy in self.policies:
                score = self._score_policy(query, policy)
                scored.append((score, policy))

            scored.sort(key=lambda x: x[0], reverse=True)
            best_score, best_policy = scored[0]

            if best_score <= 0:
                return (
                    "No exact policy match found. Available Florence Beauty India topics include "
                    "account access, shipping, address changes, returns, refunds, exchanges, "
                    "shade mismatch, damaged or wrong items, billing, product reactions, security, and escalation."
                )

            return (
                f"Policy found: {best_policy['title']}\n"
                f"Details: {best_policy['content']}"
            )

        except Exception as e:
            return f"Failed to search policy: {str(e)}"

    def create_ticket(
        self, issue_type: str, user_message: str, priority: str = "normal"
    ) -> str:
        """Create a support ticket for unresolved Florence Beauty India cases"""
        try:
            if not issue_type.strip():
                return "Error: issue_type is required"

            if not user_message.strip():
                return "Error: user_message is required"

            self.ticket_counter += 1
            ticket_id = f"FBI-TICKET-{self.ticket_counter}"

            priority = priority.strip().lower()
            if priority not in {"low", "normal", "high"}:
                priority = self._detect_priority(f"{issue_type} {user_message}")

            return (
                f"Support ticket created successfully.\n"
                f"Ticket ID: {ticket_id}\n"
                f"Issue Type: {issue_type}\n"
                f"Priority: {priority}\n"
                f"Customer Message: {user_message}\n"
                f"Next Step: A Florence Beauty support specialist will review this case."
            )

        except Exception as e:
            return f"Failed to create ticket: {str(e)}"

    def escalate_to_human(self, reason: str, conversation_summary: str) -> str:
        """Escalate a case to a Florence Beauty India human support specialist"""
        try:
            if not reason.strip():
                return "Error: reason is required"

            if not conversation_summary.strip():
                return "Error: conversation_summary is required"

            escalation_id = f"FBI-ESC-{uuid.uuid4().hex[:8].upper()}"
            priority = self._detect_priority(f"{reason} {conversation_summary}")

            return (
                f"Escalation successful.\n"
                f"Escalation ID: {escalation_id}\n"
                f"Priority: {priority}\n"
                f"Reason: {reason}\n"
                f"Summary Sent to Human Agent: {conversation_summary}\n"
                f"Status: Waiting for human support follow-up."
            )

        except Exception as e:
            return f"Failed to escalate case: {str(e)}"

    def get_order_status(self, order_id: str) -> str:
        """Check demo order status"""
        try:
            order_id = order_id.strip().upper()

            if not order_id:
                return "Error: order_id is required"

            order = self.orders.get(order_id)
            if not order:
                return (
                    f"No order found for ID {order_id}. "
                    "Ask the customer to confirm the order ID. "
                    "If needed, create a support ticket for manual order investigation."
                )

            return (
                f"Order ID: {order_id}\n"
                f"Status: {order['status']}\n"
                f"ETA: {order['eta']}\n"
                f"Tracking Note: {order['tracking_note']}"
            )

        except Exception as e:
            return f"Failed to fetch order status: {str(e)}"

    def get_tools(self) -> dict[str, Any]:
        """Return dictionary of available tools for OpenAI function calling"""
        return {
            "search_policy": self,
            "create_ticket": self,
            "escalate_to_human": self,
            "get_order_status": self,
        }