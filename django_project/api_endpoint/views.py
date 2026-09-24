from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from blog.models import Post
from django.contrib.auth.models import User


@csrf_exempt
def item_list(request):
    if request.method == 'GET':
        return JsonResponse({
            "message": "Hello from pure Django!",
            "status": "success"
        }, status=200)


def api_blog_collection(request):

    # Handle Read
    if request.method == 'GET':
        blogs = Post.objects.all()

        # convert queryset into a list of dictionaries
        data = [
            {
                'title': blog.title,
                'content': blog.content,
                # Convert datetime object to ISO string
                'date_posted': blog.date_posted.isoformat() if blog.date_posted else None,
                # Extract the string username instead of passing the whole User object
                'author': blog.author.username if blog.author else None,
            }

            for blog in blogs
        ]

        # safe=False allows serializing Python list objects (instead of standard dicts)
        return JsonResponse(data, safe=False, status=200)

    # HANDLE CREATE
    elif request.method == 'POST':
        try:
            # 1. Parse incoming JSON request body
            body = json.loads(request.body)

            # 2. Extract fields from payload
            title = body.get('title')
            content = body.get('content')

            # Simple validation for required fields
            if not title or not content:
                return JsonResponse({'error': 'Title and content are required'}, status=400)

            # Assign an author (e.g., logged-in user or first available user for testing)
            author = request.user if request.user.is_authenticated else User.objects.first()

            # 3. Create and save the Post instance
            new_post = Post.objects.create(
                title=title,
                content=content,
                author=author
            )

            # 4. Format the new object into a response dictionary
            response_data = {
                'id': new_post.id,
                'title': new_post.title,
                'content': new_post.content,
                'date_posted': new_post.date_posted.isoformat() if hasattr(new_post, 'date_posted') and new_post.date_posted else None,
                'author': new_post.author.username if new_post.author else None
            }

            # Return new post with 201 Created status
            return JsonResponse(response_data, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    # Return 405 Method Not Allowed for unhandled methods for now
    return JsonResponse({'error': 'Method not allowed'}, status=405)
