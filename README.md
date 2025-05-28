# MCP Recovery Tools

Emergency recovery tools for Jules/Claude Desktop environment failures.

Created: 2025-05-28

## Quick Start

If you're experiencing shell execution timeouts in Claude Desktop:

1. Run the recovery script (outside Claude):
   ```bash
   bash recovery_script.sh
   ```

2. Try the Python diagnostic tool:
   ```python
   python3 mcp_diagnostic_tool.py
   ```

3. Check the EMERGENCY_RECOVERY.md for detailed instructions.

## Contents

- **compression_mcp_client.py** - Compression client for three-layer memory
- **recovery_script.sh** - Shell-based recovery tool
- **mcp_diagnostic_tool.py** - Python diagnostic tool
- **EMERGENCY_RECOVERY.md** - Detailed recovery guide
- **minimal_mcp_config.json** - Minimal working configuration
