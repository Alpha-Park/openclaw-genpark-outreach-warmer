# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Outreach Warmer Client
Pure Python Standard Library (Zero External Dependencies)
Implements sigmoid email ramp-up volume progression, SPF/DKIM/DMARC authentication posture scoring,
and sender reputation domain decay modeling.
"""

import math
from typing import Dict, Any, List, Optional

class OpenClawGenParkOutreachWarmer:
    """
    Email deliverability optimization and domain warmup engine for outbound AI agents.
    """

    def __init__(self):
        pass

    def calculate_sigmoid_rampup_schedule(
        self,
        target_daily_volume: int = 500,
        warmup_days: int = 21,
        midpoint_day: float = 10.5,
        growth_steepness: float = 0.35
    ) -> Dict[str, Any]:
        """
        Calculates daily sending volume schedule using a continuous generalized logistic (sigmoid) function:
          V(t) = ceil( target_volume / (1 + exp(-k * (t - t0))) )
        """
        days = max(7, warmup_days)
        target = max(10, target_daily_volume)
        schedule = []
        cumulative_volume = 0

        for day in range(1, days + 1):
            # Sigmoid formula
            exponent = -growth_steepness * (day - midpoint_day)
            sigmoid_val = 1.0 / (1.0 + math.exp(max(-50.0, min(50.0, exponent))))
            daily_vol = max(5, math.ceil(target * sigmoid_val))
            
            # Safe burst limit (no more than 30% of daily total per hour)
            max_hourly_burst = max(2, math.ceil(daily_vol * 0.25))
            cumulative_volume += daily_vol

            schedule.append({
                "day": day,
                "recommended_daily_volume": daily_vol,
                "max_hourly_burst": max_hourly_burst,
                "ramp_percentage": round((daily_vol / target) * 100.0, 1),
                "cumulative_volume": cumulative_volume
            })

        return {
            "target_daily_volume": target,
            "warmup_days": days,
            "total_warmup_volume_dispatched": cumulative_volume,
            "schedule": schedule
        }

    def validate_email_auth_alignment_records(
        self,
        spf_record: str,
        dkim_selector_length: int = 2048,
        dmarc_policy: str = "reject"
    ) -> Dict[str, Any]:
        """
        Evaluates email authentication alignment posture across SPF, DKIM, and DMARC.
        Assigns an overall deliverability security posture score (0 - 100).
        """
        score = 0.0
        checks = {}

        # 1. SPF Evaluation (35 points max)
        spf_score = 0.0
        spf_clean = spf_record.strip().lower()
        if "v=spf1" in spf_clean:
            spf_score += 15.0
            if "-all" in spf_clean:
                spf_score += 20.0  # Hard fail is strict
                checks["spf_posture"] = "STRICT_HARDFAIL"
            elif "~all" in spf_clean:
                spf_score += 12.0  # Soft fail is acceptable
                checks["spf_posture"] = "MODERATE_SOFTFAIL"
            else:
                checks["spf_posture"] = "WEAK_PERMISSIVE"
        else:
            checks["spf_posture"] = "MISSING_OR_INVALID"
        score += spf_score

        # 2. DKIM Evaluation (35 points max)
        dkim_score = 0.0
        if dkim_selector_length >= 2048:
            dkim_score = 35.0
            checks["dkim_posture"] = "ROBUST_2048_BIT"
        elif dkim_selector_length >= 1024:
            dkim_score = 20.0
            checks["dkim_posture"] = "LEGACY_1024_BIT"
        else:
            checks["dkim_posture"] = "INSUFFICIENT_KEY_LENGTH"
        score += dkim_score

        # 3. DMARC Policy Evaluation (30 points max)
        dmarc_clean = dmarc_policy.strip().lower()
        dmarc_score = 0.0
        if dmarc_clean == "reject":
            dmarc_score = 30.0
            checks["dmarc_posture"] = "STRICT_REJECT"
        elif dmarc_clean == "quarantine":
            dmarc_score = 20.0
            checks["dmarc_posture"] = "MODERATE_QUARANTINE"
        elif dmarc_clean == "none":
            dmarc_score = 8.0
            checks["dmarc_posture"] = "MONITORING_ONLY"
        else:
            checks["dmarc_posture"] = "MISSING_POLICY"
        score += dmarc_score

        posture = "EXCELLENT" if score >= 85 else ("ACCEPTABLE" if score >= 65 else "AT_RISK_SPAM_BOX")

        return {
            "overall_posture_score": round(score, 1),
            "deliverability_posture": posture,
            "spf_score": spf_score,
            "dkim_score": dkim_score,
            "dmarc_score": dmarc_score,
            "detailed_checks": checks
        }

    def estimate_domain_reputation_decay(
        self,
        baseline_score: float = 95.0,
        bounce_rate_pct: float = 1.5,
        spam_complaint_rate_pct: float = 0.05,
        days_idle: int = 0
    ) -> Dict[str, Any]:
        """
        Estimates sender reputation degradation under bounce penalties, complaint multipliers,
        and inactive dormancy decay:
          Penalty = (Bounce * 4.0) + (Spam * 50.0) + (DaysIdle * 0.5)
        """
        bounce_penalty = max(0.0, bounce_rate_pct) * 4.0
        spam_penalty = max(0.0, spam_complaint_rate_pct) * 60.0
        dormancy_penalty = max(0, days_idle) * 0.4

        total_penalty = bounce_penalty + spam_penalty + dormancy_penalty
        projected_reputation = max(0.0, round(baseline_score - total_penalty, 2))

        status = "HEALTHY" if projected_reputation >= 80 else ("CAUTION" if projected_reputation >= 60 else "THROTTLED_SUSPENDED")

        return {
            "baseline_score": baseline_score,
            "projected_reputation_score": projected_reputation,
            "reputation_status": status,
            "penalties": {
                "bounce_penalty": round(bounce_penalty, 2),
                "spam_complaint_penalty": round(spam_penalty, 2),
                "dormancy_penalty": round(dormancy_penalty, 2),
                "total_penalty": round(total_penalty, 2)
            }
        }
