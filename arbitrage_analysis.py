"""
Financial Arbitrage Analysis (Argentina)

Pulls live USD exchange rates from DolarAPI, simulates buying USD at the
official rate and selling them through alternative routes (Blue, MEP, Crypto,
Card), and saves the results to a CSV file used by the Tableau dashboard.

Note: the "Card" rate is the price paid for card purchases abroad (official
rate plus taxes). It is not a rate at which USD can be sold, so that route is
kept for reference only.
"""

import csv
import os
from datetime import datetime

import requests

BASE_URL = "https://dolarapi.com/v1/dolares"
COMMISSION = 0.01                      # 1% commission on the final amount
DEFAULT_CAPITAL = 1_000_000            # starting capital in ARS
CSV_FILE = "resultados_arbitraje.csv"  # same name the Tableau workbook reads

CSV_HEADERS = [
    "Date & Time",
    "Performance Type",
    "Route",
    "Buy Price",
    "Sell Price",
    "Difference",
    "Difference (%)",
    "Result",
    "Return (%)",
    "Initial Capital",
    "Net Gain",
    "Final Capital",
]

# Each route: (display name, DolarAPI endpoint for the destination rate)
DESTINATIONS = [
    ("Official to Blue", "blue"),
    ("Official to Mep", "bolsa"),
    ("Official to Crypto", "cripto"),
    ("Official to Card", "tarjeta"),
]


def fetch_rate(name):
    """Return the quote for one dollar type from DolarAPI."""
    response = requests.get(f"{BASE_URL}/{name}", timeout=10)
    response.raise_for_status()
    return response.json()


def calculate_arbitrage(buy_price, sell_price, amount, commission=COMMISSION):
    """Net result in ARS of buying USD at buy_price and selling at sell_price."""
    dollars = amount / buy_price
    pesos = dollars * sell_price
    commission_cost = pesos * commission
    return pesos - commission_cost - amount


def build_routes():
    """Fetch all rates and build the list of routes to analyze."""
    official = fetch_rate("oficial")
    print("Last update (official):", official["fechaActualizacion"])

    buy_price = official["venta"]  # we buy USD at the official selling rate
    routes = []
    for route_name, endpoint in DESTINATIONS:
        quote = fetch_rate(endpoint)
        print(f"Last update ({endpoint}):", quote["fechaActualizacion"])
        routes.append(
            {
                "name": route_name,
                "buy_price": buy_price,
                "sell_price": quote["compra"],  # we sell USD at their buying rate
            }
        )
    return routes


def analyze_route(route, capital):
    """Compute all the metrics for one route."""
    difference = route["sell_price"] - route["buy_price"]
    difference_pct = difference / route["buy_price"] * 100
    result = calculate_arbitrage(route["buy_price"], route["sell_price"], capital)
    return {
        "difference": round(difference, 2),
        "difference_pct": round(difference_pct, 2),
        "result": round(result, 2),
        "return_pct": round(result / capital * 100, 2),
        "final_capital": round(capital + result, 2),
        "performance": "Profitable" if result > 0 else "Not Profitable",
    }


def ask_capital():
    """Ask the user for a starting capital (Enter = default)."""
    raw = input(f"Initial capital in ARS (Enter for {DEFAULT_CAPITAL:,}): ").strip()
    if not raw:
        return float(DEFAULT_CAPITAL)
    try:
        value = float(raw)
    except ValueError:
        print("Invalid number, using the default capital.")
        return float(DEFAULT_CAPITAL)
    return value if value > 0 else float(DEFAULT_CAPITAL)


# Routes shown for reference only: they are not real selling rates, so they
# are excluded from the "best route" summary.
REFERENCE_ONLY = {"Official to Card"}


def print_report(routes, capital):
    """Print the analysis of every route plus a summary."""
    print("\n----- ROUTE ANALYSIS -----")
    profitable = []
    for route in routes:
        metrics = analyze_route(route, capital)
        print(route["name"])
        print("  Buy price:", route["buy_price"])
        print("  Sell price:", route["sell_price"])
        print("  Difference:", metrics["difference"])
        print("  Difference (%):", metrics["difference_pct"], "%")
        print("  Result:", metrics["result"])
        print("  Return:", metrics["return_pct"], "%")
        print("  ->", metrics["performance"])
        if route["name"] in REFERENCE_ONLY:
            print("  (reference only: not a real selling rate, excluded from summary)")
            continue
        if metrics["result"] > 0:
            profitable.append((route["name"], metrics))

    print("\n----- SUMMARY -----")
    print("Routes analyzed:", len(routes))
    print("Profitable routes:", len(profitable))
    if profitable:
        best_name, best = max(profitable, key=lambda item: item[1]["result"])
        print("Best route:", best_name)
        print("Net gain:", best["result"])
        print("Return:", best["return_pct"], "%")
        print("Final capital:", best["final_capital"])
    else:
        print("No profitable routes.")


def save_results(routes, capital):
    """Append one row per route to the CSV file."""
    file_exists = os.path.exists(CSV_FILE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(CSV_HEADERS)
        for route in routes:
            m = analyze_route(route, capital)
            writer.writerow(
                [
                    timestamp,
                    m["performance"],
                    route["name"],
                    route["buy_price"],
                    route["sell_price"],
                    m["difference"],
                    m["difference_pct"],
                    m["result"],
                    m["return_pct"],
                    capital,
                    m["result"],
                    m["final_capital"],
                ]
            )
    print(f"\nResults saved to {CSV_FILE}")


def main():
    try:
        routes = build_routes()
    except requests.RequestException as error:
        print("Could not fetch exchange rates:", error)
        return

    capital = ask_capital()
    print_report(routes, capital)
    save_results(routes, capital)


if __name__ == "__main__":
    main()
