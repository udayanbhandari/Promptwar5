"""Deterministic rule-based fallback templates for all 5 AI output domains.

Guarantees 100% application functionality when Gemini API is offline,
unconfigured, or experiencing network or quota limitations.
"""

from typing import Dict
from app.schemas.ai_outputs import (
    BudgetSplitOutput,
    CategoryPercentage,
    IdeasOutput,
    PersonalizedIdea,
    RiskScenarioItem,
    RiskScenariosOutput,
    VendorBriefOutput,
    VendorCategoriesOutput,
    VendorCategoryRecommendation,
)


# -----------------------------------------------------------------------------
# 1. Fallback Budget Splits (Percentages sum to exactly 100.0)
# -----------------------------------------------------------------------------
FALLBACK_BUDGETS: Dict[str, BudgetSplitOutput] = {
    "wedding": BudgetSplitOutput(
        categories=[
            CategoryPercentage(category="Catering & Bar", percentage=40.0, reason="Core guest hospitality experience."),
            CategoryPercentage(category="Venue & Rentals", percentage=25.0, reason="Secures site and essential tables/seating."),
            CategoryPercentage(category="Photography & Video", percentage=15.0, reason="Preserves lifelong memories."),
            CategoryPercentage(category="Floral & Styling", percentage=10.0, reason="Transforms atmosphere and aesthetic."),
            CategoryPercentage(category="Music & Entertainment", percentage=5.0, reason="Sets celebration energy."),
            CategoryPercentage(category="Contingency Buffer", percentage=5.0, reason="Covers day-of emergency expenses."),
        ]
    ),
    "birthday": BudgetSplitOutput(
        categories=[
            CategoryPercentage(category="Food, Drinks & Cake", percentage=45.0, reason="Main enjoyment factor for celebratory gatherings."),
            CategoryPercentage(category="Venue / Activity Fees", percentage=30.0, reason="Space rental, entry tickets, or table reservations."),
            CategoryPercentage(category="Decor & Visual Theme", percentage=12.0, reason="Balloons, lighting, and signage."),
            CategoryPercentage(category="Entertainment & Games", percentage=8.0, reason="DJ, playlist gear, or group activities."),
            CategoryPercentage(category="Contingency Buffer", percentage=5.0, reason="Tips and last-minute supplies."),
        ]
    ),
    "community": BudgetSplitOutput(
        categories=[
            CategoryPercentage(category="Permits, Safety & Sanitation", percentage=25.0, reason="Mandatory city compliance, first-aid, and waste management."),
            CategoryPercentage(category="Staging, Tents & Equipment", percentage=35.0, reason="Infrastructure for mass outdoor/indoor attendance."),
            CategoryPercentage(category="Promotion & Signage", percentage=15.0, reason="Outreach, banners, and directional wayfinding."),
            CategoryPercentage(category="Hydration & Refreshments", percentage=15.0, reason="Volunteer fuel and participant water stations."),
            CategoryPercentage(category="Contingency Fund", percentage=10.0, reason="Weather adjustments and equipment repairs."),
        ]
    ),
}


def get_fallback_budget_split(event_type: str) -> BudgetSplitOutput:
    """Return deterministic budget allocation percentages."""
    normalized = event_type.lower().strip()
    return FALLBACK_BUDGETS.get(normalized, FALLBACK_BUDGETS["community"])


