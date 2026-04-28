import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from mcp.server.fastmcp import FastMCP
from tools.assignments import (
    get_course_list,
    get_assignments,
    get_upcoming_deadlines,
    get_assignment_details,
    get_submission_status,
)
from tools.grades import (
    get_course_grades,
    get_grade_breakdown,
    get_missing_assignments,
)
from tools.announcements import (
    get_announcements,
    get_course_modules,
    get_module_items,
)
from tools.calendar import (
    get_calendar_events,
    get_weekly_schedule,
    get_upcoming_events,
)

mcp = FastMCP("Canvas LMS Assistant")

# ── Assignments & Courses ─────────────────────────────────────────────────────

@mcp.tool()
def canvas_get_course_list() -> str:
    """List all active enrolled courses with their IDs."""
    return get_course_list()


@mcp.tool()
def canvas_get_assignments(course_id: int = None) -> str:
    """
    Get all assignments, optionally filtered by course.
    Leave course_id empty to get assignments from all courses.
    """
    return get_assignments(course_id)


@mcp.tool()
def canvas_get_upcoming_deadlines(days: int = 7) -> str:
    """
    Get assignments due within the next N days (default 7).
    Color-coded by urgency: red (≤1 day), yellow (≤3 days), green (>3 days).
    """
    return get_upcoming_deadlines(days)


@mcp.tool()
def canvas_get_assignment_details(course_id: int, assignment_id: int) -> str:
    """Get full details of a specific assignment including description and submission type."""
    return get_assignment_details(course_id, assignment_id)


@mcp.tool()
def canvas_get_submission_status(course_id: int = None) -> str:
    """
    Check submission status (submitted vs missing) for all assignments.
    Leave course_id empty to check all courses.
    """
    return get_submission_status(course_id)


# ── Grades ────────────────────────────────────────────────────────────────────

@mcp.tool()
def canvas_get_course_grades() -> str:
    """Get current grades with visual progress bars for all active courses."""
    return get_course_grades()


@mcp.tool()
def canvas_get_grade_breakdown(course_id: int) -> str:
    """Get assignment-level grade breakdown for a specific course with running total."""
    return get_grade_breakdown(course_id)


@mcp.tool()
def canvas_get_missing_assignments() -> str:
    """List all missing or unsubmitted assignments that have a due date."""
    return get_missing_assignments()


# ── Announcements & Modules ───────────────────────────────────────────────────

@mcp.tool()
def canvas_get_announcements(course_id: int = None, limit: int = 5) -> str:
    """
    Get recent announcements. Leave course_id empty for all courses.
    Adjust limit to control how many announcements to return.
    """
    return get_announcements(course_id, limit)


@mcp.tool()
def canvas_get_course_modules(course_id: int) -> str:
    """Get all modules for a course, showing locked/unlocked/completed status."""
    return get_course_modules(course_id)


@mcp.tool()
def canvas_get_module_items(course_id: int, module_id: int) -> str:
    """Get all items within a specific module with completion checkboxes."""
    return get_module_items(course_id, module_id)


# ── Calendar ──────────────────────────────────────────────────────────────────

@mcp.tool()
def canvas_get_calendar_events(days: int = 14) -> str:
    """Get all calendar events and assignment deadlines for the next N days."""
    return get_calendar_events(days)


@mcp.tool()
def canvas_get_weekly_schedule() -> str:
    """Get a structured week-at-a-glance view of all assignments due this week."""
    return get_weekly_schedule()


@mcp.tool()
def canvas_get_upcoming_events(limit: int = 10) -> str:
    """Get the next N upcoming events and deadlines across all courses (looks 30 days ahead)."""
    return get_upcoming_events(limit)


if __name__ == "__main__":
    mcp.run()
