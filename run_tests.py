#!/usr/bin/env python
"""
Test runner script for the MaxmAuto test framework.
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from config.config import Config


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="MaxmAuto Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                      # Run all tests
  python run_tests.py --file setup         # Clean install + permission
  python run_tests.py --file login         # Run login tests
  python run_tests.py --file logout
  python run_tests.py --html
  python run_tests.py --env PROD
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        choices=['setup', 'login', 'logout', 'all'],
        default='all',
        help='Specify which test file to run'
    )
    
    parser.add_argument('--marker', '-m', type=str, help='Run tests with specific marker')
    parser.add_argument('--html', action='store_true', help='Generate HTML report')
    parser.add_argument('--env', '-e', choices=['STG', 'PROD'], default='STG')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--collect-only', action='store_true')

    return parser.parse_args()


def setup_environment(args):
    os.environ['MAXM_ENV'] = args.env
    Config.create_directories()
    print(f"🔧 Environment: {args.env}")


def build_pytest_command(args):
    cmd = [sys.executable, '-m', 'pytest']
    
    if args.file == 'all':
        cmd.append('tests/')
    elif args.file == 'setup':
        cmd.append('tests/test_setup.py')
    elif args.file == 'login':
        cmd.append('tests/test_login.py')
    elif args.file == 'logout':
        cmd.append('tests/test_logout.py')
    
    if args.marker:
        cmd.extend(['-m', args.marker])

    cmd.append('-s')
    
    if args.verbose:
        cmd.append('-v')
    else:
        cmd.append('-v')
    
    if args.html:
        html_path = Config.REPORTS_DIR / 'report.html'
        cmd.extend(['--html', str(html_path), '--self-contained-html'])
    
    if args.collect_only:
        cmd.append('--collect-only')
    
    cmd.extend(['--tb=short', '--maxfail=3'])
    return cmd


def run_tests(args):
    print("\n" + "=" * 70)
    print("🚀 MaxmAuto Test Runner")
    print("=" * 70)
    
    setup_environment(args)
    
    cmd = build_pytest_command(args)
    print(f"📋 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=Config.PROJECT_ROOT, env=os.environ.copy())
        
        print("\n" + "=" * 70)
        if result.returncode == 0:
            print("✅ Success!")
        else:
            print(f"❌ Failed with code: {result.returncode}")
        print("=" * 70)
        
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest not found. Run: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def main():
    args = parse_arguments()
    sys.exit(run_tests(args))


if __name__ == '__main__':
    main()