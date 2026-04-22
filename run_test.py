import threading
import time
import pyautogui
import os
import sys
from pathlib import Path

pyautogui.FAILSAFE = False

def keep_awake():
    while True:
        pyautogui.move(1, 1)
        pyautogui.move(-1, -1)
        time.sleep(60)

awake_thread = threading.Thread(target=keep_awake, daemon=True)
awake_thread.start()

from config import get_agents, TOURNAMENT
from arena.orchestrator import run_tournament
from analysis.metrics import compute_leaderboard, print_leaderboard


def delete_old_checkpoint():
    """
    Elimina esplicitamente il checkpoint del run precedente.
    Da chiamare SOLO prima di un rerun definitivo da zero.
    """
    checkpoint_path = Path("data/checkpoints/tournament_checkpoint.json")
    if checkpoint_path.exists():
        print("\n[!] Trovato checkpoint esistente dal run precedente.")
        print(f"    Path: {checkpoint_path}")
        confirm = input("    Vuoi eliminarlo e ripartire da zero? [s/N] ").strip().lower()
        if confirm == "s":
            checkpoint_path.unlink()
            print("    [OK] Checkpoint eliminato. Il torneo partirà da zero.\n")
        else:
            print("    [OK] Checkpoint mantenuto. Il torneo riprenderà dal punto di interruzione.\n")
    else:
        print("\n[OK] Nessun checkpoint trovato — torneo fresco.\n")


def run_pre_tournament():
    print("\n" + "#"*60)
    print("TORNEO FINALE — tutti gli agenti, parametri produzione")
    print("#"*60)

    # Gestione checkpoint: chiede conferma prima di procedere
    delete_old_checkpoint()

    all_agents = get_agents()

    if len(all_agents) < 3:
        print("ERRORE: servono almeno 3 agenti. Controlla config.py")
        sys.exit(1)

    print(f"Agenti nel torneo: {[a.name for a in all_agents]}")
    print(f"Round per match:   {TOURNAMENT['rounds_per_match']}")
    print(f"Phishing ratio:    {TOURNAMENT['phishing_ratio']}")
    print(f"Ripetizioni:       {TOURNAMENT['matches_per_pair']}")

    # Calcolo match totali
    from itertools import permutations
    combos = list(permutations(all_agents, 3))
    total = len(combos) * TOURNAMENT["matches_per_pair"]
    print(f"Match totali:      {total}")
    print()

    results = run_tournament(
        agents=all_agents,
        rounds_per_match=TOURNAMENT["rounds_per_match"],
        phishing_ratio=TOURNAMENT["phishing_ratio"],
        repetitions=TOURNAMENT["matches_per_pair"]
    )

    leaderboard = compute_leaderboard(results)
    print_leaderboard(leaderboard)

    print("\n" + "="*60)
    print("File completo salvato in data/results/")
    print("="*60)


if __name__ == "__main__":
    run_pre_tournament()