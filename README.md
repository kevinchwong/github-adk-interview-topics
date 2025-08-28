# Software Interview Topics Generator

**GitHub Actions + Google ADK + MongoDB on Railway**

Generate high-quality software engineering interview discussion topics using GitHub Actions workflow automation, Google Agent Development Kit for AI generation, and MongoDB for data persistence on Railway.

## 🏗️ Architecture

```
GitHub Actions (Scheduler) 
    ↓
Google ADK Agent (Topic Generation)
    ↓
MongoDB on Railway (Storage)
```

- **Trigger**: GitHub Actions cron schedule (daily/weekly)
- **AI Generation**: Google ADK with Gemini for structured topic creation
- **Database**: MongoDB service deployed on Railway
- **Deployment**: Containerized Python application with ADK

## 🎯 What This Generates

**Software Interview Topics** including:
- Technical deep-dive questions
- System design scenarios  
- Coding challenge discussions
- Behavioral interview frameworks
- Technology trend conversations
- Architecture decision case studies

Each topic includes:
- `title` - Interview topic title
- `category` - Type (technical, behavioral, system design, etc.)
- `difficulty` - Junior, Mid-level, Senior, Staff
- `description` - Detailed scenario or question
- `keyPoints` - Main discussion areas
- `duration` - Estimated interview time
- `technologies` - Relevant tech stack
- `generatedAt` - Timestamp
- `runId` - Unique execution identifier

## 🚀 Quick Start

### 1. Fork & Setup Repository
```bash
git clone <your-fork>
cd github-adk-project
```

### 2. Railway Setup
1. Create Railway project
2. Add MongoDB service → copy connection string
3. Note: No additional Railway services needed (GitHub Actions handles execution)

### 3. Google ADK Setup
1. Get Google Cloud Project with Vertex AI enabled
2. Create service account with Vertex AI permissions
3. Download service account JSON

### 4. GitHub Secrets
Set these repository secrets:
```
MONGODB_URI=mongodb+srv://...
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account",...}
GEMINI_MODEL=gemini-pro
```

### 5. Enable GitHub Actions
- Actions will run automatically based on cron schedule
- Manual trigger available via workflow dispatch

## 📁 Project Structure

```
github-adk-project/
├── .github/
│   └── workflows/
│       └── generate-topics.yml      # GitHub Actions workflow
├── src/
│   ├── agents/
│   │   └── interview_agent.py       # Google ADK agent
│   ├── database/
│   │   └── mongodb_client.py        # MongoDB operations
│   └── main.py                      # Entry point
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container definition
└── README.md
```

## ⚙️ Configuration

### Interview Categories
Customize in `src/agents/interview_agent.py`:
- Technical coding challenges
- System design scenarios
- Behavioral questions
- Technology discussions
- Architecture decisions

### Difficulty Levels
- **Junior**: Entry-level positions (0-2 years)
- **Mid-level**: Experienced developers (3-5 years)
- **Senior**: Senior engineers (6+ years)
- **Staff**: Staff/Principal engineers (8+ years)

### Generation Schedule
Modify in `.github/workflows/generate-topics.yml`:
```yaml
schedule:
  - cron: '0 9 * * MON'  # Weekly Monday 9am UTC
```

## 🔧 Development

### Local Testing
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MONGODB_URI="mongodb+srv://..."
export GOOGLE_CLOUD_PROJECT="your-project"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

# Run locally
python src/main.py
```

### Docker Development
```bash
docker build -t interview-topics .
docker run --env-file .env interview-topics
```

## 📊 Database Schema

**Collection**: `interview_topics`

```javascript
{
  _id: ObjectId,
  runId: "2024-12-27-abc123",
  generatedAt: ISODate("2024-12-27T09:00:00Z"),
  model: "gemini-pro",
  topics: [
    {
      title: "Microservices vs Monolith Architecture Decision",
      category: "system_design",
      difficulty: "senior",
      description: "Discuss when to choose microservices over monolithic architecture...",
      keyPoints: ["Scalability", "Team structure", "Complexity trade-offs"],
      duration: 45,
      technologies: ["Docker", "Kubernetes", "API Gateway"]
    }
  ]
}
```

## 🎯 Usage Examples

### Query Recent Topics
```javascript
// Get last 10 generated topics
db.interview_topics.find().sort({generatedAt: -1}).limit(10)

// Filter by difficulty
db.interview_topics.find({"topics.difficulty": "senior"})

// Search by technology
db.interview_topics.find({"topics.technologies": "React"})
```

### GitHub Actions Manual Trigger
1. Go to Actions tab in GitHub repository
2. Select "Generate Interview Topics" workflow
3. Click "Run workflow" → "Run workflow"

## 🔐 Security

- **Service Account**: Minimal Vertex AI permissions only
- **MongoDB**: Railway-managed with connection string authentication
- **Secrets**: Stored in GitHub repository secrets
- **No exposed endpoints**: Workflow runs in GitHub's infrastructure

## 📈 Monitoring & Scaling

### Success Tracking
- GitHub Actions execution logs
- MongoDB document counts by runId
- Error alerts via GitHub notifications

### Scaling Options
- **Frequency**: Adjust cron schedule for more/fewer runs
- **Volume**: Increase `numTopics` parameter in agent
- **Variety**: Add more categories or difficulty levels
- **Multiple Workflows**: Separate workflows for different interview types

## 🚨 Troubleshooting

**Common Issues:**
- **Google ADK auth errors**: Verify service account JSON and project ID
- **MongoDB connection**: Check Railway connection string format
- **GitHub Actions timeout**: Increase timeout in workflow YAML
- **Rate limits**: Implement exponential backoff for Gemini API

## 💡 Extensions

**Future Enhancements:**
- Slack/Discord notifications for new topics
- Web dashboard for topic browsing
- Interview feedback collection integration
- Custom company-specific topics
- Multi-language topic generation

## 📚 References

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Railway MongoDB Setup](https://docs.railway.app/databases/mongodb)
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add comprehensive tests
4. Submit pull request with clear description

## 📄 License

MIT - See LICENSE file for details