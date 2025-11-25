"""
Test script for the LLM client manager.

This script verifies that the LLM client can be instantiated and used correctly.
"""

from src.core.llm_clients import (
    get_llm_client,
    get_available_providers,
    validate_provider_config
)


def test_available_providers():
    """Test getting available providers."""
    print("\n=== Testing Available Providers ===")
    providers = get_available_providers()
    print(f"Available providers: {providers}")

    if not providers:
        print("⚠️  No providers configured!")
        return False

    print(f"✓ Found {len(providers)} configured provider(s)")
    return True


def test_provider_validation():
    """Test provider configuration validation."""
    print("\n=== Testing Provider Validation ===")
    providers = get_available_providers()

    for provider in providers:
        is_valid, error = validate_provider_config(provider)
        if is_valid:
            print(f"✓ {provider}: Valid configuration")
        else:
            print(f"✗ {provider}: {error}")

    return True


def test_client_creation():
    """Test creating an LLM client."""
    print("\n=== Testing Client Creation ===")

    try:
        llm = get_llm_client()
        print(f"✓ Successfully created LLM client")
        print(f"  Provider: {llm.__class__.__name__}")
        return True
    except Exception as e:
        print(f"✗ Failed to create LLM client: {e}")
        return False


def test_simple_query():
    """Test a simple query to the LLM."""
    print("\n=== Testing Simple Query ===")

    try:
        llm = get_llm_client()

        response = llm.invoke([
            {"role": "user", "content": "Say 'Hello' in one word."}
        ])

        print(f"✓ Query successful!")
        print(f"  Response: {response.content[:50]}")
        return True
    except Exception as e:
        print(f"✗ Query failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("LLM Client Manager Test Suite")
    print("=" * 60)

    tests = [
        test_available_providers,
        test_provider_validation,
        test_client_creation,
        test_simple_query
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} passed")
    print("=" * 60)

    if passed == total:
        print("✓ All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    main()
