from typing import Dict, Any

TOOL_METADATA: Dict[str, Dict[str, str]] = {
    "get_linkedin_profile_data": {
        "title": "Linkedin Profile Data",
        "description": "Fetching detailed profile information from LinkedIn"
    },
    "get_linkedin_profile_posts": {
        "title": "Linkedin Profile Posts",
        "description": "Retrieving recent posts and activities from the profile"
    },
    "get_linkedin_profile_reactions": {
        "title": "Linkedin Profile Reactions",
        "description": "Analyzing post reactions and engagement patterns"
    },
    "get_linkedin_company_details": {
        "title": "Linkedin Company Details",
        "description": "Gathering comprehensive company information"
    },
    "get_linkedin_company_posts": {
        "title": "Linkedin Company Posts",
        "description": "Collecting recent company updates and announcements"
    },
    "browse_web": {
        "title": "Browse Web",
        "description": "Extracting information from web pages"
    },
    "analyze_with_llm": {
        "title": "Analyze With LLM",
        "description": "Processing and analyzing collected data with AI"
    },
    "search_web": {
        "title": "Search Web",
        "description": "Searching the web for relevant information"
    },
    "search_company_news": {
        "title": "Search Company News",
        "description": "Finding latest news and updates about the company"
    },
    "search_person_news": {
        "title": "Search Person News",
        "description": "Discovering recent news mentions and articles"
    },
    "finish": {
        "title": "Finish",
        "description": "Completing research and generating final assessment"
    }
}
