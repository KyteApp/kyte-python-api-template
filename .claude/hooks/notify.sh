#!/usr/bin/env bash
# Simple notification script for Claude Code hooks.
# Works on macOS (osascript) and Linux (notify-send).

MESSAGE="${1:-Task completed}"

if command -v osascript &>/dev/null; then
    osascript -e "display notification \"$MESSAGE\" with title \"Claude Code\""
elif command -v notify-send &>/dev/null; then
    notify-send "Claude Code" "$MESSAGE"
else
    echo "[notify] $MESSAGE"
fi
