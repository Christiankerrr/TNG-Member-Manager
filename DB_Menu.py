# Touch-N-Go Member Manager
# Adrian Fanjoy
# Test cases and add/delete

import DB_Manage
from time import time as time_now

# Function to test get_attrs
def test_get_attrs():
    testMemberID = 99999
    testTag = "TEST_TAG"
    testName = "Test Member"
    testEventName = "TEST_EVENT"

    print("\n=== Starting get_attrs() Test ===\n")

    try:
        print("Adding test member and event...")
        DB_Manage.write_member(testMemberID, testTag, testName)
        DB_Manage.write_event(testEventName, False)
        print("Test data created successfully.\n")

        test_cases = [
            # Valid cases
            {
                "description": "Get member by numeric ID (valid)",
                "mode": "members",
                "identifier": testMemberID,
                "expected": "Should return member dict",
                "should_fail": False
            },
            {
                "description": "Get member by tag (valid)",
                "mode": "members",
                "identifier": testTag,
                "expected": "Should return member dict",
                "should_fail": False
            },
            {
                "description": "Get event by name (valid)",
                "mode": "events",
                "identifier": testEventName,
                "expected": "Should return event dict",
                "should_fail": False
            },

            # Invalid cases
            {
                "description": "Invalid mode",
                "mode": "invalid_mode",
                "identifier": testMemberID,
                "expected": "Should raise Exception about invalid mode",
                "should_fail": True
            },
            {
                "description": "Non-existent numeric ID",
                "mode": "members",
                "identifier": 00000,
                "expected": "Should raise Exception about no member found",
                "should_fail": True
            },
            {
                "description": "Non-existent tag",
                "mode": "members",
                "identifier": "NON_EXISTENT_TAG",
                "expected": "Should raise Exception about no member found",
                "should_fail": True
            },
            {
                "description": "Non-existent event",
                "mode": "events",
                "identifier": "NON_EXISTENT_EVENT",
                "expected": "Should raise Exception about no event found",
                "should_fail": True
            },
            {
                "description": "String ID when expecting numeric",
                "mode": "members",
                "identifier": "STRING_ID",
                "expected": "Should raise Exception about no member found",
                "should_fail": True
            }
        ]

        for case in test_cases:
            print(f"\nTest Case: {case['description']}")
            print(f"Mode: {case['mode']}")
            print(f"Identifier: {case['identifier']} (Type: {type(case['identifier']).__name__})")
            print(f"Expected: {case['expected']}")

            try:
                result = DB_Manage.get_attrs(case['mode'], case['identifier'])

                if case['should_fail']:
                    print("❌ Test FAILED - Expected exception but none was raised")
                else:
                    print("✅ Test PASSED")
                    print(f"Result: {result}")
            except Exception as e:
                if case['should_fail']:
                    print(f"✅ Test PASSED (expected exception)")
                    print(f"Exception: {str(e)}")
                else:
                    print(f"❌ Test FAILED - Unexpected exception")
                    print(f"Exception: {str(e)}")

    finally:
        print("\nCleaning up test data...")
        try:
            DB_Manage.remove_member(testMemberID)
            DB_Manage.remove_event(testEventName)
            print("Test data cleaned up successfully.")
        except Exception as e:
            print(f"Warning: Failed to clean up test data: {str(e)}")

        print("\n=== get_attrs() Test Complete ===")

