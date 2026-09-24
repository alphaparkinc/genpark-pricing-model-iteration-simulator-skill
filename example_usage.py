import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import PricingModelIterationSimulatorClient

def main():
    client = PricingModelIterationSimulatorClient()
    res = client.simulate_pricing_iteration()
    print("=== Pricing Model Iteration Simulator Output ===")
    print(f"Cohort: {res['customer_cohort']} | Active Users: {res['active_users']:,}")
    print(f"Total API Calls: {res['total_api_calls_this_month']:,}")
    print(f"\nModel Revenue Comparison:")
    for model, rev in res["model_revenues"].items():
        flag = " ← RECOMMENDED" if model.replace("_usd", "") == res["recommended_model"].replace("_", "_") else ""
        print(f"  {model:25s}: ${rev:>12,.2f}{flag}")
    print(f"\nRecommended: {res['recommended_model'].upper()} (${res['recommended_model_revenue_usd']:,.2f})")
    print(f"Revenue Uplift vs Seat: {res['revenue_uplift_vs_seat_pct']}%")
    print(f"Usage Elasticity at 3.5x Volume: {res['usage_elasticity_uplift_at_3_5x_volume_pct']}")
    print(f"Iteration Confidence: {res['iteration_confidence_score']}")
    print(f"Verdict: {res['verdict']}")

if __name__ == "__main__":
    main()
