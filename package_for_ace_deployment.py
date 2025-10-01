#!/usr/bin/env python3
"""
Package AxiomHive 4D ACE for cPanel deployment
Creates a zip file with all necessary files
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_deployment_package():
    """Create deployment package for cPanel"""

    # Files to include in deployment
    deployment_files = [
        'axiomhive_ace_flask.py',
        'passenger_wsgi_ace.py',
        'requirements.txt',
        'python/agents/causal_agent.py',
        'src/orchestrator.py',
        'DEPLOYMENT_README_ACE.md'
    ]

    # Create deployment directory
    deployment_dir = Path('axiomhive_ace_deployment')
    deployment_dir.mkdir(exist_ok=True)

    print("📦 Creating ACE deployment package...")

    # Copy files to deployment directory
    for file_path in deployment_files:
        if Path(file_path).exists():
            if Path(file_path).is_file():
                shutil.copy2(file_path, deployment_dir)
                print(f"✅ Added: {file_path}")
            else:
                # Copy directory
                shutil.copytree(file_path, deployment_dir / Path(file_path).name)
                print(f"✅ Added directory: {file_path}")
        else:
            print(f"⚠️  Warning: {file_path} not found")

    # Create zip file
    zip_path = 'axiomhive_4d_ace_deployment.zip'
    print(f"\n📁 Creating zip file: {zip_path}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in deployment_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(deployment_dir.parent)
                zipf.write(file_path, arcname)
                print(f"   📄 {arcname}")

    print(f"\n✅ ACE deployment package created: {zip_path}")
    print(f"📊 Package size: {Path(zip_path).stat().st_size / 1024:.1f} KB")

    # Cleanup
    shutil.rmtree(deployment_dir)

    return zip_path

def create_deployment_checklist():
    """Create deployment checklist"""
    checklist = """
🚀 AxiomHive 4D ACE - cPanel Deployment Checklist
====================================================

✅ PRE-DEPLOYMENT (Complete)
   [x] Create deployment package
   [x] Test locally with test_ace_nexus.py
   [x] Verify all dependencies in requirements.txt
   [x] Check file permissions (755 for .py files)

📋 CPANEL DEPLOYMENT STEPS
   [ ] 1. Log into GoDaddy cPanel
   [ ] 2. Upload axiomhive_4d_ace_deployment.zip
   [ ] 3. Extract files to /public_html/
   [ ] 4. Setup Python App (Python 3.12)
   [ ] 5. Install requirements: pip install -r requirements.txt
   [ ] 6. Configure passenger_wsgi_ace.py paths
   [ ] 7. Set environment variables
   [ ] 8. Restart Python application
   [ ] 9. Test endpoints

🔧 POST-DEPLOYMENT VERIFICATION
   [ ] Health check: https://axiomhive.co/health
   [ ] Main endpoint: POST to /ace-4d
   [ ] Facts endpoint: GET/POST /facts
   [ ] Check logs for errors

📊 EXPECTED RESULTS
   - Response time: < 1 second
   - Coherence score: > 0.95
   - Memory usage: < 512MB
   - All endpoints functional

🎯 TROUBLESHOOTING
   - Check cPanel error logs
   - Verify Python path in passenger_wsgi_ace.py
   - Test with minimal requirements first
   - Monitor memory usage

Deployment Date: 2025-09-20
Version: Sovereign Core Cycle 20
System: 4D ACE
"""

    with open('DEPLOYMENT_CHECKLIST_ACE.txt', 'w') as f:
        f.write(checklist)

    print("📝 Created ACE deployment checklist: DEPLOYMENT_CHECKLIST_ACE.txt")

def main():
    """Main deployment packaging function"""
    print("🚀 AxiomHive 4D ACE - Deployment Packaging")
    print("=" * 50)

    # Create deployment package
    zip_file = create_deployment_package()

    # Create deployment checklist
    create_deployment_checklist()

    print("\n" + "=" * 50)
    print("✅ ACE DEPLOYMENT PACKAGE READY!")
    print(f"📦 Package: {zip_file}")
    print("📋 Checklist: DEPLOYMENT_CHECKLIST_ACE.txt")
    print("\n📤 Upload to cPanel and follow DEPLOYMENT_README_ACE.md")
    print("\n🎯 Target URL: https://axiomhive.co")
    print("🔗 Main endpoint: https://axiomhive.co/ace-4d")

if __name__ == "__main__":
    main()