# -----------------------------------------------------------------------------
# 2. Fallback Personalized Ideas (Exactly 5 aspects)
# -----------------------------------------------------------------------------
FALLBACK_IDEAS: Dict[str, IdeasOutput] = {
    "wedding": IdeasOutput(
        ideas=[
            PersonalizedIdea(
                aspect="theme",
                title="Timeless Botanical Elegance",
                description="Organic greenery, warm candlelit tables, and muted neutral accents.",
                cost_tier="medium",
                why_it_fits="Provides a sophisticated ambiance that complements any venue gracefully.",
            ),
            PersonalizedIdea(
                aspect="decor",
                title="Suspended Greenery & Fairy Light Canopy",
                description="Hanging eucalyptus garlands interwoven with warm micro-LED lights.",
                cost_tier="medium",
                why_it_fits="Creates high visual drama without overcrowding table guest space.",
            ),
            PersonalizedIdea(
                aspect="food",
                title="Seasonal Grazing Table & Signature Spritz",
                description="Artisanal cheese and fruit spread during cocktail hour with rosemary spritzers.",
                cost_tier="low",
                why_it_fits="Encourages relaxed guest mingling before formal dinner service.",
            ),
            PersonalizedIdea(
                aspect="entertainment",
                title="Acoustic Duo Transitioning to Curated Live DJ",
                description="Mellow acoustic guitars for vows, moving into high-energy dance floor anthems.",
                cost_tier="medium",
                why_it_fits="Adapts audio pacing seamlessly across day-of emotional phases.",
            ),
            PersonalizedIdea(
                aspect="memorable_touch",
                title="Audio Guestbook Vintage Telephone",
                description="Vintage rotary phone where guests leave heartfelt voicemail messages.",
                cost_tier="low",
                why_it_fits="Captures authentic guest emotions and voices as lasting keepsakes.",
            ),
        ]
    ),
    "birthday": IdeasOutput(
        ideas=[
            PersonalizedIdea(
                aspect="theme",
                title="Retro Neon Arcade & Synthwave",
                description="Vibrant magenta and cyan neon glow with nostalgic arcade touches.",
                cost_tier="low",
                why_it_fits="High-energy, interactive theme that immediately breaks the ice.",
            ),
            PersonalizedIdea(
                aspect="decor",
                title="Custom LED Monogram & Balloon Garland Wall",
                description="Photo-ready backdrop featuring birthday year and vivid neon signage.",
                cost_tier="low",
                why_it_fits="Guarantees share-worthy photo opportunities for guests.",
            ),
            PersonalizedIdea(
                aspect="food",
                title="Gourmet Slider Flight & Custom Cupcake Tower",
                description="Miniature smash burgers, vegan sliders, and color-matched cupcakes.",
                cost_tier="medium",
                why_it_fits="Finger food that keeps people socializing without sitting down.",
            ),
            PersonalizedIdea(
                aspect="entertainment",
                title="Retro Console Station & Interactive Trivia",
                description="Classic video game tournaments and custom host trivia via smartphones.",
                cost_tier="low",
                why_it_fits="Engages competitive groups of all ages effortlessly.",
            ),
            PersonalizedIdea(
                aspect="memorable_touch",
                title="Personalized Retro Ticket Favors",
                description="Golden arcade token keychains engraved with the event date.",
                cost_tier="low",
                why_it_fits="A charming, tangible reminder of a celebratory evening.",
            ),
        ]
    ),
    "community": IdeasOutput(
        ideas=[
            PersonalizedIdea(
                aspect="theme",
                title="Vibrant Neighborhood Harvest & Fair",
                description="Celebration of local arts, green living, and community connection.",
                cost_tier="low",
                why_it_fits="Welcoming and accessible across diverse community age demographics.",
            ),
            PersonalizedIdea(
                aspect="decor",
                title="Burlap Bunting & Directional Wooden Wayfinding",
                description="Eco-friendly banners, reclaimed wood signage, and solar fairy lights.",
                cost_tier="low",
                why_it_fits="Sustainable, reusable outdoor materials that withstand wind and weather.",
            ),
            PersonalizedIdea(
                aspect="food",
                title="Local Food Truck Showcase & Hydration Hubs",
                description="Curated neighborhood food trucks and complimentary iced water stations.",
                cost_tier="low",
                why_it_fits="Eliminates catering overhead while supporting local small food businesses.",
            ),
            PersonalizedIdea(
                aspect="entertainment",
                title="Acoustic Community Stage & Lawn Games",
                description="Open mic sets from local musicians, giant Jenga, and cornhole boards.",
                cost_tier="low",
                why_it_fits="Allows fluid, self-paced attendee engagement throughout the event.",
            ),
            PersonalizedIdea(
                aspect="memorable_touch",
                title="Collaborative Community Mural Canvas",
                description="Large outdoor canvas where attendees add their handprint or greeting.",
                cost_tier="low",
                why_it_fits="Creates a permanent piece of community art to display locally.",
            ),
        ]
    ),
}


