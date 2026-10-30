# -*- coding: utf-8 -*-
from client import OpenClawGenParkOutreachWarmer

warmer = OpenClawGenParkOutreachWarmer()

# 1. Sigmoid Warmup Schedule
sched = warmer.calculate_sigmoid_rampup_schedule(target_daily_volume=400, warmup_days=14)
print(f"Sigmoid Warmup: Target {sched['target_daily_volume']}/day over {sched['warmup_days']} days (Total: {sched['total_warmup_volume_dispatched']})")
for d in sched['schedule'][::3]:
    print(f"  Day {d['day']}: {d['recommended_daily_volume']} emails/day (Max burst: {d['max_hourly_burst']}/hr, {d['ramp_percentage']}%)")

# 2. DNS Auth Alignment
auth = warmer.validate_email_auth_alignment_records(
    spf_record="v=spf1 include:_spf.google.com ~all",
    dkim_selector_length=2048,
    dmarc_policy="reject"
)
print(f"\nAuthentication Posture: Score={auth['overall_posture_score']}/100 ({auth['deliverability_posture']})")

# 3. Reputation Decay Forecast
rep = warmer.estimate_domain_reputation_decay(baseline_score=98.0, bounce_rate_pct=2.1, spam_complaint_rate_pct=0.08)
print(f"\nReputation Projection: Score={rep['projected_reputation_score']} ({rep['reputation_status']})")
