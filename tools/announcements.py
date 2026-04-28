import re
from datetime import datetime
from canvas_client import CanvasClient

client = CanvasClient()


def _strip_html(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html or "").strip()


def get_announcements(course_id: int = None, limit: int = 5) -> str:
    """Get recent announcements across all courses or a specific course."""
    if course_id:
        courses = [{"id": course_id, "name": f"Course {course_id}"}]
    else:
        courses = client._get("courses", {"enrollment_state": "active"})

    all_announcements = []
    for course in courses:
        cid = course["id"]
        cname = course.get("name", f"Course {cid}")
        try:
            announcements = client._get(
                f"courses/{cid}/discussion_topics",
                {"only_announcements": True, "order_by": "posted_at", "per_page": limit}
            )
            for a in announcements:
                a["_course_name"] = cname
                all_announcements.append(a)
        except Exception:
            continue

    if not all_announcements:
        return "No announcements found."

    # Sort by posted date
    all_announcements.sort(key=lambda x: x.get("posted_at", ""), reverse=True)

    lines = [f"📢 **Recent Announcements (Latest {limit}):**\n"]
    for a in all_announcements[:limit]:
        posted = a.get("posted_at", "")
        date_str = datetime.fromisoformat(posted.replace("Z", "+00:00")).strftime("%b %d, %Y") if posted else "Unknown date"
        message = _strip_html(a.get("message", ""))[:300]
        lines.append(f"  📌 **{a.get('title', 'Untitled')}** — {a['_course_name']}")
        lines.append(f"     Posted: {date_str}")
        lines.append(f"     {message}...")
        lines.append("")

    return "\n".join(lines)


def get_course_modules(course_id: int) -> str:
    """Get all modules for a specific course."""
    modules = client._get(f"courses/{course_id}/modules")

    if not modules:
        return f"No modules found for course {course_id}."

    lines = [f"📦 **Modules for Course {course_id}:**\n"]
    for m in modules:
        state = m.get("state", "unlocked")
        icon = "🔒" if state == "locked" else "✅" if state == "completed" else "📂"
        items_count = m.get("items_count", 0)
        lines.append(f"  {icon} **{m['name']}** ({items_count} items)")

    return "\n".join(lines)


def get_module_items(course_id: int, module_id: int) -> str:
    """Get all items within a specific module."""
    items = client._get(f"courses/{course_id}/modules/{module_id}/items")

    if not items:
        return "No items found in this module."

    type_icons = {
        "Assignment": "📝",
        "Quiz": "❓",
        "File": "📄",
        "Page": "📃",
        "Discussion": "💬",
        "ExternalUrl": "🔗",
        "SubHeader": "📌",
    }

    lines = [f"📋 **Module Items:**\n"]
    for item in items:
        item_type = item.get("type", "Unknown")
        icon = type_icons.get(item_type, "•")
        completion = item.get("completion_requirement", {})
        completed = completion.get("completed", False)
        check = "✅" if completed else "⬜"
        lines.append(f"  {check} {icon} {item.get('title', 'Untitled')} [{item_type}]")

    return "\n".join(lines)