def get_fallback_ideas(event_type: str) -> IdeasOutput:
    """Return deterministic 5-part creative idea bundle."""
    normalized = event_type.lower().strip()
    return FALLBACK_IDEAS.get(normalized, FALLBACK_IDEAS["community"])


# -----------------------------------------------------------------------------
# 3. Fallback Vendor Categories (5 questions, 3 red flags each)
# -----------------------------------------------------------------------------
FALLBACK_VENDOR_CATEGORIES: Dict[str, VendorCategoriesOutput] = {
    "wedding": VendorCategoriesOutput(
        categories=[
            VendorCategoryRecommendation(
                category="Catering & Bar Service",
                questions=[
                    "Are kitchen cleanup, trash removal, and table bussing included in your quote?",
                    "What is your server-to-guest ratio for plated or buffet dinner?",
                    "Can you accommodate dietary restrictions (vegan, gluten-free, halal) at no extra surcharge?",
                    "Do you provide a tasting session prior to signing the contract?",
                    "What is your policy regarding unconsumed alcohol or leftover food?",
                ],
                red_flags=[
                    "Refusal to provide an itemized quote with service fees and gratuities.",
                    "No valid food handler licensing or liability insurance coverage.",
                    "Vague answers about who will actually manage the kitchen day-of.",
                ],
            ),
            VendorCategoryRecommendation(
                category="Venue Management",
                questions=[
                    "What are the exact load-in and load-out hour restrictions for vendors?",
                    "Is there a mandatory sound decibel curfew or music shut-off cutoff time?",
                    "What is the venue's backup plan if rain occurs during an outdoor ceremony?",
                    "Are we restricted to an exclusive preferred vendor list or free to bring licensed outside vendors?",
                    "Is an on-site facility manager present for the entire duration of the event?",
                ],
                red_flags=[
                    "Hidden cleaning, security, or overtime fees not disclosed in initial rate sheet.",
                    "Non-functional ADA accessibility or inadequate restroom facilities for guest count.",
                    "No written weather contingency plan.",
                ],
            ),
            VendorCategoryRecommendation(
                category="Photography & Video",
                questions=[
                    "Will you personally shoot the event, or will associate shooters be assigned?",
                    "What is your guaranteed delivery timeline for digital galleries and albums?",
                    "What redundant backup equipment (cameras, dual SD slots, lenses) do you bring?",
                    "Do we receive full personal printing and high-resolution download rights?",
                    "What is your protocol if an emergency prevents you from attending on the date?",
                ],
                red_flags=[
                    "Portfolio consists solely of staged styled-shoots with no full wedding gallery.",
                    "No dual-card backup camera bodies.",
                    "Delivery timeline exceeds 16 weeks without clear contractual milestones.",
                ],
            ),
        ]
    ),
    "birthday": VendorCategoriesOutput(
        categories=[
            VendorCategoryRecommendation(
                category="Venue or Private Room",
                questions=[
                    "What is the food/drink minimum spend required to waive room rental fees?",
                    "Can we bring in outside specialty items like custom birthday cakes?",
                    "Do you have an auxiliary cable, Bluetooth, or screen for playing custom playlists and video reels?",
                    "What time are we granted access for setting up decorations?",
                    "What is the policy for cancellation or rescheduling due to host illness?",
                ],
                red_flags=[
                    "Strict cake-cutting fees exceeding the cost of the cake itself.",
                    "Unclear minimum spend policies that trigger unexpected card charges.",
                    "Unreliable sound equipment with no staff available to troubleshoot.",
                ],
            ),
            VendorCategoryRecommendation(
                category="Entertainment & Music",
                questions=[
                    "Do you bring your own PA sound system, microphones, and lighting rigs?",
                    "Can we provide a 'must-play' and 'do-not-play' list in advance?",
                    "What is your overtime hourly rate if the party continues past scheduled time?",
                    "How do you handle guest requests throughout the night?",
                    "What power outlet requirements do you need from the venue?",
                ],
                red_flags=[
                    "Inability to demonstrate past live set recordings.",
                    "Refusal to honor a strict do-not-play list.",
                    "Demands 100% cash payment with no signed receipt or contract.",
                ],
            ),
        ]
    ),
    "community": VendorCategoriesOutput(
        categories=[
            VendorCategoryRecommendation(
                category="Equipment & Tent Rentals",
                questions=[
                    "Do you provide delivery, setup, weighting/staking, and teardown services?",
                    "Are your tents rated for heavy wind and adverse rain conditions?",
                    "What is the emergency dispatch number on the morning of setup?",
                    "Can equipment be delivered the prior evening without extra storage charge?",
                    "Do you provide certified generator power distribution boxes?",
                ],
                red_flags=[
                    "Tents secured with insufficient water barrels or inadequate wind anchoring.",
                    "History of delayed morning deliveries that derail public kickoff.",
                    "Unsanitary or visibly damaged rental inventory.",
                ],
            ),
            VendorCategoryRecommendation(
                category="Sanitation & Waste Management",
                questions=[
                    "How many portable restrooms and handwash stations are recommended for our attendee count?",
                    "Is continuous mid-event servicing and restocking included for all-day events?",
                    "Do you provide separate recycling and compost bins with appropriate signage?",
                    "When will pump-out and final unit removal take place post-event?",
                    "Are ADA-compliant wheelchair accessible units provided?",
                ],
                red_flags=[
                    "Insufficient unit count below municipal health code minimums.",
                    "No dedicated handwashing stations.",
                    "Unclear pickup schedule leading to city fines for street obstruction.",
                ],
            ),
        ]
    ),
}


