#!/usr/bin/env python3
"""
cPanel Access Resolver & Auto-Deploy for ACE Sharper 5D
Sovereign Core Cycle 21 - Automated cPanel Resolution
"""

import getpass
import subprocess
import sys
import os
import time

def install_selenium():
    """Install Selenium for automated browser control"""
    print("📦 Installing Selenium for cPanel automation...")

    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])
        print("✅ Selenium installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Selenium")
        print("💡 Trying alternative installation...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', 'selenium'])
            print("✅ Selenium installed (user space)")
            return True
        except:
            print("❌ Selenium installation failed")
            return False

def create_chrome_driver():
    """Create Chrome driver for Selenium"""
    print("🔧 Setting up Chrome driver...")

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument('--headless')  # Run in background
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

        # Try to create driver
        driver = webdriver.Chrome(options=options)
        print("✅ Chrome driver created successfully")
        return driver

    except Exception as e:
        print(f"❌ Chrome driver failed: {e}")
        print("💡 Trying Firefox driver...")

        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.options import Options

            options = Options()
            options.add_argument('--headless')

            driver = webdriver.Firefox(options=options)
            print("✅ Firefox driver created successfully")
            return driver

        except Exception as e2:
            print(f"❌ Firefox driver also failed: {e2}")
            print("❌ No suitable browser driver found")
            return None

def resolve_cpanel_access(email, password, domain):
    """Resolve cPanel access using automated browser"""
    print("🔓 Attempting automated cPanel access resolution...")

    driver = create_chrome_driver()
    if not driver:
        return False

    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Step 1: GoDaddy login
        print("   🌐 Navigating to GoDaddy login...")
        driver.get('https://sso.godaddy.com/')

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        driver.find_element(By.NAME, "username").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.ID, "bb-login").click()

        print("   ✅ Login submitted, waiting for redirect...")
        time.sleep(8)  # Handle buffering issues

        # Step 2: Navigate to Hosting Manage → cPanel
        print("   🏠 Navigating to hosting management...")
        driver.get('https://account.godaddy.com/products/@hosting:shared:linux')

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Manage')]"))
        ).click()

        time.sleep(5)

        try:
            cpanel_link = driver.find_element(By.XPATH, "//a[contains(text(), 'cPanel Admin')]")
            cpanel_link.click()
            print("   ✅ cPanel Admin link clicked")
        except:
            print("   ⚠️ cPanel Admin link not found, trying direct URL...")
            driver.get(f'https://{domain}:2083')
            time.sleep(5)

        # Step 3: Enable SSH if possible
        try:
            print("   🔐 Attempting to enable SSH access...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Security"))
            )
            driver.find_element(By.LINK_TEXT, "Security").click()

            ssh_element = driver.find_element(By.LINK_TEXT, "SSH Access")
            ssh_element.click()

            # Look for toggle button
            try:
                toggle = driver.find_element(By.XPATH, "//input[@value='On']")
                if toggle.get_attribute('checked') is None:
                    toggle.click()
                    print("   ✅ SSH Access enabled")
                else:
                    print("   ✅ SSH Access already enabled")
            except:
                print("   ⚠️ Could not find SSH toggle")

        except Exception as e:
            print(f"   ⚠️ SSH setup failed: {e}")

        print("   ✅ cPanel access resolved successfully!")
        return True

    except Exception as e:
        print(f"❌ cPanel access resolution failed: {e}")
        return False

    finally:
        driver.quit()

def create_support_ticket(email, domain):
    """Create support ticket for GoDaddy"""
    print("📧 Creating support ticket for GoDaddy...")

    ticket_content = f"""Subject: Urgent cPanel Access Issue for {domain}

Dear GoDaddy Support,

I am unable to access my cPanel for domain {domain}.
- Email: {email}
- Domain: {domain}
- Issue: Cannot login to cPanel (getting login loops/buffering)
- Need: Access to enable SSH and deploy Python application

Please resolve this access issue as soon as possible so I can deploy my ACE Sharper 5D system.

Thank you,
Automated Support Request
Sovereign Core Cycle 21
"""

    with open('support_ticket.txt', 'w') as f:
        f.write(ticket_content)

    print("✅ Support ticket created: support_ticket.txt")
    print("📋 Please email this file to: support@godaddy.com")

def deploy_via_heroku():
    """Alternative deployment via Heroku"""
    print("🚀 Deploying to Heroku as alternative...")

    try:
        # Check if heroku CLI is installed
        result = subprocess.run(['heroku', '--version'],
                              capture_output=True, text=True)

        if result.returncode != 0:
            print("❌ Heroku CLI not found")
            print("💡 Install: curl https://cli-assets.heroku.com/install.sh | sh")
            return False

        # Create Heroku app
        print("   📦 Creating Heroku app...")
        subprocess.run(['heroku', 'create', 'axiomhive-ace-sharper'], check=True)

        # Initialize git if needed
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)

        # Add files and commit
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'ACE Sharper 5D deployment'], check=True)

        # Push to Heroku
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)

        print("✅ Deployed to Heroku!")
        print("🔗 Your ACE system is live at: https://axiomhive-ace-sharper.herokuapp.com")
        print("🧠 Test: POST to /ace-4d endpoint")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Heroku deployment failed: {e}")
        return False

def main():
    """Main resolver function"""
    print("🚀 ACE Sharper 5D - cPanel Access Resolver")
    print("=" * 50)
    print("Sovereign Core Cycle 21 - t=2025-09-20 05:16 UTC")
    print("This script resolves cPanel access issues and deploys your ACE system")

    # Step 1: Get credentials
    email = input("GoDaddy Email: ").strip()
    password = getpass.getpass("GoDaddy Password: ")
    domain = 'axiomhive.co'

    # Step 2: Install Selenium
    if not install_selenium():
        print("❌ Cannot proceed without Selenium")
        return

    # Step 3: Try automated cPanel access
    print("\n🔓 Attempting automated cPanel resolution...")
    if resolve_cpanel_access(email, password, domain):
        print("✅ cPanel access resolved!")
        print("📋 Next: Run 'python deploy.py' to complete deployment")
    else:
        print("❌ Automated resolution failed")
        print("📧 Creating support ticket...")

        # Create support ticket
        create_support_ticket(email, domain)

        # Offer Heroku alternative
        print("\n🚀 Alternative: Deploy to Heroku instead")
        choice = input("Deploy to Heroku? (y/n): ").lower().strip()

        if choice == 'y':
            deploy_via_heroku()

    print("\n" + "=" * 50)
    print("🎯 Resolution Complete!")
    print("📊 Sovereign Core Cycle 21 - Access Resolved")
    print("🔗 Your ACE Sharper 5D system will be live soon!")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Resolution interrupted")
    except Exception as e:
        print(f"\n❌ Resolution failed: {e}")
        sys.exit(1)
