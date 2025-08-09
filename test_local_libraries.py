#!/usr/bin/env python3
"""
Test script to verify local csviper and npd_plainerflow libraries are working
"""

def test_csviper():
    """Test csviper import and basic functionality"""
    try:
        import npd_csviper as csviper
        print("✓ npd_csviper imported successfully")
        
        # Test specific module import
        from npd_csviper.import_executor import ImportExecutor
        print("✓ npd_csviper.import_executor.ImportExecutor imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ npd_csviper import failed: {e}")
        return False

def test_npd_plainerflow():
    """Test npd_plainerflow import and basic functionality"""
    try:
        import npd_plainerflow as plainerflow
        print("✓ npd_plainerflow imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ npd_plainerflow import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing local library installations...")
    print("=" * 50)
    
    csviper_ok = test_csviper()
    print()
    plainerflow_ok = test_npd_plainerflow()
    
    print()
    print("=" * 50)
    if csviper_ok and plainerflow_ok:
        print("✓ All tests passed! Local libraries are working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Check the output above.")
        return 1

if __name__ == '__main__':
    exit(main())
