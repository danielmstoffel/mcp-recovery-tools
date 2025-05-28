# 🚨 EMERGENCY RECOVERY GUIDE

**Date**: May 28, 2025  
**Issue**: Complete shell execution failure in Claude Desktop / Jules environment

## Current Situation

- **Problem**: All shell commands timing out (even `echo`, `pwd`, `ls`)
- **Impact**: Cannot perform any file operations, git commands, or development tasks
- **Severity**: CRITICAL - Complete development blockage

## Immediate Actions

### 1. Check MCP Server Status

1. Open Claude Desktop
2. Go to Settings → Developer
3. Look for warning triangles (⚠️) next to MCP servers
4. Screenshot any errors

### 2. Quick Fixes to Try

```bash
# Run these OUTSIDE Claude Desktop (in regular terminal)

# Option A: Kill stuck processes
pkill -f "mcp.*server"
pkill -f "claude.*node"

# Option B: Clear MCP locks (macOS)
rm -rf ~/Library/Application\ Support/Claude/locks/*

# Option C: Reset configuration
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json ~/Desktop/backup_config.json
echo '{"mcpServers":{}}' > ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### 3. Restart Sequence

1. Quit Claude Desktop completely (Cmd+Q / Alt+F4)
2. Wait 10 seconds
3. Start Claude Desktop
4. Test with: `echo "test"`

## Alternative Development Methods

### Method 1: GitHub-Based Development

While shell is broken, use GitHub API directly:

1. All code is being created in: `https://github.com/danielmstoffel/mcp-recovery-tools`
2. Clone when environment recovers: `git clone https://github.com/danielmstoffel/mcp-recovery-tools.git`

### Method 2: External IDE

Use VS Code or another IDE:

1. Open project in external editor
2. Run MCP servers manually
3. Use Claude for guidance only

## Root Cause Analysis

Possible causes:

1. **MCP Executor Crash**: The service handling commands died
2. **Resource Exhaustion**: Hit memory/CPU limits
3. **Permission Issues**: Security policy blocking execution
4. **Zombie Processes**: Too many dead processes

## Files Created for Recovery

1. **compression_mcp_client.py**: Ready-to-use compression client
2. **recovery_script.sh**: Diagnostic and recovery tool
3. **mcp_diagnostic_tool.py**: Python-based diagnostics
4. **minimal_mcp_config.json**: Bare minimum configuration

## When Environment Returns

```bash
# 1. Clone recovery tools
git clone https://github.com/danielmstoffel/mcp-recovery-tools.git
cd mcp-recovery-tools

# 2. Run diagnostics
bash recovery_script.sh

# 3. Copy compression client to your project
cp compression_mcp_client.py ~/three-layer-memory/integrations/

# 4. Test the integration
cd ~/three-layer-memory
python3 -c "from integrations.compression_mcp_client import CompressionMCPClient; print('Import successful!')"
```

## Contact & Support

- **GitHub Repo**: https://github.com/danielmstoffel/mcp-recovery-tools
- **Issue Created**: Check repo issues for updates
- **Alternative**: Use GitHub Codespaces if local environment remains broken

## Prevention for Future

1. **Regular Backups**: Export MCP configs daily
2. **Resource Monitoring**: Watch memory/CPU usage
3. **Minimal Configs**: Start with fewer MCP servers
4. **External Tools**: Keep backup development method ready

---

**Remember**: This is temporary. Once shell access returns, all development can resume normally.
