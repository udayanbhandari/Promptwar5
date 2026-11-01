"""Deterministic fallback data for AI planning outputs."""

from app.schemas.ai_outputs import (
    RiskScenarioItem,
    RiskScenariosOutput,
)

FALLBACK_RISKS: dict[str, RiskScenariosOutput] = {
    "wedding": RiskScenariosOutput(
        risks=[
            RiskScenarioItem(
                scenario_title="Severe Rain & High Winds",
                likelihood="medium",
                impact="high",
                early_warning_sign="Weather forecast 72 hours prior predicts >60% precipitation.",
                fallback_steps="Trigger venue indoor ballroom hold; notify rental company for tent wall drops.",
                cost_impact_percent=8.0,
            ),
            RiskScenarioItem(
                scenario_title="Lead Photographer Emergency No-Show",
                likelihood="low",
                impact="high",
                early_warning_sign="No confirmation reply to final check-in call 24 hours prior.",
                fallback_steps="Activate primary backup shooter designated in contract; dispatch secondary associate.",
                cost_impact_percent=0.0,
            ),
            RiskScenarioItem(
                scenario_title="Guest Attendance Exceeds RSVP Count (+15%)",
                likelihood="medium",
                impact="medium",
                early_warning_sign="Last-minute guest messages indicating plus-ones 48 hours prior.",
                fallback_steps="Direct caterer to expand buffer seating tables; adjust cocktail food quantities.",
                cost_impact_percent=10.0,
            ),
            RiskScenarioItem(
                scenario_title="Audio PA System Failure During Ceremony",
                likelihood="low",
                impact="high",
                early_warning_sign="Audio crackling or wireless mic frequency interference during sound check.",
                fallback_steps="Switch immediately to wired backup microphone and secondary battery amplifier.",
                cost_impact_percent=0.0,
            ),
            RiskScenarioItem(
                scenario_title="Transport / Shuttle Delay Stalls Timeline",
                likelihood="medium",
                impact="medium",
                early_warning_sign="Traffic congestion alerts on primary artery to venue.",
                fallback_steps="Delay ceremony start by 20 minutes; serve welcome infused water to arrived guests.",
                cost_impact_percent=0.0,
            ),
        ]
    ),
    "birthday": RiskScenariosOutput(
        risks=[
            RiskScenarioItem(
                scenario_title="Venue Minimum Spend Shortfall",
                likelihood="medium",
                impact="medium",
                early_warning_sign="RSVP cancellations 24 hours prior reduce bar tabs.",
                fallback_steps="Order premium appetizer platters or dessert package to meet minimum threshold.",
                cost_impact_percent=5.0,
            ),
            RiskScenarioItem(
                scenario_title="Custom Birthday Cake Damaged in Transit",
                likelihood="low",
                impact="medium",
                early_warning_sign="Box shift or delayed bakery courier delivery.",
                fallback_steps=(
                    "Pick up gourmet bakery cupcakes locally; restyle with custom toppers "
                    "and sparkler candles."
                ),
                cost_impact_percent=2.0,
            ),
            RiskScenarioItem(
                scenario_title="Host Sudden Illness / Inability to Attend",
                likelihood="low",
                impact="high",
                early_warning_sign="Host unwell 12-24 hours prior.",
                fallback_steps="Designate co-host to run event or invoke venue 48-hour reschedule clause.",
                cost_impact_percent=0.0,
            ),
            RiskScenarioItem(
                scenario_title="Music Speaker Breakdown at Venue",
                likelihood="low",
                impact="medium",
                early_warning_sign="Bluetooth connection dropped or amplifier overheating.",
                fallback_steps="Deploy auxiliary backup portable Bluetooth boombox kept in vehicle trunk.",
                cost_impact_percent=0.0,
            ),
            RiskScenarioItem(
                scenario_title="Guest Surge Exceeds Private Room Capacity",
                likelihood="medium",
                impact="medium",
                early_warning_sign="More than 10 unannounced guests arrive in first 30 minutes.",
                fallback_steps="Request venue open adjoining patio section or standing cocktail high-tops.",
                cost_impact_percent=7.0,
            ),
        ]
    ),
    "community": RiskScenariosOutput(
        risks=[
            RiskScenarioItem(
                scenario_title="Extreme Heatwave Advisory",
                likelihood="medium",
                impact="high",
                early_warning_sign="Forecast 48 hours prior indicates temperatures > 36°C (97°F).",
                fallback_steps=(
                    "Deploy 2 emergency misting canopies; double water bottle orders; "
                    "shift activities earlier."
                ),
                cost_impact_percent=12.0,
            ),
            RiskScenarioItem(
                scenario_title="Key Volunteer Crew No-Show (>30%)",
                likelihood="high",
                impact="medium",
                early_warning_sign="Fewer than 70% check-ins at morning 06:30 briefing station.",
                fallback_steps="Consolidate duplicate checkpoint stations; reassign crowd safety leads as priority.",
                cost_impact_percent=0.0,
            ),
            RiskScenarioItem(
                scenario_title="Main Generator Power Grid Failure",
                likelihood="low",
                impact="high",
                early_warning_sign="Circuit breaker trip during vendor sound/cooler test.",
                fallback_steps="Engage backup silent inverter generator; isolate sound stage from refrigeration.",
                cost_impact_percent=5.0,
            ),
            RiskScenarioItem(
                scenario_title="Emergency Medical Incident in Crowd",
                likelihood="medium",
                impact="high",
                early_warning_sign="Volunteer radio alert reporting attendee collapse or injury.",
                fallback_steps="Clear designated emergency vehicle access corridor; dispatch on-site EMT first-aiders.",
                cost_impact_percent=0.0,
            ),
            RiskScenarioItem(
                scenario_title="Sanitation Overflow at High Peak Hours",
                likelihood="medium",
                impact="medium",
                early_warning_sign="Trash bins reaching capacity by midday.",
                fallback_steps="Deploy reserve heavy-duty rolling bins; dispatch roaming volunteer clean sweep team.",
                cost_impact_percent=2.0,
            ),
        ]
    ),
}
