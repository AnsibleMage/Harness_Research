# Anthropic Claude Code Official Documentation — CLAUDE.md Guide

## Official Sources (영문 원문 기준, 2026년 4월 최신)

- How Claude remembers your project: https://code.claude.com/docs/en/memory
- Best Practices for Claude Code: https://code.claude.com/docs/en/best-practices
- Explore the .claude directory: https://code.claude.com/docs/en/claude-directory
- Claude Code overview: https://code.claude.com/docs/en/overview

## What is CLAUDE.md?

CLAUDE.md is a markdown file that provides **persistent instructions** to Claude Code.  
Claude automatically reads the CLAUDE.md file at the start of every session and loads it into its context.  
It is the primary way for users to give Claude long-term, project-specific rules, coding standards, architecture decisions, workflows, and constraints that cannot be inferred from the codebase alone.

## How CLAUDE.md is Loaded (Scope and Priority)

Claude Code searches for CLAUDE.md files starting from the current working directory and moving upward. More specific locations take precedence.

**Loading Order (Official):**

- Project level: `./CLAUDE.md` or `./.claude/CLAUDE.md` (recommended for git commit and team sharing)
- User level: `~/.claude/CLAUDE.md` (applies to all projects for that user)
- Organization/Managed policy level: system-wide paths (e.g., /Library/Application Support/ClaudeCode/CLAUDE.md on macOS)
- Subdirectory level: CLAUDE.md files in subfolders are loaded when working inside that directory

In monorepos, `claudeMdExcludes` setting can be used to exclude irrelevant CLAUDE.md files.

## CLAUDE.md vs Auto Memory (Official Comparison Table)

| Item       | CLAUDE.md                      | Auto Memory                             |
| ---------- | ------------------------------ | --------------------------------------- |
| Written by | User (You)                     | Claude (automatically)                  |
| Content    | Instructions and rules         | Learnings and patterns                  |
| Scope      | Project / User / Organization  | Per working tree                        |
| Loaded     | Every session (full content)   | Every session (first 200 lines or 25KB) |
| Purpose    | Persistent context you control | Automatic accumulation of insights      |

## How to Create CLAUDE.md

1. Use the built-in command: `/init`  
   Claude analyzes the current codebase (build systems, test frameworks, code patterns, etc.) and automatically generates a starter CLAUDE.md file.

2. Manual creation: Create a file named `CLAUDE.md` in the project root or inside `.claude/` directory.

## Official Best Practices for Writing Effective CLAUDE.md

- **Length**: Keep under 200 lines (ideally much shorter) to minimize context usage.
- **Structure**: Use clear Markdown headers (#, ##) and bullet points for easy scanning by Claude.
- **Specificity**: Write concrete, verifiable instructions.  
  Good: "Use ES modules (import/export) syntax, not CommonJS (require)"  
  Bad: "Write clean code"
- **Conciseness**: Only include information Claude cannot infer from the code itself.
- **Focus**: Include bash commands, code style, naming conventions, testing workflows, architecture decisions, common gotchas, repository etiquette.
- **Avoid**: General advice, long tutorials, frequently changing information, or content already obvious from the codebase.

**Official Example from Best Practices:**

```markdown

# Code style

- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (e.g. import { foo } from 'bar')

# Workflow

- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance





Advanced Features
-----------------

* **Imports**: Use @README.md or @~/.claude/my-rules.md syntax to import other markdown files (limited depth).
* **.claude/rules/** directory: Organize rules by topic or file-type for better scoping.
* **Integration**: Works together with Skills, Hooks, Sub-agents, and Auto Memory features.

Key Official Emphasis
---------------------

* CLAUDE.md is the most powerful tool for giving Claude persistent context across sessions.
* Well-written CLAUDE.md significantly reduces repeated explanations and improves consistency.
* Review and clean CLAUDE.md periodically to remove contradictions or outdated rules.
* For team use, commit ./CLAUDE.md to git so all team members share the same instructions.
* For organization-wide rules, use managed policy CLAUDE.md at the system level.

This document summarizes all core official guidance on CLAUDE.md from Anthropic’s Claude Code documentation as of April 2026. No additional community or third-party content is included.
