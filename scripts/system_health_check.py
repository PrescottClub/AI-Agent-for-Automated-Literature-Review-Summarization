#!/usr/bin/env python3
"""
Tsearch System Health Check Tool
Check frontend-backend connectivity, environment configuration, API connections, etc.
"""

import os
import sys
import time
import json
import asyncio
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root directory to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(text: str, color: str = Colors.ENDC):
    """Print colored text, handle encoding issues"""
    try:
        # Replace problematic characters for GBK encoding
        safe_text = text.encode('gbk', errors='replace').decode('gbk')
        print(f"{color}{safe_text}{Colors.ENDC}")
    except (UnicodeEncodeError, TypeError):
        # If still fails, remove non-ASCII characters
        safe_text = ''.join(char if ord(char) < 128 else '?' for char in text)
        print(f"{color}{safe_text}{Colors.ENDC}")
    except:
        # Final fallback, remove colors
        print(text)

def print_section(title: str):
    """Print section title"""
    print_colored(f"\n{'='*60}", Colors.HEADER)
    print_colored(f"[*] {title}", Colors.HEADER)
    print_colored(f"{'='*60}", Colors.HEADER)

class SystemHealthChecker:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:5173"
        self.results = {}
        
    async def run_all_checks(self):
        """Run all health checks"""
        print_colored('[START] Tsearch System Health Check Started', Colors.HEADER)
        print_colored(f'[INFO] Project Root Directory: {PROJECT_ROOT}', Colors.OKCYAN)
        
        checks = [
            ("Environment Configuration Check", self.check_environment),
            ("Python Dependencies Check", self.check_python_dependencies),
            ("Frontend Dependencies Check", self.check_frontend_dependencies),
            ("Backend Service Check", self.check_backend_service),
            ("Frontend Service Check", self.check_frontend_service),
            ("API Connectivity Test", self.check_api_connectivity),
            ("Database Connection Check", self.check_database_connectivity),
            ("AI Model Configuration Check", self.check_ai_configuration),
        ]
        
        for check_name, check_func in checks:
            print_section(check_name)
            try:
                result = await check_func()
                self.results[check_name] = result
                if result.get('status') == 'success':
                    print_colored(f'[PASS] {check_name} Passed', Colors.OKGREEN)
                else:
                    print_colored(f'[FAIL] {check_name} Failed', Colors.FAIL)
                    if result.get('error'):
                        print_colored(f"   Error: {result['error']}", Colors.WARNING)
            except Exception as e:
                # Clean the error message to avoid encoding issues
                error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
                print_colored(f'[ERROR] {check_name} Exception: {error_msg}', Colors.FAIL)
                self.results[check_name] = {'status': 'error', 'error': error_msg}
        
        await self.generate_report()
    
    async def check_environment(self) -> Dict[str, Any]:
        """Check environment configuration"""
        try:
            # Check Python version
            python_version = sys.version_info
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
                return {'status': 'error', 'error': f'Python version too low: {python_version}'}
            
            # Check environment variable files
            env_files = [
                PROJECT_ROOT / ".env",
                PROJECT_ROOT / "config" / ".env"
            ]
            
            env_file_exists = any(f.exists() for f in env_files)
            
            # Check critical environment variables
            required_vars = ['DEEPSEEK_API_KEY', 'LLM_PROVIDER']
            missing_vars = []
            
            for var in required_vars:
                if not os.getenv(var):
                    missing_vars.append(var)
            
            return {
                'status': 'success' if env_file_exists and not missing_vars else 'warning',
                'python_version': f"{python_version.major}.{python_version.minor}.{python_version.micro}",
                'env_file_exists': env_file_exists,
                'missing_vars': missing_vars,
                'project_root': str(PROJECT_ROOT)
            }
        except Exception as e:
            # Clean the error message to avoid encoding issues
            error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
            return {'status': 'error', 'error': error_msg}
    
    async def check_python_dependencies(self) -> Dict[str, Any]:
        """Check Python dependencies"""
        try:
            pyproject_file = PROJECT_ROOT / "pyproject.toml"
            if not pyproject_file.exists():
                return {'status': 'error', 'error': 'pyproject.toml does not exist'}
            
            # Try importing critical modules
            critical_modules = [
                'fastapi', 'uvicorn', 'pydantic', 'loguru', 
                'chromadb', 'sentence_transformers', 'spacy'
            ]
            
            missing_modules = []
            for module in critical_modules:
                try:
                    __import__(module)
                except ImportError:
                    missing_modules.append(module)
            
            return {
                'status': 'success' if not missing_modules else 'error',
                'missing_modules': missing_modules,
                'requirements_exists': True
            }
        except Exception as e:
            # Clean the error message to avoid encoding issues
            error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
            return {'status': 'error', 'error': error_msg}
    
    async def check_frontend_dependencies(self) -> Dict[str, Any]:
        """Check frontend dependencies"""
        try:
            frontend_dir = PROJECT_ROOT / "frontend" / "literature-review-frontend"
            package_json = frontend_dir / "package.json"
            node_modules = frontend_dir / "node_modules"
            
            if not package_json.exists():
                return {'status': 'error', 'error': 'package.json does not exist'}
            
            if not node_modules.exists():
                return {'status': 'error', 'error': 'node_modules does not exist, please run npm install'}
            
            # Check critical dependencies
            with open(package_json, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            dependencies = package_data.get('dependencies', {})
            critical_deps = ['vue', 'axios', 'element-plus', 'tailwindcss']
            missing_deps = [dep for dep in critical_deps if dep not in dependencies]
            
            return {
                'status': 'success' if not missing_deps else 'warning',
                'missing_deps': missing_deps,
                'node_modules_exists': True,
                'package_json_exists': True
            }
        except Exception as e:
            # Clean the error message to avoid encoding issues
            error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
            return {'status': 'error', 'error': error_msg}
    
    async def check_backend_service(self) -> Dict[str, Any]:
        """Check backend service"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                return {
                    'status': 'success',
                    'url': self.backend_url,
                    'health_data': health_data
                }
            else:
                return {
                    'status': 'error',
                    'error': f'Backend service response abnormal: {response.status_code}'
                }
        except requests.exceptions.ConnectionError as e:
            return {
                'status': 'error',
                'error': 'Cannot connect to backend service, please ensure backend service is started'
            }
        except Exception as e:
            # Clean the error message to avoid encoding issues
            error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
            return {'status': 'error', 'error': error_msg}
    
    async def check_frontend_service(self) -> Dict[str, Any]:
        """Check frontend service"""
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'url': self.frontend_url
                }
            else:
                return {
                    'status': 'error',
                    'error': f'Frontend service response abnormal: {response.status_code}'
                }
        except requests.exceptions.ConnectionError as e:
            return {
                'status': 'error',
                'error': 'Cannot connect to frontend service, please ensure frontend service is started'
            }
        except Exception as e:
            # Clean the error message to avoid encoding issues
            error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
            return {'status': 'error', 'error': error_msg}
    
    async def check_api_connectivity(self) -> Dict[str, Any]:
        """Check API connectivity"""
        try:
            # Test health check endpoint
            health_response = requests.get(f"{self.backend_url}/health", timeout=5)
            
            # Test status endpoint
            status_response = requests.get(f"{self.backend_url}/api/status", timeout=5)
            
            # Test search endpoint (simulate request)
            search_data = {
                "rawQuery": "test query",
                "maxPapers": 1,
                "sources": ["arxiv"]
            }
            search_response = requests.post(
                f"{self.backend_url}/api/search",
                json=search_data,
                timeout=10
            )
            
            return {
                'status': 'success',
                'health_status': health_response.status_code,
                'status_endpoint': status_response.status_code,
                'search_endpoint': search_response.status_code
            }
        except Exception as e:
            # Clean the error message to avoid encoding issues
            error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
            return {'status': 'error', 'error': error_msg}
    
    async def check_database_connectivity(self) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            # Check ChromaDB data directory
            chroma_dir = PROJECT_ROOT / "data" / "chroma_db"
            
            return {
                'status': 'success' if chroma_dir.exists() else 'warning',
                'chroma_dir_exists': chroma_dir.exists(),
                'chroma_path': str(chroma_dir)
            }
        except Exception as e:
            # Clean the error message to avoid encoding issues
            error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
            return {'status': 'error', 'error': error_msg}
    
    async def check_ai_configuration(self) -> Dict[str, Any]:
        """Check AI configuration"""
        try:
            # Check environment variables
            llm_provider = os.getenv('LLM_PROVIDER', 'deepseek')
            api_key = os.getenv('DEEPSEEK_API_KEY')
            model = os.getenv('DEEPSEEK_MODEL', 'deepseek-reasoner')
            
            if not api_key:
                return {'status': 'error', 'error': 'DEEPSEEK_API_KEY not set'}
            
            return {
                'status': 'success',
                'llm_provider': llm_provider,
                'model': model,
                'api_key_set': bool(api_key)
            }
        except Exception as e:
            # Clean the error message to avoid encoding issues
            error_msg = str(e).encode('ascii', errors='replace').decode('ascii')
            return {'status': 'error', 'error': error_msg}
    
    async def generate_report(self):
        """Generate check report"""
        print_section("System Health Check Report")
        
        success_count = sum(1 for r in self.results.values() if r.get('status') == 'success')
        total_count = len(self.results)
        
        print_colored(f'[SUMMARY] Overall Status: {success_count}/{total_count} checks passed', Colors.HEADER)
        
        if success_count == total_count:
            print_colored('[SUCCESS] System status is good, all checks passed!', Colors.OKGREEN)
        elif success_count >= total_count * 0.7:
            print_colored('[WARNING] System is basically normal, but some issues need attention', Colors.WARNING)
        else:
            print_colored('[CRITICAL] System has serious problems that need to be fixed', Colors.FAIL)
        
        # Detailed report
        print_colored('\n[DETAILS] Detailed Check Results:', Colors.OKCYAN)
        for check_name, result in self.results.items():
            status_icon = '[OK]' if result.get('status') == 'success' else '[FAIL]'
            print_colored(f"  {status_icon} {check_name}", Colors.ENDC)
            
            if result.get('error'):
                print_colored(f"     Error: {result['error']}", Colors.WARNING)
        
        # Suggestions
        print_colored('\n[SUGGESTIONS] Fix Suggestions:', Colors.OKCYAN)
        for check_name, result in self.results.items():
            if result.get('status') != 'success':
                if 'backend' in check_name.lower():
                    print_colored('  - Start backend service: python scripts/start_backend_only.py', Colors.WARNING)
                elif 'frontend' in check_name.lower():
                    print_colored('  - Start frontend service: cd frontend/literature-review-frontend && npm run dev', Colors.WARNING)
                elif 'dependencies' in check_name.lower():
                    print_colored('  - Install dependencies: pip install -e .', Colors.WARNING)
                elif 'environment' in check_name.lower():
                    print_colored('  - Configure environment variables: create .env file and set necessary API keys', Colors.WARNING)

async def main():
    """Main function"""
    checker = SystemHealthChecker()
    await checker.run_all_checks()

if __name__ == "__main__":
    asyncio.run(main())
