from datetime import datetime, timezone, timedelta
from canvas_client import CanvasClient

client = CanvasClient()


def get_calendar_events(days: int = 14) -> str:
    """Get all calendar events (assignments + events) for the next N days."""
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)

    events = client._get("calendar_events", {
        "start_date": now.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "type": "event",
        "per_page": 50
    })

    assignments = client._get("calendar_events", {
        "start_date": now.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "type": "assignment",
        "per_page": 50
    })

    all_events = [(e, "📅") for e in events] + [(a, "📝") for a in assignments]
    all_events.sort(key=lambda x: x[0].get("start_at", ""))

    if not all_events:
        return f"No calendar events in the next {days} days."

    lines = [f"🗓️ **Calendar — Next {days} Days:**\n"]
    current_day = None

    for event, icon in all_events:
        start = event.get("start_at", "")
        if start:
            dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            day_label = dt.strftime("%A, %B %d")
            time_str = dt.strftime("%I:%M %p")
        else:
            day_label = "No date"
            time_str = ""

        if day_label != current_day:
            lines.append(f"\n  **{day_label}**")
            current_day = day_label

        title = event.get("title", "Untitled")
        context = event.get("context_name", "")
        lines.append(f"    {icon} {time_str} — {title} ({context})")

    return "\n".join(lines)


def get_weekly_schedule() -> str:
    """Get a structured week-at-a-glance view of all due items."""
    now = datetime.now(timezone.utc)
    # Start from Monday of current week
    monday = now - timedelta(days=now.weekday())
    sunday = monday + timedelta(days=6)

    assignments = client._get("calendar_events", {
        "start_date": monday.strftime("%Y-%m-%d"),
        "end_date": sunday.strftime("%Y-%m-%d"),
        "type": "assignment",
        "per_page": 100
    })

    by_day = {i: [] for i in range(7)}
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for a in assignments:
        start = a.get("start_at", "")
        if start:
            dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            weekday = dt.weekday()
            by_day[weekday].append((dt, a.get("title", "Untitled"), a.get("context_name", "")))

    lines = ["📅 **This Week's Schedule:**\n"]
    for i, day in enumerate(day_names):
        date = (monday + timedelta(days=i)).strftime("%b %d")
        is_today = (monday + timedelta(days=i)).date() == now.date()
        prefix = "👉 " if is_today else "   "
        lines.append(f"{prefix}**{day} ({date})**")

        if by_day[i]:
            for dt, title, context in sorted(by_day[i]):
                lines.append(f"    📝 {dt.strftime('%I:%M %p')} — {title} ({context})")
        else:
            lines.append("    — Nothing due")

    return "\n".join(lines)


def get_upcoming_events(limit: int = 10) -> str:
    """Get the next N upcoming events/deadlines across all courses."""
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=30)

    assignments = client._get("calendar_events", {
        "start_date": now.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "type": "assignment",
        "per_page": limit
    })

    events = client._get("calendar_events", {
        "start_date": now.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "type": "event",
        "per_page": limit
    })

    combined = sorted(
        [(e, "📝") for e in assignments] + [(e, "📅") for e in events],
        key=lambda x: x[0].get("start_at", "")
    )[:limit]

    if not combined:
        return "No upcoming events in the next 30 days."

    lines = [f"⏭️ **Next {limit} Upcoming Events:**\n"]
    for event, icon in combined:
        start = event.get("start_at", "")
        if start:
            dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            delta_days = (dt - now).days
            due_str = dt.strftime("%a, %b %d %I:%M %p")
        else:
            due_str = "No date"
            delta_days = 99

        title = event.get("title", "Untitled")
        context = event.get("context_name", "")
        lines.append(f"  {icon} **{title}** ({context})")
        lines.append(f"     {due_str} — {delta_days} day(s) away")

    return "\n".join(lines)
