import json
from typing import Dict, Any, List, Optional

class PricingModelIterationSimulatorClient:
    """
    Production-grade pricing model iteration and revenue impact simulator.
    Inspired by Metronome (metronome.com) — enabling companies to launch products faster
    and iterate pricing models confidently without engineering rework.
    Simulates seat-based, usage-based, and hybrid pricing strategies side-by-side.
    """
    def __init__(self):
        pass

    def simulate_pricing_iteration(
        self,
        customer_cohort: str = "enterprise_ai_companies",
        monthly_active_users: int = 420,
        avg_api_calls_per_user: int = 18500,
        seat_price_usd: float = 299.0,
        usage_price_per_1k_calls: float = 1.25,
        hybrid_seat_price: float = 99.0,
        hybrid_usage_price_per_1k_calls: float = 0.75,
        churned_users_pct: float = 0.08
    ) -> Dict[str, Any]:
        active_users = int(monthly_active_users * (1.0 - churned_users_pct))
        total_api_calls = active_users * avg_api_calls_per_user

        # Model A: Seat-Based (flat per user/month)
        revenue_seat = round(active_users * seat_price_usd, 2)

        # Model B: Pure Usage-Based (pay-per-call)
        revenue_usage = round((total_api_calls / 1000.0) * usage_price_per_1k_calls, 2)

        # Model C: Hybrid (reduced seat + lower usage rate)
        revenue_hybrid = round(
            active_users * hybrid_seat_price +
            (total_api_calls / 1000.0) * hybrid_usage_price_per_1k_calls,
            2
        )

        best_model = max(
            [("seat_based", revenue_seat), ("usage_based", revenue_usage), ("hybrid", revenue_hybrid)],
            key=lambda x: x[1]
        )

        # Pricing elasticity score: how well pricing scales with heavy users
        heavy_user_multiplier = 3.5
        heavy_usage_calls = active_users * avg_api_calls_per_user * heavy_user_multiplier
        usage_heavy_rev = round((heavy_usage_calls / 1000.0) * usage_price_per_1k_calls, 2)
        seat_heavy_rev = revenue_seat  # seat doesn't scale with usage
        elasticity_uplift_pct = round(((usage_heavy_rev - seat_heavy_rev) / max(1.0, seat_heavy_rev)) * 100, 1)

        return {
            "simulation_id": "pricing_sim_mtr_4471",
            "customer_cohort": customer_cohort,
            "active_users": active_users,
            "total_api_calls_this_month": total_api_calls,
            "model_revenues": {
                "seat_based_usd":  revenue_seat,
                "usage_based_usd": revenue_usage,
                "hybrid_usd":      revenue_hybrid
            },
            "recommended_model": best_model[0],
            "recommended_model_revenue_usd": best_model[1],
            "revenue_uplift_vs_seat_pct": round(((best_model[1] - revenue_seat) / max(1.0, revenue_seat)) * 100, 1),
            "usage_elasticity_uplift_at_3_5x_volume_pct": f"+{elasticity_uplift_pct}%",
            "iteration_confidence_score": round(min(1.0, 0.72 + (active_users / 10000.0)), 2),
            "verdict": "SWITCH_TO_" + best_model[0].upper() + "_MODEL",
            "powered_by": "metronome.com pricing iteration engine"
        }
