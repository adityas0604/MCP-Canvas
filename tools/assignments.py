from datetime import datetime, timezone
from canvas_client import CanvasClient

client = CanvasClient()


def get_course_list() -> str:
    """Get all active enrolled courses."""
    courses = client._get("courses", {"enrollment_state": "active", "include[]": "term"})
    if not courses:
        return "No active courses found."
    lines = ["📚 **Your Active Courses:**\n"]
    for c in courses:
        term = c.get("term", {}).get("name", "Unknown Term")
        lines.append(f"  • [{c['id']}] {c.get('name', 'Unnamed')} — {term}")
    return "\n".join(lines)


def get_assignments(course_id: int = None) -> str:
    """Get all assignments, optionally filtered by course."""
    if course_id:
        courses = [{"id": course_id, "name": f"Course {course_id}"}]
    else:
        courses = client._get("courses", {"enrollment_state": "active"})

    all_assignments = []
    for course in courses:
        cid = course["id"]
        cname = course.get("name", f"Course {cid}")
        try:
            assignments = client._get(f"courses/{cid}/assignments", {
                "include[]": ["submission"],
                "order_by": "due_at"
            })
            for a in assignments:
                a["_course_name"] = cname
                all_assignments.append(a)
        except Exception:
            continue

    if not all_assignments:
        return "No assignments found."

    lines = ["📝 **Assignments:**\n"]
    for a in all_assignments:
        due = a.get("due_at")
        due_str = datetime.fromisoformat(due.replace("Z", "+00:00")).strftime("%b %d, %Y %I:%M %p") if due else "No due date"
        pts = a.get("points_possible", "N/A")
        lines.append(f"  • {a['_course_name']}: **{a['name']}**")
        lines.append(f"    Due: {due_str} | Points: {pts}")
    return "\n".join(lines)


def get_upcoming_deadlines(days: int = 7) -> str:
    """Get assignments due within the next N days."""
    courses = client._get("courses", {"enrollment_state": "active"})
    now = datetime.now(timezone.utc)
    upcoming = []

    for course in courses:
        cid = course["id"]
        cname = course.get("name", f"Course {cid}")
        try:
            assignments = client._get(f"courses/{cid}/assignments", {"order_by": "due_at"})
            for a in assignments:
                due = a.get("due_at")
                if not due:
                    continue
                due_dt = datetime.fromisoformat(due.replace("Z", "+00:00"))
                delta = (due_dt - now).days
                if 0 <= delta <= days:
                    upcoming.append((delta, due_dt, cname, a))
        except Exception:
            continue

    if not upcoming:
        return f"🎉 No assignments due in the next {days} days!"

    upcoming.sort(key=lambda x: x[0])
    lines = [f"⏰ **Upcoming Deadlines (Next {days} Days):**\n"]
    for delta, due_dt, cname, a in upcoming:
        due_str = due_dt.strftime("%b %d, %Y %I:%M %p")
        urgency = "🔴" if delta <= 1 else "🟡" if delta <= 3 else "🟢"
        lines.append(f"  {urgency} **{a['name']}** ({cname})")
        lines.append(f"     Due: {due_str} — in {delta} day(s)")
    return "\n".join(lines)


def get_assignment_details(course_id: int, assignment_id: int) -> str:
    """Get full details of a specific assignment."""
    a = client._get(f"courses/{course_id}/assignments/{assignment_id}")
    if not a:
        return "Assignment not found."

    due = a.get("due_at")
    due_str = datetime.fromisoformat(due.replace("Z", "+00:00")).strftime("%b %d, %Y %I:%M %p") if due else "No due date"

    import re
    description = re.sub(r"<[^>]+>", "", a.get("description") or "No description provided.")

    return (
        f"📋 **{a['name']}**\n"
        f"  Points: {a.get('points_possible', 'N/A')}\n"
        f"  Due: {due_str}\n"
        f"  Submission Type: {', '.join(a.get('submission_types', []))}\n"
        f"  Description:\n{description[:1000]}"
    )


def get_submission_status(course_id: int = None) -> str:
    """Check submission status (submitted vs missing) for assignments."""
    if course_id:
        courses = [{"id": course_id, "name": f"Course {course_id}"}]
    else:
        courses = client._get("courses", {"enrollment_state": "active"})

    lines = ["📊 **Submission Status:**\n"]
    for course in courses:
        cid = course["id"]
        cname = course.get("name", f"Course {cid}")
        try:
            assignments = client._get(f"courses/{cid}/assignments", {"include[]": "submission"})
            submitted, missing = [], []
            for a in assignments:
                sub = a.get("submission", {})
                state = sub.get("workflow_state", "unsubmitted")
                if state in ("submitted", "graded"):
                    submitted.append(a["name"])
                elif a.get("due_at"):
                    missing.append(a["name"])

            lines.append(f"**{cname}**")
            lines.append(f"  ✅ Submitted: {len(submitted)} | ❌ Missing/Pending: {len(missing)}")
            for m in missing[:5]:
                lines.append(f"    • {m}")
            if len(missing) > 5:
                lines.append(f"    ... and {len(missing) - 5} more")
        except Exception:
            continue

    return "\n".join(lines)
