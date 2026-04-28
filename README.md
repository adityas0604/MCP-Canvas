# 🎓 Canvas LMS MCP Server

A robust **Model Context Protocol (MCP) server** that connects Claude AI to your Canvas LMS account — letting you interact with your coursework using natural language.

> Built with Python · Canvas REST API · MCP SDK

---

## ✨ Features (14 Tools across 4 Modules)

### 📚 Assignments & Courses
| Tool | Description |
|------|-------------|
| `canvas_get_course_list` | List all active enrolled courses |
| `canvas_get_assignments` | Get all assignments (all courses or filtered) |
| `canvas_get_upcoming_deadlines` | Deadlines in the next N days, color-coded by urgency |
| `canvas_get_assignment_details` | Full details of a specific assignment |
| `canvas_get_submission_status` | Submitted vs. missing across all courses |

### 📊 Grades
| Tool | Description |
|------|-------------|
| `canvas_get_course_grades` | Current grades with visual progress bars |
| `canvas_get_grade_breakdown` | Assignment-level breakdown with running total |
| `canvas_get_missing_assignments` | All unsubmitted assignments |

### 📢 Announcements & Modules
| Tool | Description |
|------|-------------|
| `canvas_get_announcements` | Recent announcements across courses |
| `canvas_get_course_modules` | Modules with locked/completed status |
| `canvas_get_module_items` | Items in a module with completion checkboxes |

### 📅 Calendar
| Tool | Description |
|------|-------------|
| `canvas_get_calendar_events` | All events for the next N days |
| `canvas_get_weekly_schedule` | Week-at-a-glance view |
| `canvas_get_upcoming_events` | Next N events across all courses |

---


## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/adityas0604/MCP-Canvas.git
cd canvas-mcp
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

**How to get your Canvas API Token:**
1. Log into Canvas
2. Go to **Account → Settings**
3. Scroll to **Approved Integrations**
4. Click **New Access Token**
5. Copy the token into your `.env`

### 3. Configure Claude Desktop

Add this to your `claude_desktop_config.json`:

**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "canvas": {
      "command": "python",
      "args": ["/absolute/path/to/canvas-mcp/server.py"],
      "env": {
        "CANVAS_BASE_URL": "canvas_base_url"
        "CANVAS_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

### 4. Restart Claude Desktop

The Canvas tools will now appear in your Claude sidebar!

---

## 💬 Example Prompts

Once connected, try asking Claude:

- *"What assignments do I have due this week?"*
- *"What's my current GPA estimate?"*
- *"Am I missing any assignments?"*
- *"What announcements have my professors posted recently?"*
- *"Show me my grade breakdown for course 12345"*
- *"What does my week look like?"*

---

## 🔒 Privacy & Security

- **Read-only** — this server never writes, submits, or modifies your Canvas data

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **[MCP SDK](https://github.com/anthropics/mcp)** — Model Context Protocol
- **[httpx](https://www.python-httpx.org/)** — Async-ready HTTP client
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — Environment config
- **Canvas LMS REST API**

---


