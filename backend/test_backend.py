"""
Simple test script for MAITRI backend
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from emotion_analyzer import EmotionAnalyzer
        print("✓ EmotionAnalyzer imported successfully")
        
        from chatbot import MAITRIChatbot
        print("✓ MAITRIChatbot imported successfully")
        
        from storage import GoogleDriveStorage
        print("✓ GoogleDriveStorage imported successfully")
        
        from alert_system import AlertSystem
        print("✓ AlertSystem imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_emotion_analyzer():
    """Test emotion analyzer initialization"""
    print("\nTesting EmotionAnalyzer...")
    
    try:
        from emotion_analyzer import EmotionAnalyzer
        analyzer = EmotionAnalyzer()
        print("✓ EmotionAnalyzer initialized")
        
        # Test emotion normalization
        normalized = analyzer._normalize_emotion('happy')
        print(f"✓ Emotion normalization works: 'happy' -> '{normalized}'")
        
        return True
    except Exception as e:
        print(f"✗ EmotionAnalyzer error: {e}")
        return False

def test_chatbot():
    """Test chatbot initialization"""
    print("\nTesting MAITRIChatbot...")
    
    try:
        from chatbot import MAITRIChatbot
        chatbot = MAITRIChatbot()
        print("✓ MAITRIChatbot initialized")
        
        # Test emotion response
        response = chatbot.generate_emotion_response('happy')
        print(f"✓ Emotion response generated: '{response[:50]}...'")
        
        # Test chat response
        reply = chatbot.generate_response("Hello", "neutral")
        print(f"✓ Chat response generated: '{reply[:50]}...'")
        
        return True
    except Exception as e:
        print(f"✗ MAITRIChatbot error: {e}")
        return False

def test_storage():
    """Test storage initialization"""
    print("\nTesting GoogleDriveStorage...")
    
    try:
        from storage import GoogleDriveStorage
        storage = GoogleDriveStorage()
        print("✓ GoogleDriveStorage initialized")
        
        if storage.service is None:
            print("  ℹ Using local storage fallback (Google Drive not configured)")
        else:
            print("  ℹ Google Drive API connected")
        
        return True
    except Exception as e:
        print(f"✗ GoogleDriveStorage error: {e}")
        return False

def test_alert_system():
    """Test alert system"""
    print("\nTesting AlertSystem...")
    
    try:
        from alert_system import AlertSystem
        alert_system = AlertSystem()
        print("✓ AlertSystem initialized")
        
        # Test alert check
        should_alert = alert_system.check_alert('stressed', 0.85)
        print(f"✓ Alert check works: stressed@0.85 -> {should_alert}")
        
        should_not_alert = alert_system.check_alert('happy', 0.90)
        print(f"✓ Alert check works: happy@0.90 -> {should_not_alert}")
        
        return True
    except Exception as e:
        print(f"✗ AlertSystem error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("MAITRI Backend Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("EmotionAnalyzer", test_emotion_analyzer()))
    results.append(("Chatbot", test_chatbot()))
    results.append(("Storage", test_storage()))
    results.append(("AlertSystem", test_alert_system()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
