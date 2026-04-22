import json
import os
import random
from pathlib import Path

# ---------------------------------------------------------------------------
# ARCHETIPI TARGET
# ---------------------------------------------------------------------------

TARGET_ARCHETIPI = [
    {
        "ruolo": "CFO",
        "settore": "manifatturiero",
        "familiarita_cyber": "bassa",
        "dataset_file": "cfo_manifatturiero.json"
    },
    {
        "ruolo": "HR Manager",
        "settore": "tech",
        "familiarita_cyber": "media",
        "dataset_file": "hr_manager_tech.json"
    },
    {
        "ruolo": "IT Manager",
        "settore": "logistica",
        "familiarita_cyber": "alta",
        "dataset_file": "it_manager_logistica.json"
    },
    {
        "ruolo": "Responsabile Acquisti",
        "settore": "retail",
        "familiarita_cyber": "bassa",
        "dataset_file": "responsabile_acquisti_retail.json"
    },
    {
        "ruolo": "CEO",
        "settore": "PMI generica",
        "familiarita_cyber": "bassa",
        "dataset_file": "ceo_pmi.json"
    },
    {
        "ruolo": "Avvocato",
        "settore": "studio legale",
        "familiarita_cyber": "media",
        "dataset_file": "avvocato_studio_legale.json"
    },
    {
        "ruolo": "Commerciale",
        "settore": "assicurazioni",
        "familiarita_cyber": "bassa",
        "dataset_file": "commerciale_assicurazioni.json"
    },
    {
        "ruolo": "Contabile",
        "settore": "studio commercialista",
        "familiarita_cyber": "bassa",
        "dataset_file": "contabile_commercialista.json"
    },
    {
        "ruolo": "Direttore Marketing",
        "settore": "e-commerce",
        "familiarita_cyber": "media",
        "dataset_file": "direttore_marketing_ecommerce.json"
    },
    {
        "ruolo": "Office Manager",
        "settore": "consulenza",
        "familiarita_cyber": "bassa",
        "dataset_file": "office_manager_consulenza.json"
    },
    {
        "ruolo": "Responsabile IT",
        "settore": "bancario",
        "familiarita_cyber": "alta",
        "dataset_file": "responsabile_it_bancario.json"
    },
    {
        "ruolo": "Titolare",
        "settore": "ristorante/hospitality",
        "familiarita_cyber": "molto bassa",
        "dataset_file": "titolare_hospitality.json"
    },
]

# ---------------------------------------------------------------------------
# PROMPT GENERAZIONE PROFILO TARGET
# ---------------------------------------------------------------------------

TARGET_PROFILE_GENERATION_PROMPT = """Sei un generatore di profili realistici per security awareness training.

Genera un profilo dettagliato e realistico per un professionista con queste caratteristiche:
- Ruolo: {ruolo}
- Settore: {settore}
- Familiarità con la cybersecurity: {familiarita_cyber}

Il profilo deve essere restituito SOLO come oggetto JSON valido con questa struttura:
{{
  "nome": "Nome Cognome realistico italiano",
  "eta": numero intero,
  "azienda": "Nome azienda italiana plausibile per il settore",
  "ruolo": "Titolo professionale specifico",
  "settore": "Settore di appartenenza",
  "profilo_psicologico": "Descrizione carattere, abitudini decisionali, punti di forza e debolezza",
  "stato_attuale": "Situazione lavorativa attuale con pressioni, progetti in corso, scadenze",
  "familiarita_cyber": "Descrizione dettagliata del livello di consapevolezza cyber",
  "dettagli_extra": "Abitudini digitali, dispositivi usati, comportamenti rilevanti per la sicurezza"
}}

Restituisci SOLO il JSON, senza testo aggiuntivo."""


# ---------------------------------------------------------------------------
# CARICAMENTO DATASET LEGIT STRATIFICATO
# ---------------------------------------------------------------------------

LEGIT_EMAILS_DIR = Path("data/legit_emails")


