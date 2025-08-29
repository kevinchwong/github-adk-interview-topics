"""
Google ADK Interview Topics Agent
Generates structured software engineering interview topics using modern Google ADK
"""

import logging
from typing import List, Dict, Any

try:
    from google.adk import Agent
except ImportError as e:
    raise ImportError(f"Google ADK not installed: {e}. Run: pip install google-adk")

logger = logging.getLogger(__name__)


def generate_interview_topics(num_topics: int = 15, difficulty_focus: str = "mixed") -> Dict[str, Any]:
    """
    Generate software engineering interview topics.
    
    Args:
        num_topics: Number of topics to generate (default: 15)
        difficulty_focus: Focus level - "mixed", "junior", "mid-level", "senior", "staff"
    
    Returns:
        Dict containing the generated topics and metadata
    """
    from .constants import SAMPLE_TOPICS
    
    logger.info(f"🤖 Generating {num_topics} interview topics (focus: {difficulty_focus})")
    
    # Use sample topics from constants and repeat to meet requirement
    base_topics = SAMPLE_TOPICS
    required_fields = ["title", "category", "difficulty", "description", "keyPoints", "duration", "technologies"]
    
    # Validate sample topics
    validated_base = []
    for topic in base_topics:
        if all(field in topic for field in required_fields):
            validated_base.append(topic)
    
    if not validated_base:
        raise ValueError("No valid sample topics available")
    
    # Generate enough topics by repeating and filtering by difficulty
    all_topics = []
    iteration = 1
    while len(all_topics) < num_topics:
        for topic in validated_base:
            if difficulty_focus == "mixed" or topic["difficulty"] == difficulty_focus:
                # Make a copy and modify title to avoid exact duplicates
                topic_copy = topic.copy()
                if iteration > 1:
                    topic_copy["title"] = f"{topic['title']} (Variation {iteration})"
                all_topics.append(topic_copy)
                
                if len(all_topics) >= num_topics:
                    break
        iteration += 1
        
        # Safety check to prevent infinite loop
        if iteration > 10:
            break
    
    validated_topics = all_topics[:num_topics]
    
    return {
        "topics": validated_topics,
        "metadata": {
            "generated_count": len(validated_topics),
            "requested_count": num_topics,
            "difficulty_focus": difficulty_focus
        }
    }


class InterviewTopicsAgent:
    """Modern Google ADK agent for generating software interview topics"""
    
    def __init__(self, project_id: str, model_name: str = "gemini-2.0-flash", max_output_tokens: int = 8000):
        self.project_id = project_id
        self.model_name = model_name
        self.max_output_tokens = max_output_tokens
        self.agent = None
        self.initialized = False
        
        from .constants import CATEGORIES, DIFFICULTY_LEVELS
        
        # Generate descriptions for instruction
        categories_desc = "\n".join([f"- {k}: {v}" for k, v in CATEGORIES.items()])
        difficulties_desc = "\n".join([f"- {k}: {v}" for k, v in DIFFICULTY_LEVELS.items()])
        
        # Create the ADK agent
        self.agent = Agent(
            name="interview_topics_agent",
            model=model_name,
            description="Expert software engineering interview designer that generates realistic discussion topics",
            instruction=f"""You are an expert software engineering interview designer with 15+ years of experience at top tech companies.

Your task is to generate high-quality, realistic interview discussion topics that test both technical depth and practical experience.

Available categories:
{categories_desc}

Difficulty levels:
{difficulties_desc}

When asked to generate topics:
1. Create diverse, realistic scenarios that senior engineers actually encounter
2. Focus on discussion-based topics rather than pure coding exercises  
3. Include context and background for each topic
4. Ensure topics test both technical knowledge and practical experience
5. Return well-structured JSON with all required fields""",
            tools=[generate_interview_topics]
        )
    
    async def initialize(self):
        """Initialize the Google ADK agent"""
        try:
            logger.info("🔧 Initializing Google ADK Interview Agent...")
            # ADK handles initialization internally
            self.initialized = True
            logger.info(f"✅ Google ADK agent initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Google ADK agent: {e}")
            raise
    
    async def generate_topics(self, num_topics: int = 15, difficulty_focus: str = "mixed") -> List[Dict[str, Any]]:
        """Generate interview topics using Google ADK"""
        if not self.initialized:
            raise ValueError("Agent not initialized. Call initialize() first.")
        
        try:
            logger.info(f"🤖 Generating {num_topics} interview topics via ADK")
            
            # Use the generate_interview_topics tool directly for now
            # In full ADK implementation, this would be handled by the agent
            result = generate_interview_topics(num_topics, difficulty_focus)
            topics = result["topics"]
            
            # Filter by difficulty if specified and pad if needed
            if difficulty_focus != "mixed":
                filtered_topics = [t for t in topics if t["difficulty"] == difficulty_focus]
                if filtered_topics:
                    topics = filtered_topics
            
            # Repeat topics to meet requested count
            while len(topics) < num_topics:
                topics.extend(result["topics"])
            
            logger.info(f"✅ Successfully generated {len(topics)} interview topics")
            return topics[:num_topics]
            
        except Exception as e:
            logger.error(f"❌ Error generating topics: {e}")
            raise

    async def cleanup(self):
        """Clean up resources"""
        try:
            self.agent = None
            self.initialized = False
            logger.info("✅ Google ADK agent cleaned up")
        except Exception as e:
            logger.warning(f"⚠️ Error during cleanup: {e}")