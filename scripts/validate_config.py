#!/usr/bin/env python3
"""
Configuration validation script for Tsearch system.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

class Colors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_colored(text: str, color: str = Colors.ENDC):
    """Print colored text with encoding safety."""
    try:
        print(f"{color}{text}{Colors.ENDC}")
    except (UnicodeEncodeError, TypeError):
        safe_text = text.encode('utf-8', errors='replace').decode('utf-8')
        print(f"{color}{safe_text}{Colors.ENDC}")
    except:
        print(text)

def validate_config() -> Dict[str, Any]:
    """Validate configuration settings."""
    results = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'info': []
    }
    
    # Check config files
    config_file = PROJECT_ROOT / "config" / "config.env"
    template_file = PROJECT_ROOT / "config" / "config.template.env"
    
    if not config_file.exists():
        results['errors'].append("config/config.env file not found")
        results['valid'] = False
    
    if not template_file.exists():
        results['warnings'].append("config/config.template.env template not found")
    
    # Check required environment variables
    required_vars = [
        'LLM_PROVIDER',
        'DEEPSEEK_API_KEY',
        'OPENAI_API_KEY',
        'LOG_LEVEL'
    ]
    
    # Try to load from config.env
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for var in required_vars:
                if f"{var}=" not in content:
                    results['warnings'].append(f"Variable {var} not found in config.env")
                elif f"{var}=your-" in content or f"{var}=mock-" in content:
                    results['warnings'].append(f"Variable {var} appears to use placeholder value")
                else:
                    results['info'].append(f"Variable {var} is configured")
                    
        except Exception as e:
            results['errors'].append(f"Error reading config.env: {e}")
            results['valid'] = False
    
    # Check API key format
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line.startswith('DEEPSEEK_API_KEY=') and not line.endswith('here'):
                        key = line.split('=', 1)[1]
                        if key.startswith('sk-') and len(key) > 20:
                            results['info'].append("DeepSeek API key format appears valid")
                        elif 'your-' not in key:
                            results['warnings'].append("DeepSeek API key format may be invalid")
                    
                    if line.startswith('OPENAI_API_KEY=') and not line.endswith('here'):
                        key = line.split('=', 1)[1]
                        if key.startswith('sk-') and len(key) > 20:
                            results['info'].append("OpenAI API key format appears valid")
                        elif 'your-' not in key:
                            results['warnings'].append("OpenAI API key format may be invalid")
                            
        except Exception as e:
            results['errors'].append(f"Error validating API keys: {e}")
    
    # Check security settings
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not jwt_secret or jwt_secret == 'your-secret-key-change-in-production':
        results['warnings'].append("JWT_SECRET_KEY not set or using default value")
    
    return results

def main():
    """Main validation function."""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("Tsearch Configuration Validation", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    
    results = validate_config()
    
    # Print results
    if results['info']:
        print_colored("\n[INFO] Configuration Status:", Colors.OKGREEN)
        for info in results['info']:
            print_colored(f"  [OK] {info}", Colors.OKGREEN)
    
    if results['warnings']:
        print_colored("\n[WARNING] Configuration Warnings:", Colors.WARNING)
        for warning in results['warnings']:
            print_colored(f"  [WARN] {warning}", Colors.WARNING)
    
    if results['errors']:
        print_colored("\n[ERROR] Configuration Errors:", Colors.FAIL)
        for error in results['errors']:
            print_colored(f"  [ERROR] {error}", Colors.FAIL)
    
    # Final status
    print_colored("\n" + "=" * 60, Colors.HEADER)
    if results['valid']:
        print_colored("Configuration Validation: PASSED", Colors.OKGREEN)
        if results['warnings']:
            print_colored("(with warnings - please review)", Colors.WARNING)
    else:
        print_colored("Configuration Validation: FAILED", Colors.FAIL)
        print_colored("Please fix the errors above before proceeding", Colors.FAIL)
    print_colored("=" * 60, Colors.HEADER)
    
    return 0 if results['valid'] else 1

if __name__ == "__main__":
    sys.exit(main())