def load_legit_emails_for_archetipo(archetipo: dict) -> list:
    """
    Carica le email legittime dal pool specifico per l'archetipo corrente.
    Fallback su email sintetiche generiche se il file non esiste.
    """
    dataset_file = archetipo.get("dataset_file", "")
    filepath = LEGIT_EMAILS_DIR / dataset_file

    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                emails = json.load(f)
            # Normalizza il formato per compatibilità con EmailStream
            normalized = []
            for e in emails:
                normalized.append({
                    "mittente": e.get("mittente", ""),
                    "oggetto": e.get("oggetto", ""),
                    "corpo": e.get("corpo", ""),
                    "link": e.get("link"),
                    "label": "LEGIT"
                })
            print(f"  [EmailStream] Caricate {len(normalized)} email legit "
                  f"per archetipo: {archetipo['ruolo']} / {archetipo['settore']}")
            return normalized
        except Exception as ex:
            print(f"  [EmailStream] Errore caricamento {filepath}: {ex}")

    # Fallback sintetico
    print(f"  [EmailStream] File {dataset_file} non trovato — uso fallback sintetiche.")
    return _get_synthetic_fallback(archetipo)


def _get_synthetic_fallback(archetipo: dict) -> list:
    """Email sintetiche generiche come fallback di emergenza."""
    return [
        {
            "mittente": "it-support@azienda.it",
            "oggetto": "Manutenzione programmata server — domenica ore 02:00",
            "corpo": "Buongiorno,\n\ncomunichiamo che domenica notte dalle 02:00 alle 05:00 "
                     "sarà effettuata manutenzione programmata sui server aziendali. "
                     "I servizi potrebbero non essere disponibili in quella fascia oraria.\n\nIT Department",
            "link": None,
            "label": "LEGIT"
        },
        {
            "mittente": "hr@azienda.it",
            "oggetto": "Reminder: compilazione foglio presenze entro venerdì",
            "corpo": "Gentile collega,\n\nti ricordiamo che il foglio presenze del mese corrente "
                     "va compilato entro venerdì 5. Puoi accedere al portale HR come di consueto.\n\nGrazie,\nUfficio HR",
            "link": None,
            "label": "LEGIT"
        },
        {
            "mittente": "admin@gestionale-aziendale.it",
            "oggetto": "Aggiornamento password — scadenza 30 giorni",
            "corpo": "La tua password aziendale scadrà tra 30 giorni. "
                     "Aggiornala accedendo al pannello di gestione account con le tue credenziali abituali.",
            "link": "https://gestionale-aziendale.it/account",
            "label": "LEGIT"
        },
        {
            "mittente": "payroll@azienda.it",
            "oggetto": "Cedolino disponibile",
            "corpo": "Gentile dipendente,\n\nil cedolino del mese è disponibile "
                     "sul portale HR nella sezione Documenti Personali.\n\nUfficio Paghe",
            "link": None,
            "label": "LEGIT"
        },
        {
            "mittente": "calendario@google.com",
            "oggetto": "Promemoria: Riunione team — domani ore 10:00",
            "corpo": "Questo è un promemoria automatico per la riunione programmata "
                     "per domani alle 10:00.\n\nPartecipanti: 6\nDurata: 1 ora",
            "link": "https://meet.google.com/xyz-abc-123",
            "label": "LEGIT"
        },
        {
            "mittente": "noreply@docusign.com",
            "oggetto": "Documento in attesa della tua firma",
            "corpo": "Un documento richiede la tua firma. "
                     "Accedi a DocuSign per visualizzarlo e firmarlo. "
                     "Il documento scadrà tra 5 giorni.",
            "link": "https://www.docusign.com/documents",
            "label": "LEGIT"
        },
        {
            "mittente": "noreply@fatturazione.it",
            "oggetto": "Fattura disponibile",
            "corpo": "La fattura del mese è disponibile sul portale fornitori.",
            "link": None,
            "label": "LEGIT"
        },
        {
            "mittente": "booking@hotel.it",
            "oggetto": "Conferma prenotazione",
            "corpo": "La sua prenotazione è confermata. Check-in dalle 14:00.",
            "link": None,
            "label": "LEGIT"
        },
        {
            "mittente": "newsletter@settore.it",
            "oggetto": "Aggiornamenti del settore",
            "corpo": "Buongiorno, in questa edizione trovi i principali aggiornamenti "
                     "normativi e di settore del mese.",
            "link": None,
            "label": "LEGIT"
        },
        {
            "mittente": "comunicazioni@inps.it",
            "oggetto": "Comunicazione INPS",
            "corpo": "È disponibile una nuova comunicazione sul portale INPS.",
            "link": "https://www.inps.it/",
            "label": "LEGIT"
        },
    ]


