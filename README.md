# OpenManus AI Assistant 🤖

A multi-model AI assistant with GUI, supporting OpenAI, Gemini, Claude, DeepSeek, Groq, and Perplexity. Docker-containerized for easy deployment.

![OpenManus Screenshot](https://via.placeholder.com/800x400?text=OpenManus+GUI+Demo)

## Features ✨
- 🧠 **Multiple AI Models**: Switch between 6+ AI providers
- 📁 **File Upload Support**: Process PDFs, Word docs, images, and archives
- ⚙️ **GUI Settings**: Manage API keys and models through web interface
- 🐳 **Docker Containerization**: One-command setup and deployment
- 🔒 **Secure Configuration**: Environment-based API key management

## Prerequisites 📋
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)
- API keys from at least one provider:
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Gemini](https://aistudio.google.com/app/apikey)
  - [Claude](https://console.anthropic.com/settings/keys)
  - [DeepSeek](https://platform.deepseek.com/api-keys)
  - [Groq](https://console.groq.com/keys)
  - [Perplexity](https://docs.perplexity.ai/docs/getting-started)

## Installation 🛠️
```bash
# 1. Clone repository
git clone https://github.com/yourusername/OpenManus.git
cd OpenManus

# 2. Create configuration file
cp .env.example .env

# 3. Edit .env with your API keys
nano .env  # or open in text editor

# 4. Make script executable
chmod +x run.sh

# 5. Start the application
./run.sh