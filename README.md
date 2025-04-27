# LinkSnap - Bookmark Management System
 LinkSnap is a web application designed to help you organize, save, and manage your favorite websites seamlessly. With intuitive features, you can easily categorize your bookmarks, access them quickly, and share your favorites with friends.


## Features

- **User Authentication**: Secure registration and login system
- **Bookmark Management**: Create, edit, and delete bookmarks
- **Tags**: Organize bookmarks with customizable tags
- **Favorites**: Mark important bookmarks as favorites
- **Search & Filter**: Find bookmarks easily with search and tag filtering
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark/Light Theme**: Toggle between dark and light modes
- **Profile Management**: User profile customization

## Tech Stack

- Django 5.0
- Python 3.10+
- Bootstrap 5.3
- Font Awesome 6.0
- SQLite Database

## Local Development

1. Clone the repository in Replit
2. Install dependencies using Poetry (automatically handled by Replit)
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Start the development server:
   ```
   python manage.py runserver 0.0.0.0:3000
   ```

## Project Structure

```
├── bookmarks/              # Main application directory
│   ├── migrations/        # Database migrations
│   ├── templates/        # HTML templates
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── urls.py          # URL routing
│   └── forms.py         # Form definitions
├── static/               # Static files (CSS, JS)
└── django_project/      # Project configuration
```

## Models

- **Bookmark**: Stores bookmark information including URL, title, description, and image
- **Tag**: Manages categorization of bookmarks

## Features in Detail

### Bookmark Management
- Add new bookmarks with title, URL, description, and image
- Edit existing bookmarks
- Delete unwanted bookmarks
- Mark/unmark bookmarks as favorites

### Tag System
- Create and assign tags to bookmarks
- Filter bookmarks by tags
- Manage tags through the admin interface

### User Features
- User registration and authentication
- Profile customization
- Password reset functionality
- Theme preference management

## Security

- CSRF protection enabled
- Secure password handling
- User authentication required for sensitive operations
- Django's built-in security features
