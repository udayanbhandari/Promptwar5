"""Deterministic fallback data for AI planning outputs."""

from app.schemas.ai_outputs import (
    VendorCategoriesOutput,
    VendorCategoryRecommendation,
)

FALLBACK_VENDOR_CATEGORIES: dict[str, VendorCategoriesOutput] = {
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
                    "Are we restricted to an exclusive preferred vendor list or free to bring "
                    "licensed outside vendors?",
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
                    "Do you have an auxiliary cable, Bluetooth, or screen for playing "
                    "custom playlists and video reels?",
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
