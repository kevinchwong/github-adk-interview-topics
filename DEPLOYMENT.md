# Deployment Guide: Software Interview Topics Generator

**GitHub Actions + Google ADK + Firebase Firestore**

## 🎯 Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  GitHub Actions │───▶│   Google ADK     │───▶│  Firebase       │
│  (Scheduler)    │    │   (AI Agent)     │    │  Firestore      │
│  - Cron trigger │    │  - Gemini model  │    │ - Data storage  │
│  - Secrets mgmt │    │  - Topic gen     │    │ - Query API     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Deployment (5 minutes)

### 1. Firebase Setup
```bash
# Create Firebase project
firebase projects:create your-interview-project

# Enable Firestore
firebase firestore:enable --project your-interview-project
```

### 2. Google Cloud Setup
```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Create service account
gcloud iam service-accounts create interview-topics-bot \
    --description="GitHub Actions bot for interview topics generation" \
    --display-name="Interview Topics Generator"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:interview-topics-bot@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create ./service-account-key.json \
    --iam-account=interview-topics-bot@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 3. GitHub Repository Setup
```bash
# Fork or create repository
git clone https://github.com/your-username/github-adk-interview-topics
cd github-adk-interview-topics

# Set GitHub secrets (in repo settings > Secrets and variables > Actions)
```

**Required Secrets:**
- `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Service account JSON content
- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
- `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Contents of service account JSON file

**Optional Secrets:**
- `GEMINI_MODEL`: `gemini-pro` (default)

### 4. Test Deployment
```bash
# Manual trigger from GitHub Actions tab
# Or wait for scheduled Monday 9am UTC run
```

## 📋 Detailed Setup Instructions

### Firebase Firestore Configuration

1. **Create Firebase Project**
   ```bash
   # Via Firebase CLI
   firebase projects:create your-interview-project
   firebase use your-interview-project
   ```

2. **Enable Firestore Database**
   ```bash
   # Enable Firestore in native mode
   firebase firestore:enable --project your-interview-project
   ```

3. **Create Service Account**
   ```bash
   # Create service account with Firestore permissions
   gcloud iam service-accounts create interview-bot --project your-interview-project
   gcloud projects add-iam-policy-binding your-interview-project \
     --member="serviceAccount:interview-bot@your-interview-project.iam.gserviceaccount.com" \
     --role="roles/datastore.user"
   ```

4. **Test Connection** (optional)
   ```bash
   # Test via Python
   python src/database/firebase_client.py
   ```

### Google Cloud Platform Setup

1. **Enable Required APIs**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable compute.googleapis.com
   ```

2. **Create Service Account with Minimal Permissions**
   ```bash
   # Create service account
   gcloud iam service-accounts create interview-topics-generator \
       --description="AI agent for generating interview topics" \
       --display-name="Interview Topics Generator"

   # Grant minimal required permissions
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
       --member="serviceAccount:interview-topics-generator@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/aiplatform.user"

   # Create service account key
   gcloud iam service-accounts keys create ./gcp-service-account.json \
       --iam-account=interview-topics-generator@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

3. **Verify Vertex AI Access**
   ```bash
   # Test authentication
   export GOOGLE_APPLICATION_CREDENTIALS="./gcp-service-account.json"
   gcloud auth application-default print-access-token
   ```

### GitHub Repository Configuration

1. **Repository Secrets** (Settings → Secrets and variables → Actions)
   
   | Secret Name | Value | Example |
   |-------------|-------|---------|
   | `MONGODB_URI` | Railway connection string | `mongodb+srv://mongo:abc123@...` |
   | `GOOGLE_CLOUD_PROJECT` | GCP project ID | `my-interview-project-123456` |
   | `GOOGLE_APPLICATION_CREDENTIALS_JSON` | Service account JSON content | `{"type":"service_account",...}` |

2. **Optional Configuration Secrets**
   
   | Secret Name | Default | Options |
   |-------------|---------|---------|
   | `GEMINI_MODEL` | `gemini-pro` | `gemini-pro`, `gemini-pro-vision` |

3. **Repository Variables** (optional, for default behavior)
   
   | Variable Name | Default | Description |
   |---------------|---------|-------------|
   | `DEFAULT_NUM_TOPICS` | `15` | Number of topics per generation |
   | `DEFAULT_DIFFICULTY` | `mixed` | `mixed`, `junior`, `mid-level`, `senior`, `staff` |

### Workflow Configuration

1. **Schedule Customization** (`.github/workflows/generate-topics.yml`)
   ```yaml
   schedule:
     - cron: '0 9 * * MON'  # Monday 9am UTC
     # Other examples:
     # - cron: '0 9 * * *'    # Daily 9am UTC  
     # - cron: '0 9 * * 1,3,5' # Mon, Wed, Fri 9am UTC
   ```

