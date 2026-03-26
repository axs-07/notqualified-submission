import logging
import os

import uvicorn
from dotenv import load_dotenv
from starlette.applications import Starlette

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from .openai_agent import create_agent
from .openai_agent_executor import OpenAIAgentExecutor

load_dotenv()
logging.basicConfig()


def main(host: str = "0.0.0.0", port: int = 5000):
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("OPENAI_MODEL", "openrouter/auto")

    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set")

    skill = AgentSkill(
        id="florence_beauty_customer_support",
        name="Florence Beauty Customer Support",
        description=(
            "Handles Florence Beauty India customer queries including account help, "
            "shipping, delivery, returns, refunds, payments, product guidance, "
            "shade matching, damaged or wrong items, and escalation to a human agent."
        ),
        tags=[
            "florence-beauty",
            "customer-support",
            "beauty",
            "makeup",
            "skincare",
            "shipping",
            "delivery",
            "refunds",
            "returns",
            "billing",
            "shade-matching",
            "product-guidance",
            "escalation",
        ],
        examples=[
            "How do I reset my Florence Beauty password?",
            "Where is my order ORD123?",
            "My package says delivered but I did not receive it.",
            "I received the wrong shade. Can I return it?",
            "I was charged twice for my order.",
            "A product caused irritation on my skin.",
            "Connect me to a human agent.",
        ],
    )

    agent_card = AgentCard(
        name="Florence Beauty India Support Agent",
        description=(
            "AI customer support agent for Florence Beauty India. "
            "Answers policy and support questions using the Florence Beauty "
            "customer support knowledge base and supports escalation workflows."
        ),
        url=f"http://{host}:{port}/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    agent_data = create_agent()

    agent_executor = OpenAIAgentExecutor(
        card=agent_card,
        tools=agent_data["tools"],
        api_key=api_key,
        system_prompt=agent_data["system_prompt"],
        base_url=base_url,
        model=model,
    )

    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=InMemoryTaskStore(),
    )

    a2a_app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    app = Starlette(routes=a2a_app.routes())
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