# Function to test edit_attrs
def test_edit_attr():
    testMemberID = 99999
    testTag = "TEST_TAG_EDIT"
    testName = "Test Member Edit"
    testEventName = "TEST_EVENT_EDIT"

    print("\n=== Starting edit_attr() Test ===\n")

    try:
        print("Adding test member and event...")
        DB_Manage.write_member(testMemberID, testTag, testName)
        DB_Manage.write_event(testEventName, False)
        print("Test data created successfully.\n")

        test_cases = [
            # Valid member edits
            {
                "description": "Edit member name (valid by ID)",
                "mode": "members",
                "identifier": testMemberID,
                "attr": "name",
                "value": "Updated Name",
                "force": False,
                "expected": "Should update name successfully",
                "should_fail": False
            },
            {
                "description": "Edit member tag (valid by ID)",
                "mode": "members",
                "identifier": testMemberID,  # Use ID instead of tag
                "attr": "tag",
                "value": "UPDATED_TAG",
                "force": False,
                "expected": "Should update tag successfully",
                "should_fail": False
            },
            {
                "description": "Verify tag update worked",
                "mode": "members",
                "identifier": "UPDATED_TAG",  # Now check by new tag
                "attr": "name",
                "value": testName,  # Just checking we can find it
                "force": False,
                "expected": "Should find member by new tag",
                "should_fail": False
            },
            {
                "description": "Edit member diet (valid list conversion)",
                "mode": "members",
                "identifier": testMemberID,
                "attr": "diet",
                "value": ["vegetarian", "gluten-free"],
                "force": False,
                "expected": "Should convert list to string and update",
                "should_fail": False
            },

            # Valid event edits
            {
                "description": "Edit event start time (valid)",
                "mode": "events",
                "identifier": testEventName,
                "attr": "start",
                "value": time_now(),
                "force": False,
                "expected": "Should update start time successfully",
                "should_fail": False
            },
            {
                "description": "Edit event end time with force (valid)",
                "mode": "events",
                "identifier": testEventName,
                "attr": "end",
                "value": time_now() + 3600,
                "force": True,
                "expected": "Should update end time with force=True",
                "should_fail": False
            },

            # Invalid cases
            {
                "description": "Invalid mode",
                "mode": "invalid_mode",
                "identifier": testMemberID,
                "attr": "name",
                "value": "Should Fail",
                "force": False,
                "expected": "Should raise Exception about invalid mode",
                "should_fail": True
            },
            {
                "description": "Edit non-existent member",
                "mode": "members",
                "identifier": 00000,
                "attr": "name",
                "value": "Should Fail",
                "force": False,
                "expected": "Should raise Exception about no member found",
                "should_fail": True
            },
            {
                "description": "Edit non-existent event",
                "mode": "events",
                "identifier": "NON_EXISTENT_EVENT",
                "attr": "start",
                "value": time_now(),
                "force": False,
                "expected": "Should raise Exception about no event found",
                "should_fail": True
            },
            {
                "description": "Edit invalid attribute",
                "mode": "members",
                "identifier": testMemberID,
                "attr": "invalid_attr",
                "value": "Should Fail",
                "force": False,
                "expected": "Should raise Exception about invalid attribute",
                "should_fail": True
            },
            {
                "description": "Edit isMeeting (should be immutable)",
                "mode": "events",
                "identifier": testEventName,
                "attr": "isMeeting",
                "value": True,
                "force": False,
                "expected": "Should raise Exception about immutable isMeeting",
                "should_fail": True
            },
            {
                "description": "Edit duration without force",
                "mode": "events",
                "identifier": testEventName,
                "attr": "duration",
                "value": 100,
                "force": False,
                "expected": "Should raise Exception about needing force",
                "should_fail": True
            },
            {
                "description": "Edit event end before start",
                "mode": "events",
                "identifier": testEventName,
                "attr": "end",
                "value": time_now() - 3600,
                "force": False,
                "expected": "Should raise Exception about end before start",
                "should_fail": True
            }
        ]

        for case in test_cases:
            print(f"\nTest Case: {case['description']}")
            print(f"Mode: {case['mode']}")
            print(f"Identifier: {case['identifier']} (Type: {type(case['identifier']).__name__})")
            print(f"Attribute: {case['attr']}")
            print(f"Value: {case['value']}")
            print(f"Force: {case['force']}")
            print(f"Expected: {case['expected']}")

            try:
                DB_Manage.edit_attr(
                    case['mode'],
                    case['identifier'],
                    case['attr'],
                    case['value'],
                    case['force']
                )

                if case['should_fail']:
                    print("❌ Test FAILED - Expected exception but none was raised")
                else:
                    print("✅ Test PASSED")
                    result = DB_Manage.get_attrs(case['mode'], case['identifier'])
                    print(f"Updated value: {result.get(case['attr'])}")
            except Exception as e:
                if case['should_fail']:
                    print(f"✅ Test PASSED (expected exception)")
                    print(f"Exception: {str(e)}")
                else:
                    print(f"❌ Test FAILED - Unexpected exception")
                    print(f"Exception: {str(e)}")

    finally:
        print("\nCleaning up test data...")
        try:
            DB_Manage.remove_member(testMemberID)
            DB_Manage.remove_event(testEventName)
            print("Test data cleaned up successfully.")
        except Exception as e:
            print(f"Warning: Failed to clean up test data: {str(e)}")

        print("\n=== edit_attr() Test Complete ===")