2. **Manual Trigger Parameters**
   - `num_topics`: Number of topics to generate (default: 15)
   - `difficulty_focus`: Focus level (`mixed`, `junior`, `mid-level`, `senior`, `staff`)

3. **Timeout Configuration**
   ```yaml
   jobs:
     generate-interview-topics:
       timeout-minutes: 15  # Adjust based on topic count
   ```

## 🔧 Advanced Configuration

### Custom Topic Categories

Edit `src/agents/interview_agent.py`:
```python
self.categories = {
    "technical_coding": "Coding challenges, algorithms, data structures",
    "system_design": "Architecture decisions, scalability, distributed systems",
    "custom_domain": "Your custom category description",
    # Add more categories
}
```

### MongoDB Optimization

1. **Indexes for Performance**
   ```javascript
   // Auto-created by the application
   db.topics.createIndex({"runId": 1}, {unique: true})
   db.topics.createIndex({"generatedAt": -1})
   db.topics.createIndex({"topics.category": 1, "topics.difficulty": 1})
   ```

2. **Query Examples**
   ```javascript
   // Get recent topics
   db.topics.find().sort({generatedAt: -1}).limit(5)
   
   // Filter by difficulty
   db.topics.find({"topics.difficulty": "senior"})
   
   // Search by technology
   db.topics.find({"topics.technologies": {$in: ["React", "Node.js"]}})
   ```

### Cost Optimization

1. **Vertex AI Pricing**
   - Gemini Pro: ~$0.0005 per 1k input tokens
   - Expected cost per run: $0.05-0.20
   - Monthly cost (4 runs): $0.20-0.80

2. **Railway Pricing**
   - MongoDB: $5/month for starter plan
   - No additional costs for GitHub Actions integration

3. **Optimization Strategies**
   ```yaml
   # Reduce frequency
   schedule:
     - cron: '0 9 * * 1,15'  # Twice monthly
   
   # Reduce topic count
   NUM_TOPICS: '10'
   ```

## 🔐 Security Best Practices

### Secret Management
- **Never commit service account JSON files**
- **Use GitHub repository secrets for sensitive data**
- **Rotate service account keys quarterly**
- **Use minimal IAM permissions**

### Firestore Security
- **Google manages security by default**
- **Use service account authentication**
- **Configure Firestore security rules**
- **Monitor access logs in Google Cloud Console**

### Runtime Security
```dockerfile
# Container runs as non-root user
USER appuser

# Minimal dependencies
FROM python:3.11-slim
```

## 📊 Monitoring & Troubleshooting

### Success Verification

1. **GitHub Actions Logs**
   - Check workflow execution in "Actions" tab
   - Look for "Successfully generated X interview topics"

2. **Firestore Verification**
   ```bash
   # Test connection
   python src/database/firebase_client.py
   
   # Or check via Firebase Console
   # Visit: https://console.firebase.google.com/project/YOUR_PROJECT/firestore
   ```

### Common Issues & Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Google Auth Error** | `401 Unauthorized` | Verify service account JSON and project ID |
| **Firestore Connection** | `Connection timeout` | Check service account permissions and project ID |
| **Workflow Timeout** | Job cancelled after 15min | Reduce `NUM_TOPICS` or increase timeout |
| **Topic Generation Failed** | Empty topics array | Check Gemini API quotas and model availability |
| **Duplicate Run ID** | Firestore insert error | Check for concurrent executions |

### Debug Mode

Enable verbose logging in GitHub Actions:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

## 🚀 Production Deployment Checklist

- [ ] Firebase Firestore database enabled and accessible
- [ ] Google Cloud project with Vertex AI enabled
- [ ] Service account created with minimal permissions
- [ ] GitHub repository secrets configured
- [ ] Workflow tested with manual trigger
- [ ] Firestore security rules configured
- [ ] Cost monitoring enabled
- [ ] Error notifications configured
- [ ] Documentation updated for team

## 📈 Scaling & Extensions

### Horizontal Scaling
- **Multiple repositories**: Deploy to different GitHub repos for different interview types
- **Team-specific topics**: Use different GCP projects for different teams
- **Regional deployment**: Deploy to multiple Railway regions

### Feature Extensions
- **Slack notifications**: Add webhook to notify team of new topics
- **Web dashboard**: Build simple UI to browse generated topics  
- **Custom models**: Switch to fine-tuned models for company-specific topics
- **Feedback loop**: Collect interview feedback to improve generation

### Performance Optimization
- **Batch processing**: Generate topics for multiple weeks at once
- **Caching**: Store common topic templates in Firestore
- **Parallel execution**: Generate different categories concurrently
- **Firestore indexes**: Optimize queries with composite indexes

---

**🎯 Ready to deploy?** Start with the [Quick Deployment](#-quick-deployment-5-minutes) section above!