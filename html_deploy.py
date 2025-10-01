#!/usr/bin/env python3
"""
HTML Deployment Script for ACE Sharper 5D
Simple file upload to any web hosting service
"""

import ftplib
import os
import getpass
import sys

def get_deployment_info():
    """Get deployment information from user"""
    print("🚀 ACE Sharper 5D - HTML Deployment")
    print("=" * 40)
    print("Deploying HTML interface to web hosting")

    print("\n📋 Deployment Options:")
    print("1. GoDaddy (ftp.yourdomain.com)")
    print("2. Other hosting (ftp.yourhost.com)")
    print("3. Local testing (no upload)")

    choice = input("\nChoose deployment type (1-3): ").strip()

    if choice == '3':
        return None, None, None, None

    ftp_host = input("FTP Host (e.g., ftp.axiomhive.co): ").strip()
    ftp_user = input("FTP Username: ").strip()
    ftp_pass = getpass.getpass("FTP Password: ")

    remote_dir = input("Remote directory (default: /public_html): ").strip() or "/public_html"

    return ftp_host, ftp_user, ftp_pass, remote_dir

def create_deployment_package():
    """Create deployment package with HTML files"""
    print("\n📦 Creating deployment package...")

    files_to_deploy = [
        'ace_html_interface.html',
        'index.html',
        'styles.css',
        'script.js',
        'README.md'
    ]

    # Create deployment info
    deployment_info = f"""ACE Sharper 5D - HTML Deployment
=====================================

Files deployed: {', '.join(files_to_deploy)}
Deployment Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Version: Sovereign Core Cycle 21

Access your ACE system at:
- Main Interface: https://yourdomain.com/ace_html_interface.html
- Alternative: https://yourdomain.com/index.html

For full Python ACE system, see COMPLETE_DEPLOYMENT_GUIDE.md
"""

    with open('HTML_DEPLOYMENT_INFO.txt', 'w') as f:
        f.write(deployment_info)

    files_to_deploy.append('HTML_DEPLOYMENT_INFO.txt')

    print("✅ Created deployment package with files:")
    for file in files_to_deploy:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   📄 {file} ({size} bytes)")
        else:
            print(f"   ⚠️ {file} (not found)")

    return files_to_deploy

def upload_files(ftp_host, ftp_user, ftp_pass, remote_dir, files):
    """Upload files via FTP"""
    print(f"\n📤 Uploading to {ftp_host}...")

    try:
        ftp = ftplib.FTP(ftp_host)
        ftp.login(ftp_user, ftp_pass)

        # Change to remote directory
        try:
            ftp.cwd(remote_dir)
        except:
            print(f"⚠️ Directory {remote_dir} not found, using root")
            ftp.cwd('/')

        # Upload each file
        for file_path in files:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    try:
                        ftp.storbinary(f'STOR {file_path}', f)
                        print(f"   ✅ Uploaded: {file_path}")
                    except Exception as e:
                        print(f"   ❌ Failed to upload {file_path}: {e}")

        ftp.quit()
        print("✅ Upload completed successfully!")
        return True

    except Exception as e:
        print(f"❌ FTP upload failed: {e}")
        return False

def create_local_test():
    """Create local test setup"""
    print("\n🧪 Setting up local test environment...")

    test_commands = """
# To test locally:
1. Open terminal in this directory
2. Start local server:
   python3 -m http.server 8000

3. Open browser and go to:
   http://localhost:8000/ace_html_interface.html

4. Test ACE commands:
   - "plan SF move"
   - "analyze ecosystem binding"
   - "integrate facts about gym membership"
"""

    with open('LOCAL_TEST_INSTRUCTIONS.txt', 'w') as f:
        f.write("ACE Sharper 5D - Local Testing Instructions\n")
        f.write("=" * 50)
        f.write(f"\nDate: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        f.write("\n\n" + test_commands)

    print("✅ Created local test instructions: LOCAL_TEST_INSTRUCTIONS.txt")
    print("\n🚀 To test locally:")
    print("   1. Run: python3 -m http.server 8000")
    print("   2. Open: http://localhost:8000/ace_html_interface.html")

def main():
    """Main deployment function"""
    print("🚀 ACE Sharper 5D - HTML Deployment Script")
    print("=" * 50)
    print("Sovereign Core Cycle 21 - t=2025-09-20")
    print("Deploy HTML interface to any web hosting service")

    # Get deployment info
    ftp_host, ftp_user, ftp_pass, remote_dir = get_deployment_info()

    if ftp_host is None:
        # Local testing only
        create_deployment_package()
        create_local_test()
        return

    # Create deployment package
    files = create_deployment_package()

    # Upload files
    if upload_files(ftp_host, ftp_user, ftp_pass, remote_dir, files):
        print("\n" + "=" * 50)
        print("🎉 HTML Deployment Complete!")
        print("📊 Sovereign Core Cycle 21 - Successfully Deployed")
        print("\n🔗 Access your ACE system at:")
        print(f"   🌐 https://{ftp_host.replace('ftp.', '')}/ace_html_interface.html")
        print(f"   📱 https://{ftp_host.replace('ftp.', '')}/index.html")
        print("\n🧠 Test commands:")
        print("   - 'plan SF move'")
        print("   - 'analyze ecosystem binding'")
        print("   - 'integrate facts about gym membership'")
        print("\n📋 For full Python ACE system, see COMPLETE_DEPLOYMENT_GUIDE.md")
        print("=" * 50)
    else:
        print("\n❌ Deployment failed - files not uploaded")
        print("💡 Try local testing instead:")
        print("   python3 -m http.server 8000")
        print("   Then visit: http://localhost:8000/ace_html_interface.html")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Deployment interrupted")
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        sys.exit(1)
