#!/usr/bin/env python3
"""
FastOpp
An Opinionated FastAPI Starter Kit
"""
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from admin.setup import setup_admin

app = FastAPI(
    title="Welcome to FastOpp",
    description="An Opinionated FastAPI Starter Kit",
    version="1.0.0"
)

"""Configure authentication/session for SQLAdmin login"""
# Load environment variables and secret key
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")

# Enable sessions (required by sqladmin authentication backend)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Mount SQLAdmin with authentication backend
setup_admin(app, SECRET_KEY)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Show a simple page with demo restoration instructions"""

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastOpp</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .content {
            padding: 40px;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #3B82F6;
            border-bottom: 2px solid #E5E7EB;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .code-block {
            background: #F3F4F6;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            line-height: 1.5;
            overflow-x: auto;
        }
        .command {
            background: #1F2937;
            color: #F9FAFB;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
        }
        .step {
            background: #F0F9FF;
            border-left: 4px solid #3B82F6;
            padding: 15px;
            margin: 15px 0;
            border-radius: 0 8px 8px 0;
        }
        .step h3 {
            margin: 0 0 10px 0;
            color: #1E40AF;
        }
        .demo-pages {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .demo-card {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }
        .demo-card h4 {
            margin: 0 0 10px 0;
            color: #3B82F6;
        }
        .demo-card p {
            margin: 0;
            color: #64748B;
            font-size: 0.9rem;
        }
        .warning {
            background: #FEF3C7;
            border: 1px solid #F59E0B;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        .warning h4 {
            margin: 0 0 10px 0;
            color: #92400E;
        }
        .success {
            background: #D1FAE5;
            border: 1px solid #10B981;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        .success h4 {
            margin: 0 0 10px 0;
            color: #065F46;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Welcome to FastOpp</h1>
            <p>An Opinionated FastAPI Starter Kit</p>
        </div>

        <div class="content">
            <div class="section">
                <h2>📋 Overview</h2>
                <p>This is a minimal FastAPI application. To restore the full demo with all features,
                use the <code>oppman.py</code> management tool.</p>
            </div>

            <div class="section">
                <h2>🛠️ Quick Restore Commands</h2>

                <div class="step">
                    <h3>Step 1: Restore Demo Files</h3>
                    <div class="command">uv run python oppman.py demo restore</div>
                    <p>This command restores all demo files from the <code>demo_assets</code> backup.</p>
                </div>

                <div class="step">
                    <h3>Step 2: Populate Database</h3>
                    <div class="command">uv run python oppman.py init</div>
                    <p>This initializes the database with sample data including users, products, webinars,
                    and registrants.</p>
                </div>

                <div class="step">
                    <h3>Step 3: Start the Application</h3>
                    <div class="command">uv run python oppman.py runserver</div>
                    <p>This starts the development server with all demo features enabled.</p>
                </div>
            </div>



            <div class="section">
                <h2>🔐 Admin Panel</h2>
                <p>You can log in to the admin panel at:</p>
                <div class="code-block">
http://localhost:8000/admin/
                </div>

                <div class="step">
                    <h3>Create a Database</h3>
                    <div class="command">uv run python oppman.py db</div>
                    <p>Initialize the database before accessing any data</p>
                </div>
                
                <div class="step">
                    <h3>Create an Admin User</h3>
                    <div class="command">uv run python oppman.py superuser</div>
                    <p>Run this before logging in to create your first admin account.</p>
                </div>

                <div class="step">
                    <h3>Optional: Create Sample Users and Products</h3>
                    <div class="command">uv run python oppman.py users</div>
                    <div class="command">uv run python oppman.py products</div>
                </div>
            </div>

            <div class="section">
                <h2>📚 Help</h2>

                <div class="command">uv run python oppman.py help</div>
                <p>Shows detailed help for all available commands.</p>

                <h3>Default Credentials</h3>
                <div class="code-block">
Superuser: admin@example.com / admin123
<br>
Test Users: test123 (for all test users)

                </div>
            </div>

            <div class="warning">
                <h4>⚠️ Important Notes</h4>
                <ul>
                    <li>Make sure you have <code>uv</code> installed and configured</li>
                    <li>The demo requires an OpenRouter API key for AI chat functionality</li>
                    <li>Sample photos are downloaded automatically during initialization</li>
                    <li>Database is SQLite by default (test.db)</li>
                </ul>
            </div>

            <div class="success">
                <h4>✅ Ready to Go!</h4>
                <p>Once you've restored the demo, you'll have a fully functional FastAPI application with:</p>
                <ul>
                    <li>Modern web technologies (Tailwind CSS, DaisyUI, Alpine.js, HTMX)</li>
                    <li>AI chat integration with Llama 3.3 70B</li>
                    <li>Interactive dashboards with Chart.js</li>
                    <li>File upload functionality</li>
                    <li>User authentication and authorization</li>
                    <li>Admin panel with CRUD operations</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
    """

    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Minimal FastAPI app is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
