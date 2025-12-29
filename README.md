# Pineback

An AI-powered SaaS workspace built with Django, HTMX, and Tiptap. Write your notes and let AI transform them into structured, LLM-optimized documentation.

![Django](https://img.shields.io/badge/Django-5.x-green)
![HTMX](https://img.shields.io/badge/HTMX-1.9-blue)
![Claude](https://img.shields.io/badge/AI-Claude%20Sonnet-purple)

## ✨ Features

- **📝 Rich Text Editor** - Tiptap-powered editor with formatting toolbar and bubble menu
- **🤖 AI Twin** - Automatically transform your notes into structured, LLM-optimized Markdown
- **✨ AI Assist** - Select text and ask AI to improve, explain, expand, or fix it
- **📁 Document Tree** - Hierarchical document organization with drag-and-drop reordering
- **🎨 Resizable Layout** - 3-column layout with draggable column dividers
- **💾 Auto-save** - Changes are automatically saved as you type
- **🔗 Link & Highlight** - Add links and highlights to your text
- **🌙 Dark Mode** - Beautiful dark theme designed for focus

## 🛠 Tech Stack

- **Backend**: Django 5.x
- **Frontend**: HTMX, Tailwind CSS, Tiptap Editor
- **AI**: Anthropic Claude API
- **Database**: SQLite (default), easily switchable to PostgreSQL
- **Drag & Drop**: SortableJS

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- An Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jswmusik/pineback2.git
   cd pineback2
   ```

2. **Set up virtual environment**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django anthropic python-dotenv
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp env.example.txt .env
   
   # Edit .env and add your API key
   nano .env  # or use your preferred editor
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📖 Usage

### Creating Documents
- Click **"+ New Document"** in the sidebar
- Click on a document to open it in the editor
- Use the **"+"** button on any document to create a sub-document

### AI Twin
- Write your notes in the editor
- Click **"Sync Twin"** in the right panel
- The AI will transform your notes into structured Markdown

### AI Assist
- Select any text in the editor
- Click the **lightbulb icon** in the bubble menu (or press `Ctrl+J`)
- Choose a quick action or type your own request
- Click **"Insert Response Below"** or **"Replace Text"**

### Resizing Columns
- Hover over the border between columns
- Drag to resize
- Double-click to reset to default width

## 📁 Project Structure

```
pineback/
├── backend/
│   ├── config/           # Django settings
│   ├── core/             # Main application
│   │   ├── models.py     # Document & AITwin models
│   │   ├── views.py      # View functions
│   │   ├── ai_utils.py   # AI integration
│   │   └── templates/    # HTML templates
│   └── manage.py
├── .gitignore
└── README.md
```

## 🔒 Security Notes

- **Never commit your `.env` file** - it contains your API keys
- The `.gitignore` is configured to exclude sensitive files
- Generate a new `DJANGO_SECRET_KEY` for production

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework
- [HTMX](https://htmx.org/) - High power tools for HTML
- [Tiptap](https://tiptap.dev/) - Headless rich text editor
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Anthropic](https://www.anthropic.com/) - Claude AI API