# Function to test add_attend
def test_add_attend():
    testMemberID = 88888
    testTag = "ATTEND_TEST_TAG"
    testName = "Attend Test Member"
    testEventName = "ATTEND_TEST_EVENT"

    print("\n=== Starting add_attend() Test ===\n")

    try:
        print("Creating test data...")
        DB_Manage.write_member(testMemberID, testTag, testName)
        DB_Manage.write_event(testEventName, False)
        print(f"Created member {testMemberID} and event '{testEventName}'")

        # Test cases
        test_cases = [
            {
                "description": "Add member to event (first time - should succeed)",
                "event": testEventName,
                "member": testMemberID,
                "expected": "Should add member to attendees",
                "should_fail": False
            },
            {
                "description": "Add same member again (should prevent duplicate)",
                "event": testEventName,
                "member": testMemberID,
                "expected": "Should raise exception for duplicate attendee",
                "should_fail": True
            },
            {
                "description": "Add member to non-existent event",
                "event": "NON_EXISTENT_EVENT",
                "member": testMemberID,
                "expected": "Should raise exception for event not found",
                "should_fail": True
            },
            {
                "description": "Add non-existent member to event",
                "event": testEventName,
                "member": 00000,
                "expected": "Should raise exception for member not found",
                "should_fail": True
            }
        ]

        # Run test cases
        for case in test_cases:
            print(f"\nTest Case: {case['description']}")
            print(f"Event: {case['event']}")
            print(f"Member ID: {case['member']}")
            print(f"Expected: {case['expected']}")

            try:
                DB_Manage.add_attend(case['event'], case['member'])

                if case['should_fail']:
                    print("❌ Test FAILED - Expected exception but none was raised")
                    event_data = DB_Manage.get_attrs("events", case['event'])
                    print(f"Current attendees: {event_data['attendees']}")
                else:
                    print("✅ Test PASSED")
                    event_data = DB_Manage.get_attrs("events", case['event'])
                    print(f"Current attendees: {event_data['attendees']}")
            except Exception as e:
                if case['should_fail']:
                    print(f"✅ Test PASSED (expected exception)")
                    print(f"Exception: {str(e)}")
                else:
                    print(f"❌ Test FAILED - Unexpected exception")
                    print(f"Exception: {str(e)}")

    finally:
        print("\nCleaning up test data...")
        try:
            DB_Manage.remove_member(testMemberID)
            DB_Manage.remove_event(testEventName)
            print("Test data cleaned up successfully.")
        except Exception as e:
            print(f"Warning: Cleanup failed: {str(e)}")

        print("\n=== add_attend() Test Complete ===")

# Boolean to run menu
running = True

# Menu
if __name__ == "__main__":
    while running:
        print("1. Create database")
        print("2. Delete database")
        print("3. Test get_attrs function")
        print("4. Test edit_attrs function")
        print("5. Test add_attend function")
        print("10. Exit")
        choice = input("Choose from the options above:")

        # Switch case
        if choice == "1":
            print(DB_Manage.create_database())
        elif choice == "2":
            print(DB_Manage.delete_database("memberdb"))
        elif choice == "3":
            test_get_attrs()
        elif choice == "4":
            test_edit_attr()
        elif choice == "5":
            test_add_attend()
        elif choice == "10":
            running = False
        else:
            print("Enter a valid choice.")