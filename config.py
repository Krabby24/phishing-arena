from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------------------------------------------
# MODALITA'
# "dev"  = solo Gemini (3 istanze), zero costi API
# "prod" = tutti e 4 gli agenti, torneo completo
# ---------------------------------------------------------------------------
MODE = "prod"

# ---------------------------------------------------------------------------
# PARAMETRI TORNEO
# ---------------------------------------------------------------------------
TOURNAMENT = {
    "rounds_per_match": 20,
    "phishing_ratio": 0.40,
    "matches_per_pair": 2,
}

# ---------------------------------------------------------------------------
# PREZZI REALI PER STIMA COSTI ($ per milione di token)
# Verificati ad aprile 2026
# ---------------------------------------------------------------------------
PRICING = {
    "claude": {
        "model": "claude-sonnet-4-6",
        "input_per_1m": 3.00,
        "output_per_1m": 15.00,
    },
    "openai": {
        "model": "gpt-5.4-mini",
        "input_per_1m": 0.75,
        "output_per_1m": 4.50,
    },
    "deepseek": {
        "model": "deepseek-chat",
        "input_per_1m": 0.27,
        "output_per_1m": 1.10,
    },
    "grok": {
        "model": "grok-4-fast-non-reasoning",
        "input_per_1m": 0.20,
        "output_per_1m": 0.50,
    },
}

# ---------------------------------------------------------------------------
# LINEUP AGENTI
# ---------------------------------------------------------------------------
def get_agents():
    from agents.gemini_agent import GeminiAgent

    dev_agents = [
        GeminiAgent(model="gemini-2.5-flash", instance_id=1),
        GeminiAgent(model="gemini-2.5-flash", instance_id=2),
        GeminiAgent(model="gemini-2.5-flash", instance_id=3),
    ]

    if MODE == "prod":
        from agents.claude_agent import ClaudeAgent
        from agents.openai_agent import OpenAIAgent
        from agents.deepseek_agent import DeepSeekAgent
        from agents.grok_agent import GrokAgent

        prod_agents = [
            ClaudeAgent(model="claude-sonnet-4-6"),
            OpenAIAgent(model="gpt-5.4-mini"),
            DeepSeekAgent(model="deepseek-chat"),
            GrokAgent(model="grok-4-fast-non-reasoning"),
        ]
        return prod_agents

    return dev_agents