
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Bookmark, Tag
from django.core.paginator import Paginator
from .forms import UserProfileForm

def landing(request):
    """Landing page view for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'bookmarks/landing.html')

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'bookmarks/register.html', {'form': form})

@login_required
def dashboard(request):
    """Main dashboard view to display user's bookmarks"""
    bookmarks = Bookmark.objects.filter(user=request.user)
    
    # Filter by search query
    query = request.GET.get('q')
    if query:
        # Search in title, description, URL, and tags
        bookmarks = bookmarks.filter(
            models.Q(title__icontains=query) | 
            models.Q(description__icontains=query) | 
            models.Q(url__icontains=query) |
            models.Q(tags__name__icontains=query)
        ).distinct()
    
    # Filter by tag
    tag = request.GET.get('tag')
    if tag:
        bookmarks = bookmarks.filter(tags__name=tag)
    
    # Filter by favorites
    if request.GET.get('favorites'):
        bookmarks = bookmarks.filter(is_favorite=True)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    bookmarks = bookmarks.order_by(sort)
    
    # Pagination
    paginator = Paginator(bookmarks, 9)  # 9 bookmarks per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get all user's tags for the sidebar
    tags = Tag.objects.filter(bookmarks__user=request.user).distinct()
    
    context = {
        'page_obj': page_obj,
        'tags': tags,
    }
    
    return render(request, 'bookmarks/dashboard.html', context)

@login_required
def bookmark_create(request):
    """Create a new bookmark"""
    if request.method == 'POST':
        # Process form data
        title = request.POST.get('title')
        url = request.POST.get('url')
        description = request.POST.get('description')
        image_url = request.POST.get('image_url')
        
        # Create bookmark
        bookmark = Bookmark.objects.create(
            user=request.user,
            title=title,
            url=url,
            description=description,
            image_url=image_url
        )
        
        # Process tags
        tags = request.POST.get('tags', '').split(',')
        for tag_name in tags:
            if tag_name.strip():
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                bookmark.tags.add(tag)
        
        messages.success(request, 'Bookmark created successfully!')
        return redirect('dashboard')
    
    return render(request, 'bookmarks/bookmark_form.html', {'action': 'Add'})

@login_required
def bookmark_update(request, pk):
    """Update an existing bookmark"""
    bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Process form data
        bookmark.title = request.POST.get('title')
        bookmark.url = request.POST.get('url')
        bookmark.description = request.POST.get('description')
        bookmark.image_url = request.POST.get('image_url')
        bookmark.save()
        
        # Process tags
        bookmark.tags.clear()
        tags = request.POST.get('tags', '').split(',')
        for tag_name in tags:
            if tag_name.strip():
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                bookmark.tags.add(tag)
        
        messages.success(request, 'Bookmark updated successfully!')
        return redirect('dashboard')
    
    context = {
        'bookmark': bookmark,
        'action': 'Edit',
        'tags': ','.join([tag.name for tag in bookmark.tags.all()])
    }
    
    return render(request, 'bookmarks/bookmark_form.html', context)

@login_required
def bookmark_delete(request, pk):
    """Delete a bookmark"""
    bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
    
    if request.method == 'POST':
        bookmark.delete()
        messages.success(request, 'Bookmark deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'bookmarks/bookmark_confirm_delete.html', {'bookmark': bookmark})

@login_required
def toggle_favorite(request, pk):
    """Toggle favorite status of a bookmark"""
    if request.method == 'POST':
        bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
        bookmark.is_favorite = not bookmark.is_favorite
        bookmark.save()
        
        if bookmark.is_favorite:
            messages.success(request, 'Added to favorites!')
        else:
            messages.success(request, 'Removed from favorites!')
    
    # Redirect back to the page user came from, or dashboard if not available
    referring_page = request.META.get('HTTP_REFERER')
    if referring_page:
        return redirect(referring_page)
    return redirect('dashboard')

@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'bookmarks/profile_edit.html', {'form': form})

@login_required
def profile(request):
    """View user profile"""
    bookmark_count = Bookmark.objects.filter(user=request.user).count()
    favorite_count = Bookmark.objects.filter(user=request.user, is_favorite=True).count()
    tag_count = Tag.objects.filter(bookmarks__user=request.user).distinct().count()
    
    context = {
        'user': request.user,
        'bookmark_count': bookmark_count,
        'favorite_count': favorite_count,
        'tag_count': tag_count
    }
    
    return render(request, 'bookmarks/profile.html', context)

def logout_view(request):
    """Custom logout view that supports GET request"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('landing')