def get_fallback_vendor_categories(event_type: str) -> VendorCategoriesOutput:
    """Return deterministic vendor checklist with questions and red flags."""
    normalized = event_type.lower().strip()
    return FALLBACK_VENDOR_CATEGORIES.get(normalized, FALLBACK_VENDOR_CATEGORIES["community"])


# -----------------------------------------------------------------------------
# 4. Fallback Risk Scenarios (Plan B Matrix with exactly 5 scenarios)
# -----------------------------------------------------------------------------
FALLBACK_RISKS: Dict[str, RiskScenariosOutput] = {
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
                fallback_steps="Pick up gourmet bakery cupcakes locally; restyle with custom toppers and sparkler candles.",
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
                fallback_steps="Deploy 2 emergency misting canopies; double water bottle orders; shift activities earlier.",
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


def get_fallback_risk_scenarios(event_type: str) -> RiskScenariosOutput:
    """Return deterministic Plan B risk scenarios."""
    normalized = event_type.lower().strip()
    return FALLBACK_RISKS.get(normalized, FALLBACK_RISKS["community"])


# -----------------------------------------------------------------------------
# 5. Fallback Vendor Brief
# -----------------------------------------------------------------------------
def get_fallback_vendor_brief(
    vendor_category: str,
    event_type: str,
    event_date: str = "Upcoming Date",
    guest_count: int = 50,
    city: str = "Local City",
) -> VendorBriefOutput:
    """Return ready-to-send vendor inquiry and comparison checklist."""
    category_clean = vendor_category.strip().title()
    event_clean = event_type.strip().title()

    enquiry_msg = (
        f"Hi there! I hope you're having a great week.\n\n"
        f"I am organizing a {event_clean} in {city} on {event_date} for approximately "
        f"{guest_count} guests. We are currently scouting for an experienced {category_clean} "
        f"partner who delivers high-quality service and seamless coordination.\n\n"
        f"Could you please share:\n"
        f"1. Your availability on {event_date}?\n"
        f"2. Your standard packages and pricing guides for ~{guest_count} attendees?\n"
        f"3. An overview of what deliverables and setup/teardown time are included?\n\n"
        f"Looking forward to hearing from you and discussing how we might collaborate!\n\n"
        f"Warm regards."
    )

    checklist = [
        "Transparent pricing with all service charges, taxes, and fees explicitly itemized.",
        "Clear overtime rate and cancellation/reschedule policy stated in writing.",
        "Possession of active business liability insurance and required health/safety permits.",
        "Demonstrated experience with similar event scale and venue constraints.",
        "Contingency plan or backup personnel in case of equipment failure or illness.",
    ]

    return VendorBriefOutput(
        enquiry_message=enquiry_msg,
        comparison_checklist=checklist,
    )
