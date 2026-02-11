#!/usr/bin/env python3
"""
Quick test script to verify the Vercel deployment setup
"""
import os
import sys

def test_environment():
    print("🔍 Testing Vercel Deployment Environment...")
    
    # Check environment variables
    print("\n📋 Checking Environment Variables:")
    required_vars = ["COHERE_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: SET")
        else:
            print(f"  ❌ {var}: MISSING")
            all_set = False
    
    if not all_set:
        print(f"\n❌ Not all required environment variables are set.")
        print(f"Required: {', '.join(required_vars)}")
        return False
    
    # Check dependencies
    print("\n📦 Checking Dependencies:")
    dependencies = ["fastapi", "cohere", "qdrant_client", "requests", "bs4"]
    
    all_deps_ok = True
    for dep in dependencies:
        try:
            if dep == "bs4":
                import bs4
            else:
                __import__(dep)
            print(f"  ✅ {dep}: AVAILABLE")
        except ImportError:
            print(f"  ❌ {dep}: MISSING")
            all_deps_ok = False
    
    if not all_deps_ok:
        print("\n❌ Not all required dependencies are installed.")
        print("Make sure your requirements.txt includes: cohere, qdrant-client, requests, beautifulsoup4")
        return False
    
    print("\n🎉 Environment is properly configured!")
    print("✅ All environment variables are set")
    print("✅ All dependencies are available")
    print("\n💡 Your Vercel deployment should work correctly now!")
    return True

if __name__ == "__main__":
    success = test_environment()
    if not success:
        print("\n🔧 Please fix the issues above before deploying to Vercel.")
        sys.exit(1)
    else:
        print("\n🚀 Ready for Vercel deployment!")