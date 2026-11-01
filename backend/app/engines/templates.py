"""Registry of event-specific timeline task templates."""

from app.engines.birthday_templates import BIRTHDAY_TASK_TEMPLATES
from app.engines.community_templates import COMMUNITY_TASK_TEMPLATES
from app.engines.wedding_templates import WEDDING_TASK_TEMPLATES

EVENT_TASK_TEMPLATES: dict[str, list[dict[str, object]]] = {
    "wedding": WEDDING_TASK_TEMPLATES,
    "birthday": BIRTHDAY_TASK_TEMPLATES,
    "community": COMMUNITY_TASK_TEMPLATES,
}
