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
    },
    {
        "title": "Unit Testing Strategy Implementation",
        "category": "testing_quality",
        "difficulty": "mid-level",
        "description": "Develop a comprehensive testing strategy for a new feature with complex business logic.",
        "keyPoints": ["Test coverage", "Test pyramids", "Mocking strategies", "CI/CD integration"],
        "duration": 35,
        "technologies": ["Jest", "Testing Library", "Cypress", "GitHub Actions"]
    },
    {
        "title": "CI/CD Pipeline Design",
        "category": "devops_deployment",
        "difficulty": "senior",
        "description": "Design and implement a robust CI/CD pipeline for a multi-service application.",
        "keyPoints": ["Pipeline stages", "Security scanning", "Blue-green deployment", "Rollback strategies"],
        "duration": 50,
        "technologies": ["Jenkins", "Docker", "AWS", "Terraform"]
    },
    {
        "title": "Debugging Production Memory Leaks",
        "category": "debugging_troubleshooting",
        "difficulty": "senior",
        "description": "Identify and resolve memory leaks in a production Node.js application.",
        "keyPoints": ["Memory profiling", "Heap analysis", "Monitoring setup", "Prevention strategies"],
        "duration": 45,
        "technologies": ["Node.js", "Memory Profiler", "New Relic", "Chrome DevTools"]
    },
    {
        "title": "Junior Developer Onboarding",
        "category": "behavioral",
        "difficulty": "mid-level",
        "description": "Describe your approach to onboarding and mentoring new junior developers.",
        "keyPoints": ["Learning plans", "Code reviews", "Pair programming", "Progress tracking"],
        "duration": 25,
        "technologies": ["Mentoring", "Documentation", "Code Review Tools"]
    },
    {
        "title": "Algorithm Complexity Analysis",
        "category": "technical_coding",
        "difficulty": "junior",
        "description": "Analyze the time and space complexity of common algorithms and data structures.",
        "keyPoints": ["Big O notation", "Trade-offs", "Optimization techniques", "Real-world applications"],
        "duration": 30,
        "technologies": ["Data Structures", "Algorithms", "Python", "JavaScript"]
    },
    {
        "title": "Cloud Migration Planning",
        "category": "system_design",
        "difficulty": "staff",
        "description": "Plan the migration of a legacy on-premises system to cloud infrastructure.",
        "keyPoints": ["Migration strategies", "Cost analysis", "Risk assessment", "Timeline planning"],
        "duration": 60,
        "technologies": ["AWS", "Azure", "Kubernetes", "Migration Tools"]
    },
    {
        "title": "Code Review Best Practices",
        "category": "testing_quality",
        "difficulty": "junior",
        "description": "Discuss effective code review practices and how to give constructive feedback.",
        "keyPoints": ["Review criteria", "Feedback delivery", "Security considerations", "Documentation"],
        "duration": 25,
        "technologies": ["Git", "GitHub", "Code Review Tools"]
    }
]