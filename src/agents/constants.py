"""
Shared constants for interview topic generation
"""

# Interview categories and their focus areas
CATEGORIES = {
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
DIFFICULTY_LEVELS = {
    "junior": "Entry-level (0-2 years experience)",
    "mid-level": "Experienced developer (3-5 years experience)", 
    "senior": "Senior engineer (6+ years experience)",
    "staff": "Staff/Principal engineer (8+ years experience)"
}

# Sample topics for mock generation
SAMPLE_TOPICS = [
    {
        "title": "Microservices vs Monolith Architecture Decision",
        "category": "system_design",
        "difficulty": "senior",
        "description": "Discuss architectural trade-offs when migrating a monolithic e-commerce platform to microservices.",
        "keyPoints": ["Scalability considerations", "Data consistency", "Team structure", "Deployment complexity"],
        "duration": 45,
        "technologies": ["Docker", "Kubernetes", "API Gateway", "Service Mesh"]
    },
    {
        "title": "Database Performance Optimization",
        "category": "technical_coding",
        "difficulty": "senior",
        "description": "Analyze and optimize slow-performing queries in a high-traffic application database.",
        "keyPoints": ["Index optimization", "Query analysis", "Caching strategies", "Database scaling"],
        "duration": 40,
        "technologies": ["PostgreSQL", "Redis", "Monitoring", "SQL"]
    },
    {
        "title": "Leading a Cross-Functional Team",
        "category": "behavioral",
        "difficulty": "staff",
        "description": "Share experiences leading a diverse team through a complex technical migration project.",
        "keyPoints": ["Communication strategies", "Stakeholder management", "Conflict resolution", "Technical mentoring"],
        "duration": 35,
        "technologies": ["Project Management", "Leadership", "Mentoring"]
    },
    {
        "title": "React Performance Optimization",
        "category": "technology_deep_dive", 
        "difficulty": "mid-level",
        "description": "Identify and fix performance bottlenecks in a React application with heavy data rendering.",
        "keyPoints": ["React profiling", "Memoization", "Virtual scrolling", "Bundle optimization"],
        "duration": 30,
        "technologies": ["React", "JavaScript", "Webpack", "Performance Tools"]
    },
    {
        "title": "API Design Best Practices",
        "category": "architecture_decisions",
        "difficulty": "senior",
        "description": "Design a REST API for a multi-tenant SaaS application with complex authorization requirements.",
        "keyPoints": ["RESTful design", "Authentication", "Rate limiting", "Versioning strategies"],
        "duration": 40,
        "technologies": ["REST", "OAuth", "API Gateway", "OpenAPI"]
    }
]