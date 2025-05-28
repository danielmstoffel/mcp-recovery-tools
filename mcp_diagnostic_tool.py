#!/usr/bin/env python3
"""
MCP Diagnostic Tool
Purpose: Diagnose MCP execution issues without shell commands
"""

import os
import sys
import json
import psutil
import platform
from datetime import datetime
from pathlib import Path


class MCPDiagnostic:
    def __init__(self):
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'platform': platform.system(),
            'python_version': sys.version,
            'checks': {}
        }
    
    def check_system_resources(self):
        """Check CPU and memory usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            self.report['checks']['resources'] = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': disk.percent,
                'disk_free_gb': disk.free / (1024**3)
            }
            
            # Check if resources are critically low
            if memory.percent > 90:
                print("⚠️  WARNING: Memory usage is critically high!")
            if disk.percent > 95:
                print("⚠️  WARNING: Disk space is critically low!")
                
        except Exception as e:
            self.report['checks']['resources'] = {'error': str(e)}
    
    def check_mcp_processes(self):
        """Find MCP-related processes"""
        try:
            mcp_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if any(keyword in cmdline.lower() for keyword in ['mcp', 'claude', 'node']):
                        mcp_processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'status': proc.info['status'],
                            'cmdline': cmdline[:200]  # Truncate long commands
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            self.report['checks']['mcp_processes'] = mcp_processes
            
            # Check for zombie processes
            zombies = [p for p in mcp_processes if p['status'] == 'zombie']
            if zombies:
                print(f"⚠️  WARNING: Found {len(zombies)} zombie processes!")
                
        except Exception as e:
            self.report['checks']['mcp_processes'] = {'error': str(e)}
    
    def check_mcp_config(self):
        """Check MCP configuration files"""
        config_paths = [
            Path.home() / "Library/Application Support/Claude/claude_desktop_config.json",
            Path.home() / ".config/claude/claude_desktop_config.json",
            Path.home() / "AppData/Roaming/Claude/claude_desktop_config.json"
        ]
        
        for path in config_paths:
            if path.exists():
                try:
                    with open(path, 'r') as f:
                        config = json.load(f)
                    
                    self.report['checks']['mcp_config'] = {
                        'path': str(path),
                        'exists': True,
                        'server_count': len(config.get('mcpServers', {})),
                        'servers': list(config.get('mcpServers', {}).keys())
                    }
                    
                    print(f"✅ Found MCP config at: {path}")
                    print(f"   Configured servers: {', '.join(config.get('mcpServers', {}).keys())}")
                    break
                    
                except Exception as e:
                    self.report['checks']['mcp_config'] = {
                        'path': str(path),
                        'exists': True,
                        'error': str(e)
                    }
        else:
            self.report['checks']['mcp_config'] = {'exists': False}
            print("❌ No MCP configuration file found!")
    
    def check_permissions(self):
        """Check file system permissions"""
        try:
            test_dir = Path.home() / ".mcp_test"
            test_file = test_dir / "test.txt"
            
            # Try to create directory and file
            test_dir.mkdir(exist_ok=True)
            test_file.write_text("test")
            content = test_file.read_text()
            
            # Clean up
            test_file.unlink()
            test_dir.rmdir()
            
            self.report['checks']['permissions'] = {
                'can_create_dirs': True,
                'can_write_files': True,
                'can_read_files': True
            }
            print("✅ File system permissions OK")
            
        except Exception as e:
            self.report['checks']['permissions'] = {'error': str(e)}
            print("❌ File system permission issues detected!")
    
    def generate_recovery_suggestions(self):
        """Generate specific recovery suggestions based on findings"""
        suggestions = []
        
        # Check resources
        resources = self.report['checks'].get('resources', {})
        if resources.get('memory_percent', 0) > 90:
            suggestions.append("Close other applications to free memory")
        if resources.get('disk_percent', 0) > 95:
            suggestions.append("Free up disk space (at least 1GB recommended)")
        
        # Check processes
        processes = self.report['checks'].get('mcp_processes', [])
        if any(p.get('status') == 'zombie' for p in processes):
            suggestions.append("Kill zombie processes: pkill -f 'mcp.*server'")
        
        # Check config
        config = self.report['checks'].get('mcp_config', {})
        if not config.get('exists'):
            suggestions.append("Create minimal MCP config file")
        elif config.get('server_count', 0) > 5:
            suggestions.append("Reduce number of MCP servers (current: {})".format(
                config.get('server_count')))
        
        self.report['recovery_suggestions'] = suggestions
        return suggestions
    
    def run_diagnostics(self):
        """Run all diagnostic checks"""
        print("=== MCP Diagnostic Tool ===")
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nRunning diagnostics...\n")
        
        # Run all checks
        self.check_system_resources()
        self.check_mcp_processes()
        self.check_mcp_config()
        self.check_permissions()
        
        # Generate suggestions
        suggestions = self.generate_recovery_suggestions()
        
        print("\n=== Recovery Suggestions ===")
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")
        else:
            print("No specific issues detected.")
        
        # Save report
        report_file = f"mcp_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        
        print(f"\n📄 Full report saved to: {report_file}")
        
        return self.report


if __name__ == "__main__":
    diagnostic = MCPDiagnostic()
    diagnostic.run_diagnostics()
    
    # Quick fix attempt
    print("\n=== Quick Fix Commands ===")
    print("Run these in a terminal OUTSIDE Claude Desktop:")
    print("\n# Option 1: Restart Claude Desktop")
    print("killall 'Claude Desktop' 2>/dev/null; sleep 2; open -a 'Claude Desktop'")
    print("\n# Option 2: Clear MCP processes")
    print("pkill -f 'mcp.*server'; pkill -f 'node.*mcp'")
    print("\n# Option 3: Reset to minimal config")
    print("echo '{\"mcpServers\":{}}' > ~/Library/Application\\ Support/Claude/claude_desktop_config.json")
