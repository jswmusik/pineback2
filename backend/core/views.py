import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import Document
from .ai_utils import generate_twin_content, get_twin_content, ai_assist_text


def workspace(request):
    # Fetch all top-level documents for the tree
    documents = Document.objects.filter(parent=None)
    return render(request, 'core/workspace.html', {'documents': documents})


def create_document(request):
    # Get parent_id from request if provided
    parent_id = request.POST.get('parent_id')
    parent = None
    if parent_id:
        parent = get_object_or_404(Document, id=parent_id)
    
    # Create a new blank document
    Document.objects.create(
        title="Untitled Document",
        content="",
        parent=parent
    )
    
    # After creating, return the UPDATED list of documents to the sidebar
    documents = Document.objects.filter(parent=None)
    return render(request, 'core/partials/document_list.html', {'documents': documents})


def get_document(request, doc_id):
    """Load a document into the editor and AI Twin panel."""
    doc = get_object_or_404(Document, id=doc_id)
    
    # Check if an AI Twin already exists
    ai_content = get_twin_content(doc)
    
    # Return both the editor AND the AI column with OOB swap
    return render(request, 'core/partials/doc_load_sync.html', {
        'doc': doc,
        'ai_content': ai_content
    })


def update_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    if request.method == "POST":
        doc.title = request.POST.get('title', doc.title)
        doc.content = request.POST.get('content', doc.content)
        doc.save()
    
    # Return just the sidebar with OOB swap to sync titles
    # without disrupting the editor while typing
    documents = Document.objects.filter(parent=None)
    return render(request, 'core/partials/sidebar_sync.html', {
        'doc': doc,
        'documents': documents
    })


def delete_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    doc.delete()
    
    # After deleting, return the updated sidebar list
    documents = Document.objects.filter(parent=None)
    return render(request, 'core/partials/document_list.html', {'documents': documents})


@require_POST
def reorder_documents(request):
    """Handle drag & drop reordering of documents.
    
    - If parent_id is null/None: reordering top-level parent documents
    - If parent_id is provided: reordering children within that parent
    """
    try:
        data = json.loads(request.body)
        order_list = data.get('order', [])
        parent_id = data.get('parent_id')  # Can be None for top-level docs
        
        for index, doc_id in enumerate(order_list):
            # Update order for each document
            # The parent relationship stays the same - we're only changing order
            Document.objects.filter(id=doc_id).update(order=index)
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@require_POST
def sync_ai_twin(request, doc_id):
    """
    Generate or refresh the AI Twin for a document.
    This calls Claude to transform human notes into structured markdown.
    """
    doc = get_object_or_404(Document, id=doc_id)
    
    # Generate the AI Twin content
    ai_content = generate_twin_content(doc)
    
    # Return just the AI column content
    return render(request, 'core/partials/ai_column.html', {
        'doc': doc,
        'ai_content': ai_content
    })


@require_POST
def ai_assist(request):
    """
    AI assistant endpoint for selected text.
    Accepts JSON with: selected_text, prompt, and optionally full_context
    Returns JSON with: response and optionally suggested_text
    """
    try:
        data = json.loads(request.body)
        selected_text = data.get('selected_text', '')
        user_prompt = data.get('prompt', '')
        full_context = data.get('full_context', '')
        
        if not selected_text or not user_prompt:
            return JsonResponse({
                'error': 'Both selected_text and prompt are required'
            }, status=400)
        
        result = ai_assist_text(selected_text, user_prompt, full_context)
        
        return JsonResponse(result)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
