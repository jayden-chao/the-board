#!/usr/bin/env python
"""
Simple test script for TheBoard
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from crew import TheBoard, load_prompts

def test_basic():
    """Test TheBoard with a simple input"""
    print("=" * 60)
    print("Testing TheBoard - Basic Test")
    print("=" * 60)
    
    # Load perspective prompts
    perspective_prompts = load_prompts('perspectives')
    
    # Test with contrarian perspective
    perspective = "contrarian"
    perspective_prompt = perspective_prompts['perspectives'][perspective]
    
    print(f"\nUsing perspective: {perspective}")
    print(f"Perspective prompt: {perspective_prompt[:100]}...\n")
    
    # Create board instance
    board = TheBoard(perspective_prompt)
    
    # Test input
    test_input = "I want to start a new business selling coffee online."
    
    print(f"Test input: {test_input}\n")
    print("Running pipeline...\n")
    
    try:
        result = board.run_pipeline(test_input)
        
        print("=" * 60)
        print("RESULT:")
        print("=" * 60)
        
        # Try to extract the final response
        try:
            reply = result["tasks_output"][-1]["raw"]
            print(f"\nFinal Response:\n{reply}\n")
        except (KeyError, TypeError, IndexError):
            print(f"\nFull Result:\n{result}\n")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_different_perspectives():
    """Test with different perspectives"""
    print("\n" + "=" * 60)
    print("Testing Different Perspectives")
    print("=" * 60)
    
    perspective_prompts = load_prompts('perspectives')
    test_input = "I'm thinking about learning Python programming."
    
    for perspective_name in ["contrarian", "supporter"]:
        print(f"\n--- Testing with {perspective_name} perspective ---")
        perspective_prompt = perspective_prompts['perspectives'][perspective_name]
        board = TheBoard(perspective_prompt)
        
        try:
            result = board.run_pipeline(test_input)
            try:
                reply = result["tasks_output"][-1]["raw"]
                print(f"Response: {reply}\n")
            except (KeyError, TypeError, IndexError):
                print(f"Result: {result}\n")
        except Exception as e:
            print(f"ERROR: {e}\n")

if __name__ == "__main__":
    # Check for environment variables
    api_key = os.getenv("API_KEY")
    model = os.getenv("MODEL")
    
    if not api_key or not model:
        print("WARNING: API_KEY and MODEL environment variables should be set.")
        print("Please create a .env file with:")
        print("  API_KEY=your_api_key")
        print("  MODEL=your_model_name")
        print("\nContinuing anyway...\n")
    
    # Run basic test
    success = test_basic()
    
    if success and len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Run additional tests
        test_different_perspectives()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
