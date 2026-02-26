"""
Migration Verification Script
Checks that the GameObject system is fully integrated and old systems are removed.
"""

import os
import sys

def check_file_exists(path, should_exist=True):
    exists = os.path.exists(path)
    status = "[OK]" if exists == should_exist else "[FAIL]"
    expected = "exists" if should_exist else "removed"
    actual = "exists" if exists else "removed"
    print(f"{status} {path} - Expected: {expected}, Actual: {actual}")
    return exists == should_exist

def check_import_in_file(filepath, import_statement, should_exist=True):
    if not os.path.exists(filepath):
        print(f"[FAIL] {filepath} does not exist")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
        exists = import_statement in content
        status = "[OK]" if exists == should_exist else "[FAIL]"
        expected = "present" if should_exist else "removed"
        actual = "present" if exists else "removed"
        print(f"{status} '{import_statement}' in {filepath} - Expected: {expected}, Actual: {actual}")
        return exists == should_exist

def main():
    print("=" * 60)
    print("GameObject System Migration Verification")
    print("=" * 60)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    all_checks_passed = True
    
    print("\n1. Checking new GameObject system files exist...")
    all_checks_passed &= check_file_exists(os.path.join(base_path, "objects", "game_object.py"), True)
    all_checks_passed &= check_file_exists(os.path.join(base_path, "objects", "object_types.py"), True)
    all_checks_passed &= check_file_exists(os.path.join(base_path, "objects", "object_factory.py"), True)
    
    print("\n2. Checking old system files are removed...")
    all_checks_passed &= check_file_exists(os.path.join(base_path, "jsonHandler"), False)
    all_checks_passed &= check_file_exists(os.path.join(base_path, "objects", "block.py"), False)
    
    print("\n3. Checking game_state.py uses new system...")
    game_state_path = os.path.join(base_path, "game_state.py")
    all_checks_passed &= check_import_in_file(game_state_path, "from main.objects.object_factory import ObjectFactory", True)
    all_checks_passed &= check_import_in_file(game_state_path, "ObjectFactory.create", True)
    all_checks_passed &= check_import_in_file(game_state_path, "from main.objects.block import Platform", False)
    
    print("\n4. Checking player_file.py uses polymorphic collision...")
    player_path = os.path.join(base_path, "playerDir", "player_file.py")
    all_checks_passed &= check_import_in_file(player_path, "check_objects", True)
    all_checks_passed &= check_import_in_file(player_path, "check_platforms", False)
    
    print("\n5. Checking objects.json has new format...")
    objects_json_path = os.path.join(base_path, "objects.json")
    all_checks_passed &= check_import_in_file(objects_json_path, '"object":', True)
    
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("[SUCCESS] ALL CHECKS PASSED - Migration Complete!")
    else:
        print("[FAILED] SOME CHECKS FAILED - Review above")
    print("=" * 60)
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
