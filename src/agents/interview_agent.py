"""
Google ADK Interview Topics Agent
Generates structured software engineering interview topics using Gemini
"""

import json
import logging
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime

# Google ADK and Vertex AI imports
try:
    from google.cloud import aiplatform
    from google.oauth2 import service_account
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
    from vertexai.generative_models import GenerationConfig
except ImportError as e:
    raise ImportError(f"Required Google Cloud libraries not installed: {e}")

logger = logging.getLogger(__name__)


class InterviewTopicsAgent:
    """Google ADK agent for generating software interview topics"""
    
    def __init__(self, project_id: str, model_name: str = "gemini-pro"):
        self.project_id = project_id
        self.model_name = model_name
        self.model = None
        self.initialized = False
        
        # Interview categories and their focus areas
        self.categories = {
            "technical_coding": "Coding challenges, algorithms, data structures",
            "system_design": "Architecture decisions, scalability, distributed systems",
            "behavioral": "Leadership, teamwork, problem-solving approaches", 
            "technology_deep_dive": "Specific technology expertise and experience",
            "architecture_decisions": "Technical trade-offs, design patterns, best practices",
            "debugging_troubleshooting": "Problem diagnosis, error handling, performance issues",
            "testing_quality": "Testing strategies, QA processes, code quality",
            "devops_deployment": "CI/CD, infrastructure, monitoring, deployment strategies"
        }
        
        # Difficulty level mappings
        self.difficulty_levels = {
            "junior": "Entry-level (0-2 years experience)",
            "mid-level": "Experienced developer (3-5 years experience)", 
            "senior": "Senior engineer (6+ years experience)",
            "staff": "Staff/Principal engineer (8+ years experience)"
        }
    
    async def initialize(self):
        """Initialize the Google ADK agent and Vertex AI"""
        try:
            logger.info("🔧 Initializing Google ADK Interview Agent...")
            
            # Initialize Vertex AI
            vertexai.init(project=self.project_id, location="us-central1")
            
            # Initialize the generative model
            self.model = GenerativeModel(self.model_name)
            
            self.initialized = True
            logger.info(f"✅ Google ADK agent initialized with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Google ADK agent: {e}")
            raise
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for interview topic generation"""
        categories_str = "\n".join([f"- {k}: {v}" for k, v in self.categories.items()])
        difficulties_str = "\n".join([f"- {k}: {v}" for k, v in self.difficulty_levels.items()])
        
        return f"""You are an expert software engineering interview designer with 15+ years of experience at top tech companies (Google, Meta, Apple, Amazon, Microsoft).

Your task is to generate high-quality, realistic interview discussion topics that test both technical depth and practical experience.

AVAILABLE CATEGORIES:
{categories_str}

DIFFICULTY LEVELS:
{difficulties_str}

REQUIREMENTS:
1. Create diverse, realistic scenarios that senior engineers actually encounter
2. Focus on discussion-based topics rather than pure coding exercises
3. Include context and background for each topic
4. Ensure topics test both technical knowledge and practical experience
5. Return ONLY a JSON array of topic objects

RESPONSE FORMAT:
Return exactly this JSON structure with NO additional text:

[
  {{
    "title": "Specific, engaging topic title",
    "category": "one of the available categories above",
    "difficulty": "one of: junior, mid-level, senior, staff",
    "description": "Detailed scenario or question (2-3 sentences)",
    "keyPoints": ["point1", "point2", "point3"],
    "duration": 30,
    "technologies": ["tech1", "tech2", "tech3"]
  }}
]

Focus on creating realistic, practical scenarios that experienced engineers face in their daily work."""

    def _build_user_prompt(self, num_topics: int, difficulty_focus: str) -> str:
        """Build the user prompt with specific requirements"""
        focus_instruction = ""
        if difficulty_focus != "mixed":
            focus_instruction = f"Focus primarily on {difficulty_focus} level topics (80% of topics)."
        
        return f"""Generate {num_topics} software engineering interview discussion topics.

REQUIREMENTS:
- {focus_instruction}
- Mix different categories evenly
- Include modern technologies and practices
- Focus on real-world scenarios
- Ensure topics are discussion-heavy rather than coding-heavy
- Duration should be 20-60 minutes per topic
- Include 3-5 key discussion points per topic
- List 2-4 relevant technologies per topic

