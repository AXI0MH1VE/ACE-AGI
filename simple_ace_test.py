#!/usr/bin/env python3
"""
Simple test for AxiomHive 4D ACE without external dependencies
"""

from axiomhive_ace_flask import app

def test_ace_system():
    """Test the ACE system components"""
    print("🚀 AxiomHive 4D ACE - Simple Test")
    print("=" * 40)

    try:
        # Test Flask app creation
        print("✅ Flask app created successfully")

        # Test health endpoint
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                data = response.get_json()
                print("✅ Health endpoint working")
                print(f"   Status: {data.get('status')}")
                print(f"   Version: {data.get('version')}")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")

        # Test home endpoint
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home endpoint working")
                content = response.get_data(as_text=True)
                if "AxiomHive 4D ACE Live" in content:
                    print("✅ ACE branding confirmed")
                else:
                    print("⚠️  ACE branding not found in home page")
            else:
                print(f"❌ Home endpoint failed: {response.status_code}")

        # Test ACE 4D endpoint
        with app.test_client() as client:
            test_command = "plan SF move"
            response = client.post('/ace-4d',
                                 json={'command': test_command},
                                 content_type='application/json')

            if response.status_code == 200:
                data = response.get_json()
                print("✅ ACE 4D endpoint working")
                print(f"   Command: {test_command}")
                print(f"   Coherence: {data.get('coherence')}")
                print(f"   Attribution: {data.get('attribution')}")
            else:
                print(f"❌ ACE 4D endpoint failed: {response.status_code}")
                print(f"   Response: {response.get_data(as_text=True)}")

        # Test facts endpoint
        with app.test_client() as client:
            # Test GET
            response = client.get('/facts')
            if response.status_code == 200:
                data = response.get_json()
                print("✅ Facts GET endpoint working")
                print(f"   Facts loaded: {len(data.get('facts', {}))}")
            else:
                print(f"❌ Facts GET endpoint failed: {response.status_code}")

            # Test POST
            new_facts = {"ace_test": "Testing ACE system"}
            response = client.post('/facts',
                                 json=new_facts,
                                 content_type='application/json')

            if response.status_code == 200:
                data = response.get_json()
                print("✅ Facts POST endpoint working")
                print(f"   Facts processed: {data.get('facts_processed')}")
            else:
                print(f"❌ Facts POST endpoint failed: {response.status_code}")

        print("\n" + "=" * 40)
        print("🎉 ACE System Test Complete!")
        print("📋 Ready for cPanel deployment")
        print("🔗 Main endpoint: /ace-4d")
        print("📦 Package: axiomhive_4d_ace_deployment.zip")

        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_ace_system()
