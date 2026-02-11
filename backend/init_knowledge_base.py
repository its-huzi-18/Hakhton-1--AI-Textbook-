#!/usr/bin/env python3
"""
Simple initialization script to populate the knowledge base
Run this script after deploying your backend and frontend
"""

import os
import sys
import time

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def initialize_knowledge_base():
    print("Starting knowledge base initialization...")
    
    # Check if environment variables are set
    required_vars = ['COHERE_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY', 'TARGET_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"ERROR: Missing environment variables: {missing_vars}")
        print("Please set all required environment variables before running this script.")
        return False
    
    print("✓ All environment variables are set")
    
    # Import and run the process_book function
    try:
        print("Importing process_book module...")
        from process_book import process_book
        print("✓ Successfully imported process_book")
        
        print("Starting book processing...")
        process_book()
        print("✓ Knowledge base initialization completed successfully!")
        return True
        
    except ImportError as e:
        print(f"ERROR: Could not import process_book: {e}")
        print("Make sure you're running this script from the backend directory")
        return False
    except Exception as e:
        print(f"ERROR: Failed to initialize knowledge base: {e}")
        return False

if __name__ == "__main__":
    print("AI Textbook Knowledge Base Initializer")
    print("=" * 40)
    
    success = initialize_knowledge_base()
    
    if success:
        print("\n🎉 Success! Your knowledge base has been populated.")
        print("Your chatbot should now be able to answer questions about your textbook content.")
    else:
        print("\n❌ Initialization failed. Please check the error messages above.")
        print("Make sure:")
        print("- All environment variables are set correctly")
        print("- Your frontend is deployed and accessible")
        print("- You're running this script from the backend directory")
    
    input("\nPress Enter to exit...")