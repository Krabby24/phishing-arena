import time
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Classe base per tutti gli agenti LLM.
    Implementa exponential backoff per gestire errori temporanei delle API.
    """

    def __init__(self, name: str):
        self.name = name

    def generate(self, system_prompt: str, user_message: str) -> str:
        """
        Genera una risposta con exponential backoff.
        5 tentativi con delay crescente: 2, 5, 15, 30, 60 secondi.
        Non crasha mai il torneo — se tutti i tentativi falliscono
        restituisce una stringa JSON con dettaglio errore per il logging.
        """
        delays = [2, 5, 15, 30, 60]
        last_error = None
        last_error_type = None

        # Rate limiter: 1 secondo tra ogni chiamata API
        time.sleep(1)

        for attempt, delay in enumerate(delays, 1):
            try:
                response = self._generate(system_prompt, user_message)
                if response and response.strip():
                    return response
                print(f"  [{self.name}] Tentativo {attempt}: risposta vuota, riprovo...")
                last_error = "empty_response"
                last_error_type = "empty_response"
            except Exception as e:
                last_error = str(e)
                last_error_type = type(e).__name__
                print(f"  [{self.name}] Errore tentativo {attempt}/{len(delays)}: "
                      f"{last_error_type}: {last_error[:200]}")

            if attempt < len(delays):
                print(f"  [{self.name}] Attendo {delay}s...")
                time.sleep(delay)

        # Tutti i tentativi falliti — restituisce errore dettagliato loggabile
        import json
        print(f"  [{self.name}] Tutti i tentativi falliti. Marcato come errore.")
        return json.dumps({
            "error": "all_retries_failed",
            "error_type": last_error_type,
            "error_detail": str(last_error)[:500] if last_error else "unknown",
            "agent": self.name,
            "raw": ""
        }, ensure_ascii=False)

    @abstractmethod
    def _generate(self, system_prompt: str, user_message: str) -> str:
        """Implementazione specifica per ogni provider LLM."""
        pass