#!/usr/bin/env python3
"""
Test script for AxiomHive 4D Nexus
Run this locally to verify functionality before cPanel deployment
"""

import requests
import json
import sys
from axiomhive_flask import app

def test_health():
    """Test health endpoint"""
    print("🧪 Testing health endpoint...")
    try:
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Health check passed: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_home():
    """Test home endpoint"""
    print("🧪 Testing home endpoint...")
    try:
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home endpoint working")
                print(f"Response: {response.get_data(as_text=True)[:200]}...")
                return True
            else:
                print(f"❌ Home endpoint failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Home endpoint error: {e}")
        return False

def test_grok_4d():
    """Test main 4D Grok endpoint"""
    print("🧪 Testing /grok-4d endpoint...")
    test_commands = [
        "plan SF move",
        "integrate facts about gym membership",
        "analyze ecosystem binding"
    ]

    for command in test_commands:
        try:
            with app.test_client() as client:
                response = client.post('/grok-4d',
                                     data=json.dumps({'command': command}),
                                     content_type='application/json')

                if response.status_code == 200:
                    data = response.get_json()
                    print(f"✅ Command '{command}' processed successfully")
                    print(f"   Coherence: {data.get('coherence', 'N/A')}")
                    print(f"   Attribution: {data.get('attribution', 'N/A')}")
                else:
                    print(f"❌ Command '{command}' failed: {response.status_code}")
                    print(f"   Response: {response.get_data(as_text=True)}")
        except Exception as e:
            print(f"❌ Command '{command}' error: {e}")

def test_facts():
    """Test facts endpoint"""
    print("🧪 Testing facts endpoint...")
    try:
        with app.test_client() as client:
            # Test GET
            response = client.get('/facts')
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Facts GET working: {len(data.get('facts', {}))} facts loaded")

            # Test POST
            new_facts = {
                "test_fact": "This is a test fact for deployment verification",
                "deployment_date": "2025-09-20"
            }

            response = client.post('/facts',
                                 data=json.dumps(new_facts),
                                 content_type='application/json')

            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Facts POST working: {data.get('facts_processed', 0)} facts processed")
            else:
                print(f"❌ Facts POST failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Facts endpoint error: {e}")

def main():
    """Run all tests"""
    print("🚀 AxiomHive 4D Nexus - Local Test Suite")
    print("=" * 50)

    tests = [
        ("Health Check", test_health),
        ("Home Endpoint", test_home),
        ("4D Grok Processing", test_grok_4d),
        ("Facts Management", test_facts)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed! Ready for cPanel deployment.")
        print("📋 Next steps:")
        print("   1. Upload files to cPanel")
        print("   2. Setup Python App")
        print("   3. Install requirements")
        print("   4. Configure WSGI")
        print("   5. Test live at axiomhive.co")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
