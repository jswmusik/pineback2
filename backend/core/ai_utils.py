"""
AI Twin Generation Utilities

This module handles the transformation of human-written notes into
AI-optimized, structured Markdown that LLMs can digest instantly.
"""

import os
import anthropic
from .models import AITwin

# API Key - Load from environment variable
# Set via: export ANTHROPIC_API_KEY="your-key" or in .env file
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    import warnings
    warnings.warn("ANTHROPIC_API_KEY not set. AI features will not work.")
    client = None
else:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_twin_content(document):
    """
    Takes human text and transforms it into an AI-optimized Markdown twin.
    
    The AI Twin is a highly structured version of your notes that:
    - Strips away conversational fluff
    - Organizes information into clear sections
    - Extracts technical requirements as bullet points
    - Represents logic as pseudocode when applicable
    
    Args:
        document: A Document model instance
        
    Returns:
        str: The AI-generated markdown content
    """
    
    # Check if API client is available
    if client is None:
        return "## ⚠️ API Key Not Configured\n\nPlease set the `ANTHROPIC_API_KEY` environment variable to enable AI features."
    
    # Strip HTML tags from content for cleaner processing
    import re
    clean_content = re.sub(r'<[^>]+>', '', document.content)
    
    prompt = f"""You are a Senior Software Architect and Technical Writer.

Transform the following human-written project notes into a high-density, 
structured Markdown document optimized for an LLM to understand a codebase or project.

HUMAN NOTES:
---
Title: {document.title}

Content:
{clean_content}
---

OUTPUT REQUIREMENTS:
1. Use clear hierarchical headers:
   - ## Technical Context (what this is about)
   - ## Core Requirements (extracted as bullet points)
   - ## Data Structures (if any entities/models are mentioned)
   - ## Logic Flow (pseudocode if any processes are described)
   - ## Dependencies & Integrations (external systems, APIs)
   - ## Open Questions (uncertainties or TODOs)

2. Extract ALL technical requirements into concise bullet points
3. If any logic or workflow is mentioned, represent it in pseudocode
4. Identify and list any data entities, their attributes, and relationships
5. Keep it CONCISE - no conversational filler, no repetition
6. Use code blocks for any technical specifications
7. If the content is too brief, note what information is missing

IMPORTANT: Output ONLY the structured markdown. No preamble or explanation."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",  # Latest Claude Sonnet model
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        ai_content = message.content[0].text
        
        # Save or update the Twin
        twin, created = AITwin.objects.get_or_create(document=document)
        twin.content_ai = ai_content
        twin.save()
        
        return ai_content
        
    except Exception as e:
        # Return error message that can be displayed in UI
        error_msg = f"## ⚠️ AI Generation Error\n\nFailed to generate AI Twin:\n\n```\n{str(e)}\n```\n\nPlease check your API key and try again."
        return error_msg


def get_twin_content(document):
    """
    Retrieves existing AI Twin content for a document.
    
    Args:
        document: A Document model instance
        
    Returns:
        str or None: The AI content if it exists, None otherwise
    """
    try:
        return document.twin.content_ai
    except AITwin.DoesNotExist:
        return None


def ai_assist_text(selected_text, user_prompt, full_context=""):
    """
    AI assistant for selected text - can answer questions or suggest modifications.
    
    Args:
        selected_text: The text the user has selected
        user_prompt: What the user wants to do with the text
        full_context: Optional full document context for better understanding
        
    Returns:
        dict: Contains 'response' (AI answer) and optionally 'suggested_text' (replacement)
    """
    import re
    
    # Clean HTML from selected text
    clean_selected = re.sub(r'<[^>]+>', '', selected_text)
    clean_context = re.sub(r'<[^>]+>', '', full_context) if full_context else ""
    
    system_prompt = """You are an intelligent writing assistant embedded in a document editor.
The user has selected some text and is asking you to help with it.

Your capabilities:
1. Answer questions about the selected text
2. Suggest improvements, rewrites, or edits
3. Expand on ideas
4. Fix grammar, spelling, or style issues
5. Translate or change tone
6. Summarize or simplify

CRITICAL RESPONSE FORMAT:
- If the user asks a QUESTION about the text (like "what does this mean?"), just provide a helpful answer.
- If the user wants you to MODIFY, IMPROVE, FIX, REWRITE, EXPAND, SHORTEN, or CHANGE the text in ANY way, you MUST:
  1. First give a brief explanation (1-2 sentences max) of what you changed
  2. Then provide the COMPLETE replacement text wrapped EXACTLY like this:
     <suggested_text>your replacement text here</suggested_text>

IMPORTANT: 
- The <suggested_text> tags are REQUIRED for any modification request
- Put the ENTIRE replacement text inside the tags, not just the changed parts
- Do not include any formatting or extra text inside the tags, just the plain replacement text
- Keep explanations brief - the user wants to see the result quickly"""

    user_message = f"""SELECTED TEXT:
---
{clean_selected}
---

"""
    
    if clean_context:
        user_message += f"""FULL DOCUMENT CONTEXT:
---
{clean_context}
---

"""
    
    user_message += f"""USER REQUEST: {user_prompt}"""
    
    # Check if API client is available
    if client is None:
        return {
            'response': "API key not configured. Please set the ANTHROPIC_API_KEY environment variable.",
            'suggested_text': None
        }
    
    # Check if this is a modification request
    modification_keywords = ['improve', 'fix', 'rewrite', 'change', 'make', 'shorten', 'expand', 
                            'grammar', 'spelling', 'professional', 'clearer', 'concise', 'better',
                            'translate', 'simplify', 'formal', 'casual', 'correct', 'edit']
    is_modification_request = any(kw in user_prompt.lower() for kw in modification_keywords)

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        response_text = message.content[0].text
        
        # Extract suggested text if present with tags
        suggested_text = None
        match = re.search(r'<suggested_text>(.*?)</suggested_text>', response_text, re.DOTALL)
        if match:
            suggested_text = match.group(1).strip()
            # Remove the tags from the response for cleaner display
            response_text = re.sub(r'<suggested_text>.*?</suggested_text>', '', response_text, flags=re.DOTALL).strip()
        
        # If no tags found but it's a modification request, make a follow-up call to extract
        if not suggested_text and is_modification_request:
            # Ask Claude to extract just the replacement text
            extraction_message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=512,
                messages=[
                    {"role": "user", "content": f"""Based on this AI response about modifying text, extract ONLY the suggested replacement text.

ORIGINAL TEXT: {clean_selected}

AI RESPONSE: {response_text}

Return ONLY the replacement text that should replace the original. No explanation, no quotes, just the raw replacement text. If there's no clear replacement suggested, return exactly: NO_REPLACEMENT"""}
                ]
            )
            
            extracted = extraction_message.content[0].text.strip()
            if extracted and extracted != "NO_REPLACEMENT" and len(extracted) > 3:
                suggested_text = extracted
        
        return {
            'response': response_text,
            'suggested_text': suggested_text
        }
        
    except Exception as e:
        return {
            'response': f"Error: {str(e)}",
            'suggested_text': None
        }
