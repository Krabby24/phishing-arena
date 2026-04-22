from collections import defaultdict

def compute_leaderboard(tournament_results: dict) -> dict:
    phisher_stats = defaultdict(lambda: {
        "bypass_rates": [],
        "click_probs": [],
        "learning_curves": []
    })
    filter_stats = defaultdict(lambda: {
        "fp_rates": [],
        "detection_rates": []
    })

    for match in tournament_results["matches"]:
        p = match["phisher"]
        f = match["filter"]
        score = match["score"]

        phisher_stats[p]["bypass_rates"].append(score["phisher_bypass_rate"])
        phisher_stats[p]["click_probs"].append(
            score["phisher_avg_click_probability"]
        )
        if score.get("learning_curve"):
            phisher_stats[p]["learning_curves"].append(
                score["learning_curve"]
            )

        phishing_rounds = score["phishing_rounds"]
        bypassed = round(score["phisher_bypass_rate"] * phishing_rounds)
        detected = phishing_rounds - bypassed
        detection_rate = detected / phishing_rounds if phishing_rounds > 0 else 0

        filter_stats[f]["fp_rates"].append(score["filter_false_positive_rate"])
        filter_stats[f]["detection_rates"].append(detection_rate)

    def avg(lst):
        return round(sum(lst) / len(lst), 3) if lst else 0

    phisher_leaderboard = sorted([
        {
            "agent": agent,
            "avg_bypass_rate": avg(stats["bypass_rates"]),
            "avg_click_probability": avg(stats["click_probs"]),
            "learning_trend": _compute_learning_trend(stats["learning_curves"])
        }
        for agent, stats in phisher_stats.items()
    ], key=lambda x: x["avg_bypass_rate"], reverse=True)

    filter_leaderboard = sorted([
        {
            "agent": agent,
            "avg_detection_rate": avg(stats["detection_rates"]),
            "avg_false_positive_rate": avg(stats["fp_rates"])
        }
        for agent, stats in filter_stats.items()
    ], key=lambda x: x["avg_detection_rate"], reverse=True)

    return {
        "phisher_leaderboard": phisher_leaderboard,
        "filter_leaderboard": filter_leaderboard
    }


def _compute_learning_trend(learning_curves: list) -> str:
    """
    Calcola se il bypass rate migliora, peggiora o rimane stabile
    nel corso dei match — indica la capacità adattiva del modello.
    """
    if not learning_curves:
        return "insufficient_data"

    all_first = []
    all_last = []

    for curve in learning_curves:
        if len(curve) >= 2:
            all_first.append(curve[0]["bypass_rate"])
            all_last.append(curve[-1]["bypass_rate"])

    if not all_first or not all_last:
        return "insufficient_data"

    avg_first = sum(all_first) / len(all_first)
    avg_last = sum(all_last) / len(all_last)
    delta = avg_last - avg_first

    if delta > 0.10:
        return f"improving (+{int(delta*100)}%)"
    elif delta < -0.10:
        return f"declining ({int(delta*100)}%)"
    else:
        return f"stable ({'+' if delta >= 0 else ''}{int(delta*100)}%)"


def print_leaderboard(leaderboard: dict):
    print("\n" + "="*50)
    print("PHISHER LEADERBOARD (chi attacca meglio)")
    print("="*50)
    for i, entry in enumerate(leaderboard["phisher_leaderboard"], 1):
        print(f"{i}. {entry['agent']}")
        print(f"   Bypass rate:      {entry['avg_bypass_rate']:.1%}")
        print(f"   Avg click prob:   {entry['avg_click_probability']:.1f}%")
        print(f"   Trend adattivo:   {entry['learning_trend']}")

    print("\n" + "="*50)
    print("FILTER LEADERBOARD (chi difende meglio)")
    print("="*50)
    for i, entry in enumerate(leaderboard["filter_leaderboard"], 1):
        print(f"{i}. {entry['agent']}")
        print(f"   Detection rate:   {entry['avg_detection_rate']:.1%}")
        print(f"   False positive:   {entry['avg_false_positive_rate']:.1%}")