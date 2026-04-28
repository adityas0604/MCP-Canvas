from canvas_client import CanvasClient

client = CanvasClient()

def _percent_to_letter(pct: float) -> str:
    if pct >= 93: return "A"
    if pct >= 90: return "A-"
    if pct >= 87: return "B+"
    if pct >= 83: return "B"
    if pct >= 80: return "B-"
    if pct >= 77: return "C+"
    if pct >= 73: return "C"
    if pct >= 70: return "C-"
    if pct >= 67: return "D+"
    if pct >= 63: return "D"
    if pct >= 60: return "D-"
    return "F"


def get_course_grades() -> str:
    """Get current grades for all active courses."""
    enrollments = client._get("courses", {
        "enrollment_state": "active",
        "include[]": "total_scores"
    })

    if not enrollments:
        return "No grade data found."

    lines = ["📊 **Current Course Grades:**\n"]
    for course in enrollments:
        cname = course.get("name", "Unknown Course")
        enrollment = course.get("enrollments", [{}])[0]
        score = enrollment.get("computed_current_score")
        grade = enrollment.get("computed_current_grade")

        if score is not None:
            letter = grade or _percent_to_letter(score)
            bar_filled = int(score / 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            lines.append(f"  **{cname}**")
            lines.append(f"    [{bar}] {score:.1f}% — {letter}")
        else:
            lines.append(f"  **{cname}**: No grade data yet")

    return "\n".join(lines)


def get_grade_breakdown(course_id: int) -> str:
    """Get detailed assignment-level grade breakdown for a course."""
    assignments = client._get(f"courses/{course_id}/assignments", {
        "include[]": "submission",
        "order_by": "due_at"
    })

    if not assignments:
        return "No assignment data found for this course."

    lines = [f"📋 **Grade Breakdown for Course {course_id}:**\n"]
    total_earned = 0
    total_possible = 0

    for a in assignments:
        sub = a.get("submission", {})
        pts_possible = a.get("points_possible") or 0
        pts_earned = sub.get("score")
        state = sub.get("workflow_state", "unsubmitted")

        if pts_earned is not None and pts_possible:
            pct = (pts_earned / pts_possible) * 100
            total_earned += pts_earned
            total_possible += pts_possible
            lines.append(f"  ✅ {a['name']}: {pts_earned}/{pts_possible} ({pct:.1f}%)")
        elif state == "unsubmitted":
            lines.append(f"  ⬜ {a['name']}: Not submitted ({pts_possible} pts)")
        else:
            lines.append(f"  ⏳ {a['name']}: Awaiting grade ({pts_possible} pts)")

    if total_possible > 0:
        overall = (total_earned / total_possible) * 100
        lines.append(f"\n  **Overall: {total_earned}/{total_possible} ({overall:.1f}%) — {_percent_to_letter(overall)}**")

    return "\n".join(lines)


def get_missing_assignments() -> str:
    """List all missing or unsubmitted assignments across courses."""
    courses = client._get("courses", {"enrollment_state": "active"})
    lines = ["❌ **Missing / Unsubmitted Assignments:**\n"]
    found_any = False

    for course in courses:
        cid = course["id"]
        cname = course.get("name", f"Course {cid}")
        try:
            assignments = client._get(f"courses/{cid}/assignments", {"include[]": "submission"})
            missing = []
            for a in assignments:
                sub = a.get("submission", {})
                state = sub.get("workflow_state", "unsubmitted")
                if state == "unsubmitted" and a.get("due_at"):
                    pts = a.get("points_possible", 0)
                    missing.append((a["name"], pts))

            if missing:
                found_any = True
                lines.append(f"**{cname}** ({len(missing)} missing):")
                for name, pts in missing:
                    lines.append(f"  • {name} — {pts} pts")
        except Exception:
            continue

    if not found_any:
        return "🎉 No missing assignments found across all courses!"

    return "\n".join(lines)