Generate exactly {num_topics} topics and return only the JSON array."""

    async def generate_topics(self, num_topics: int = 15, difficulty_focus: str = "mixed") -> List[Dict[str, Any]]:
        """Generate interview topics using Google ADK/Gemini"""
        if not self.initialized:
            raise ValueError("Agent not initialized. Call initialize() first.")
        
        try:
            logger.info(f"🤖 Generating {num_topics} interview topics (focus: {difficulty_focus})")
            
            # Build prompts
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(num_topics, difficulty_focus)
            
            # Configure generation parameters
            generation_config = GenerationConfig(
                temperature=0.8,  # Creative but not too random
                top_p=0.9,
                top_k=40,
                max_output_tokens=4000,  # Ensure enough space for all topics
            )
            
            # Generate content
            logger.info("🔄 Calling Gemini API...")
            
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = await asyncio.create_task(
                self._generate_with_retry(full_prompt, generation_config)
            )
            
            if not response:
                raise ValueError("Empty response from Gemini")
            
            # Parse the response
            topics = self._parse_response(response)
            
            # Validate topics
            validated_topics = self._validate_topics(topics, num_topics)
            
            logger.info(f"✅ Successfully generated {len(validated_topics)} interview topics")
            return validated_topics
            
        except Exception as e:
            logger.error(f"❌ Error generating topics: {e}")
            raise

    async def _generate_with_retry(self, prompt: str, config: GenerationConfig, max_retries: int = 3) -> str:
        """Generate content with retry logic"""
        for attempt in range(max_retries):
            try:
                logger.info(f"🔄 Generation attempt {attempt + 1}/{max_retries}")
                
                response = self.model.generate_content(
                    prompt,
                    generation_config=config
                )
                
                if response and response.text:
                    return response.text.strip()
                else:
                    raise ValueError("Empty response from model")
                    
            except Exception as e:
                logger.warning(f"⚠️ Generation attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse the JSON response from Gemini"""
        try:
            # Try to extract JSON array from response
            response = response.strip()
            
            # Look for JSON array pattern
            if response.startswith('[') and response.endswith(']'):
                topics = json.loads(response)
            else:
                # Try to find JSON array within the response
                import re
                json_match = re.search(r'\[[\s\S]*\]', response)
                if json_match:
                    topics = json.loads(json_match.group())
                else:
                    raise ValueError("No JSON array found in response")
            
            if not isinstance(topics, list):
                raise ValueError("Response is not a list")
                
            return topics
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing error: {e}")
            logger.error(f"Response was: {response[:500]}...")
            raise ValueError(f"Failed to parse JSON response: {e}")

    def _validate_topics(self, topics: List[Dict[str, Any]], expected_count: int) -> List[Dict[str, Any]]:
        """Validate and clean the generated topics"""
        validated_topics = []
        
        required_fields = ["title", "category", "difficulty", "description", "keyPoints", "duration", "technologies"]
        
        for i, topic in enumerate(topics):
            try:
                # Check required fields
                for field in required_fields:
                    if field not in topic:
                        logger.warning(f"⚠️ Topic {i+1} missing field '{field}', skipping")
                        continue
                
                # Validate field types and values
                if not isinstance(topic["title"], str) or len(topic["title"]) < 10:
                    logger.warning(f"⚠️ Topic {i+1} has invalid title, skipping")
                    continue
                
                if topic["category"] not in self.categories:
                    logger.warning(f"⚠️ Topic {i+1} has invalid category '{topic['category']}', skipping")
                    continue
                
                if topic["difficulty"] not in self.difficulty_levels:
                    logger.warning(f"⚠️ Topic {i+1} has invalid difficulty '{topic['difficulty']}', skipping")
                    continue
                
                if not isinstance(topic["keyPoints"], list) or len(topic["keyPoints"]) == 0:
                    logger.warning(f"⚠️ Topic {i+1} has invalid keyPoints, skipping")
                    continue
                
                if not isinstance(topic["duration"], (int, float)) or topic["duration"] < 15 or topic["duration"] > 120:
                    logger.warning(f"⚠️ Topic {i+1} has invalid duration, defaulting to 30 minutes")
                    topic["duration"] = 30
                
                if not isinstance(topic["technologies"], list):
                    logger.warning(f"⚠️ Topic {i+1} has invalid technologies, defaulting to empty list")
                    topic["technologies"] = []
                
                # Clean and format the topic
                cleaned_topic = {
                    "title": topic["title"].strip(),
                    "category": topic["category"],
                    "difficulty": topic["difficulty"], 
                    "description": topic["description"].strip(),
                    "keyPoints": [str(point).strip() for point in topic["keyPoints"][:5]],  # Max 5 points
                    "duration": int(topic["duration"]),
                    "technologies": [str(tech).strip() for tech in topic["technologies"][:6]]  # Max 6 technologies
                }
                
                validated_topics.append(cleaned_topic)
                
            except Exception as e:
                logger.warning(f"⚠️ Error validating topic {i+1}: {e}")
                continue
        
        logger.info(f"📊 Validated {len(validated_topics)}/{len(topics)} topics")
        
        if len(validated_topics) < expected_count * 0.7:  # At least 70% success rate
            raise ValueError(f"Too few valid topics generated: {len(validated_topics)}/{expected_count}")
        
        return validated_topics

    async def cleanup(self):
        """Clean up resources"""
        try:
            self.model = None
            self.initialized = False
            logger.info("✅ Google ADK agent cleaned up")
        except Exception as e:
            logger.warning(f"⚠️ Error during cleanup: {e}")