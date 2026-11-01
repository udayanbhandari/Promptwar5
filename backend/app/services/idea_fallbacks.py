"""Deterministic fallback data for AI planning outputs."""

from app.schemas.ai_outputs import (
    IdeasOutput,
    PersonalizedIdea,
)

FALLBACK_IDEAS: dict[str, IdeasOutput] = {
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