# ---------------------------------------------------------------------------
# MAZZO ARCHETIPI
# ---------------------------------------------------------------------------

class ArchetipoMazzo:
    """
    Sistema a mazzo di carte per gli archetipi.
    Garantisce copertura completa prima di ripetere.
    """

    def __init__(self):
        self._mazzo = []
        self._shuffle()

    def _shuffle(self):
        self._mazzo = TARGET_ARCHETIPI.copy()
        random.shuffle(self._mazzo)

    def draw(self) -> dict:
        if not self._mazzo:
            self._shuffle()
        return self._mazzo.pop()


# ---------------------------------------------------------------------------
# EMAIL STREAM STRATIFICATO
# ---------------------------------------------------------------------------

class EmailStream:
    """
    Stream misto di email legittime (stratificate per archetipo) e phishing.
    Le email legit vengono pescate dal pool specifico dell'archetipo corrente.
    """

    def __init__(self, phishing_ratio: float = 0.20):
        self.phishing_ratio = phishing_ratio
        self._archetipo_mazzo = ArchetipoMazzo()
        self._current_archetipo = None
        self._legit_pool = []
        self._legit_used = []
        self._phishing_queue = []
        self._stream_queue = []
        self._stats = {"total": 0, "phishing": 0, "legit": 0}

    def get_next_archetipo(self) -> dict:
        """Pesca il prossimo archetipo e carica il pool legit corrispondente."""
        self._current_archetipo = self._archetipo_mazzo.draw()
        self._load_legit_pool(self._current_archetipo)
        return self._current_archetipo

    def _load_legit_pool(self, archetipo: dict):
        """Carica e mescola il pool legit per l'archetipo corrente."""
        emails = load_legit_emails_for_archetipo(archetipo)
        self._legit_pool = emails.copy()
        self._legit_used = []
        random.shuffle(self._legit_pool)

    def _get_next_legit(self) -> dict:
        """
        Pesca la prossima email legit dal pool dell'archetipo corrente.
        Se il pool è esaurito, rimescola usando anche quelle già usate.
        """
        if not self._legit_pool:
            # Pool esaurito — rimescola tutto
            self._legit_pool = self._legit_used.copy()
            self._legit_used = []
            random.shuffle(self._legit_pool)

        email = self._legit_pool.pop()
        self._legit_used.append(email)
        return email

    def add_phishing_email(self, email: dict):
        """Aggiunge l'email phishing generata dal Phisher alla coda."""
        email["label"] = "PHISHING"
        self._phishing_queue.append(email)

    def get_next_email(self) -> dict:
        """
        Restituisce la prossima email dallo stream misto.
        Con probabilità phishing_ratio restituisce una email phishing,
        altrimenti una email legit coerente con l'archetipo corrente.
        """
        # Se c'è una email phishing in coda e il dado dice phishing
        if self._phishing_queue and random.random() < self.phishing_ratio:
            email = self._phishing_queue.pop(0)
            self._stats["total"] += 1
            self._stats["phishing"] += 1
            return email

        # Altrimenti email legit stratificata per archetipo
        email = self._get_next_legit()
        self._stats["total"] += 1
        self._stats["legit"] += 1
        return email

    def get_stats(self) -> dict:
        actual_ratio = (
            self._stats["phishing"] / self._stats["total"]
            if self._stats["total"] > 0 else 0
        )
        return {
            "total": self._stats["total"],
            "phishing": self._stats["phishing"],
            "legit": self._stats["legit"],
            "actual_ratio": round(actual_ratio, 3)
        }