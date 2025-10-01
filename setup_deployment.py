#!/usr/bin/env python3
"""
Setup script for ACE Sharper 5D deployment
Installs required dependencies and prepares for deployment
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing deployment dependencies...")

    packages = [
        'ftplib',  # Built-in, no install needed
        'sshpass',  # Will be installed via pip
    ]

    try:
        # Install sshpass for SSH automation
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sshpass'])
        print("✅ sshpass installed successfully")

        # Install requests for testing
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
        print("✅ requests installed successfully")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    print("\n📋 Checking required files...")

    required_files = [
        'axiomhive_ace_flask.py',
        'passenger_wsgi_ace.py',
        'requirements.txt',
        'python/agents/causal_agent.py',
        'src/orchestrator.py'
    ]

    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")

    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} files:")
        for file in missing_files:
            print(f"   - {file}")
        return False

    print("✅ All required files present")
    return True

def create_deployment_checklist():
    """Create deployment checklist"""
    checklist = """
🚀 ACE Sharper 5D - GoDaddy Deployment Checklist
=================================================

✅ PRE-DEPLOYMENT (Complete these first)
   [ ] 1. Install dependencies: python setup_deployment.py
   [ ] 2. Enable SSH in cPanel (Security > SSH Access > Manage > On)
   [ ] 3. Verify FTP credentials work
   [ ] 4. Backup any existing site files

📋 ONE-TIME CPANEL SETUP (5 minutes)
   [ ] 1. Log into GoDaddy cPanel
   [ ] 2. Go to: Security > SSH Access > Manage
   [ ] 3. Toggle SSH Access: ON (green)
   [ ] 4. Note your SSH username (usually same as cPanel)
   [ ] 5. Test SSH connection: ssh username@server

🚀 AUTOMATED DEPLOYMENT (2 minutes)
   [ ] 1. Run: python deploy.py
   [ ] 2. Enter FTP credentials when prompted
   [ ] 3. Enter SSH password when prompted
   [ ] 4. Wait for completion message

🧪 POST-DEPLOYMENT TESTING
   [ ] 1. Visit: https://axiomhive.co/health
   [ ] 2. Test ACE: POST to https://axiomhive.co/ace-4d
   [ ] 3. Check: https://axiomhive.co/ (home page)

📊 EXPECTED RESULTS
   - Health endpoint: 200 OK
   - ACE endpoint: JSON response with coherence > 0.95
   - Response time: < 1 second
   - Memory usage: < 512MB

🔧 TROUBLESHOOTING
   - SSH timeout: Wait longer or check SSH access
   - FTP errors: Verify credentials and host
   - 500 errors: Check cPanel error logs
   - Module errors: Verify Python version (3.12+)

Deployment Date: 2025-09-20
Version: Sovereign Core Cycle 21
System: ACE Sharper 5D
"""

    with open('ACE_DEPLOYMENT_CHECKLIST.txt', 'w') as f:
        f.write(checklist)

    print("📝 Created deployment checklist: ACE_DEPLOYMENT_CHECKLIST.txt")

def main():
    """Main setup function"""
    print("🚀 ACE Sharper 5D - Deployment Setup")
    print("=" * 45)
    print("Sovereign Core Cycle 21 - t=2025-09-20")

    # Step 1: Install dependencies
    if not install_dependencies():
        print("❌ Setup failed - cannot install dependencies")
        return False

    # Step 2: Check files
    if not check_files():
        print("❌ Setup failed - missing required files")
        return False

    # Step 3: Create checklist
    create_deployment_checklist()

    print("\n" + "=" * 45)
    print("✅ Setup Complete!")
    print("📋 Next steps:")
    print("   1. Enable SSH in GoDaddy cPanel")
    print("   2. Run: python deploy.py")
    print("   3. Follow the prompts")
    print("   4. Your ACE system will be live!")
    print("=" * 45)

    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 Ready for deployment!")
        else:
            print("\n❌ Setup failed - please fix issues and try again")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
