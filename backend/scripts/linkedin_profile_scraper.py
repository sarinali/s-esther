import asyncio
import sys
import os

# Add the parent directory to the path so we can import from services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.linkedin_api_enhanced_service import service as linkedin_service

async def test_linkedin_api():
    print("=== Testing LinkedIn API Service ===")

    try:
        # Initialize the LinkedIn API service
        print("Initializing LinkedIn API service...")
        linkedin_service.initialize()
        print("✅ LinkedIn API initialized successfully")

        # Test 2: Get single profile by URL
        print("\n--- Test 2: Getting profile by URL ---")
        try:
            profile = await linkedin_service.get_single_profile("https://www.linkedin.com/in/sarinali/")
            print(f"✅ Successfully fetched profile:")
            print(f"   Name: {profile.name}")
            print(f"   Profile Link: {profile.profile_link}")
            print(f"   Job Title: {profile.job_title}")
            print(f"   Location: {profile.location}")
            print(f"   Profile Image: {profile.profile_image_url}")
        except Exception as e:
            print(f"❌ Error fetching single profile: {e}")

        # Test 3: Search for profiles
        print("\n--- Test 3: Searching for profiles ---")
        try:
            profiles = await linkedin_service.get_user_profiles("software engineer")
            print(f"✅ Found {len(profiles)} profiles for 'software engineer'")

            for i, profile in enumerate(profiles[:3]):  # Show first 3 results
                print(f"   Profile {i+1}:")
                print(f"     Name: {profile.name}")
                print(f"     Job Title: {profile.job_title}")
                print(f"     Location: {profile.location}")
                print(f"     Profile Link: {profile.profile_link}")
                print()
        except Exception as e:
            print(f"❌ Error searching profiles: {e}")

    except Exception as e:
        print(f"❌ Failed to initialize LinkedIn API: {e}")
        print("Make sure LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables are set")

if __name__ == "__main__":
    asyncio.run(test_linkedin_api())