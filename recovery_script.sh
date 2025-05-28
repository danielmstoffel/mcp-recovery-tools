#!/bin/bash
# MCP Environment Recovery Script
# Created: 2025-05-28
# Purpose: Diagnose and recover from MCP execution failures

echo "=== MCP Environment Recovery Tool ==="
echo "Time: $(date)"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Basic System Check
echo "[1/6] Basic System Check"
echo "------------------------"
echo "Hostname: $(hostname 2>/dev/null || echo 'FAILED')"
echo "Current User: $(whoami 2>/dev/null || echo 'FAILED')"
echo "Current Directory: $(pwd 2>/dev/null || echo 'FAILED')"
echo "Shell: $SHELL"
echo ""

# 2. Process Check
echo "[2/6] Process Check"
echo "-------------------"
echo "Checking for MCP-related processes..."
ps aux | grep -E "(mcp|claude|node)" | grep -v grep || echo "No MCP processes found"
echo ""

# 3. Resource Check
echo "[3/6] Resource Check"
echo "--------------------"
echo "Memory Usage:"
free -m 2>/dev/null || echo "Cannot check memory"
echo ""
echo "Disk Usage:"
df -h . 2>/dev/null || echo "Cannot check disk"
echo ""

# 4. MCP Configuration Check
echo "[4/6] MCP Configuration Check"
echo "-----------------------------"
CONFIG_PATHS=(
    "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    "$HOME/.config/claude/claude_desktop_config.json"
    "$HOME/AppData/Roaming/Claude/claude_desktop_config.json"
)

for path in "${CONFIG_PATHS[@]}"; do
    if [ -f "$path" ]; then
        echo -e "${GREEN}Found config at: $path${NC}"
        echo "Config content (first 500 chars):"
        head -c 500 "$path" 2>/dev/null
        echo ""
        break
    fi
done

# 5. Kill Stuck Processes
echo "[5/6] Cleanup Actions"
echo "---------------------"
echo "Attempting to clean up stuck processes..."

# Kill any hanging node processes related to MCP
STUCK_PIDS=$(ps aux | grep -E "(mcp.*server|claude.*node)" | grep -v grep | awk '{print $2}')
if [ ! -z "$STUCK_PIDS" ]; then
    echo -e "${YELLOW}Found stuck processes: $STUCK_PIDS${NC}"
    echo "Run 'kill -9 $STUCK_PIDS' to force terminate"
else
    echo -e "${GREEN}No stuck processes found${NC}"
fi

# 6. Recovery Recommendations
echo ""
echo "[6/6] Recovery Recommendations"
echo "------------------------------"
echo "1. Restart Claude Desktop completely"
echo "2. Check if antivirus is blocking execution"
echo "3. Try minimal MCP config:"
echo '   {"mcpServers":{}}'
echo "4. Check system logs:"
echo "   - macOS: Console.app or 'log show --last 5m | grep -i claude'"
echo "   - Linux: 'journalctl -f' or 'dmesg | tail'"
echo "   - Windows: Event Viewer"
echo ""
echo "5. If nothing works, reset Claude Desktop:"
echo "   - Backup your config"
echo "   - Delete config file"
echo "   - Restart Claude Desktop"
echo ""

# Create diagnostic report
REPORT_FILE="mcp_diagnostic_$(date +%Y%m%d_%H%M%S).txt"
echo "Creating diagnostic report: $REPORT_FILE"
{
    echo "MCP Diagnostic Report - $(date)"
    echo "================================"
    echo ""
    echo "System Info:"
    uname -a
    echo ""
    echo "Environment Variables:"
    env | grep -E "(PATH|NODE|CLAUDE|MCP)" | sort
    echo ""
    echo "Recent System Errors:"
    dmesg | tail -20 2>/dev/null || echo "Cannot access system log"
} > "$REPORT_FILE" 2>&1

echo -e "${GREEN}Diagnostic report saved to: $REPORT_FILE${NC}"
echo ""
echo "=== Recovery Script Complete ==="
