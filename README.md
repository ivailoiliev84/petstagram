# 🐾 Petstagram

**A full-stack Django portfolio project for a pet-focused social platform, with AI-assisted content moderation.**

Petstagram is a server-rendered web application where registered users can manage profiles, publish photos, interact with posts, and discuss pet-related content. It is built end to end with **Python/Django on the backend** and **Django Templates, HTML, CSS, Bootstrap and a small amount of vanilla JavaScript on the frontend**. It does not depend on a separate SPA framework such as React or Vue.

> **Project status:** Actively developed portfolio project. The features below are based on the source code reviewed on 6 November 2026. Planned capabilities are deliberately distinguished from implemented ones.

## Purpose and engineering goals

The goal is not to reproduce a large commercial social network. Petstagram demonstrates how to design and implement a coherent full-stack product with particular emphasis on:

- Django application structure and class-based views;
- data modelling, relationships and ORM query optimisation;
- custom authentication, user profiles and object ownership;
- forms, server-side validation and secure state-changing requests;
- external AI API integration and separation of application/service logic;
- responsive server-rendered UI without a frontend framework;
- operational fundamentals such as environment configuration, static assets and Gunicorn.

## Features implemented

### Accounts and profiles

- **Custom email-based user model:** `AppUser` derives from `AbstractBaseUser` and uses a custom `AppUserManager`.
- **Account registration, login and logout** using Django authentication and custom forms.
- **Profile model:** one-to-one `UserProfile` with personal information, description and profile picture.
- **Automatic profile creation** using a Django `post_save` signal.
- **Profile editing** and **password changing** through Django forms/views.
- **Cloudinary-backed profile picture field** (`CloudinaryField`).

### Gallery and social interactions

- Create, view, edit and delete posts with an image, title and description.
- Gallery ordered by creation time with **server-side pagination: six posts per page**.
- Post detail pages showing comments and aggregate counts.
- Create, edit and delete comments. New comments are created directly from the post detail page.
- Like/unlike and dislike/undislike interactions. Selecting one reaction removes the opposite reaction for that user and post.
- **Ownership checks** in post/comment edit and delete handlers, using `get_object_or_404(..., user=request.user)`.
- **POST + CSRF** for likes, dislikes and post/comment deletion.
- **Post/Redirect/Get** after successful creations/edits to avoid normal refresh resubmissions.

### AI moderation (currently implemented)

A moderation service in `gallery/services/moderation.py` integrates the OpenAI **`omni-moderation-latest`** model:

- Uploaded post images are checked before a post is saved.
- Post titles, descriptions and comment text are checked for prohibited content.
- Rejected content is attached to the relevant Django form field with `form.add_error()`, allowing validation feedback within the page.
- During editing, the service can moderate **only changed fields**, avoiding unnecessary calls for unchanged content.
- Image moderation additionally rejects images whose `sexual` score exceeds an application-defined threshold of `0.2`, even when the general `flagged` result is false.

This is a synchronous API integration in the request flow, **not** an asynchronous moderation pipeline. The threshold is an application decision, not a universal safety standard. Moderation does **not yet** verify whether an image contains an animal.

### Frontend and UX

- Server-side **Django Template Language**, template inheritance and partial includes.
- Responsive page layouts with **HTML5, custom CSS, Bootstrap 5 and Font Awesome**.
- Small **vanilla JavaScript** behaviour for the mobile navigation toggle and accessible `aria-expanded` state.
- Photo gallery cards, post details, profile pages, authentication forms and simple informational pages.
- Field-level validation and AI moderation feedback rendered in templates.
- Homepage, Explore and Contact pages; Explore uses Django's `cache_page` decorator with a **five-minute** timeout.

Some interface elements, such as the star display, are visual-only at this stage and are **not** a persisted rating system.

## Technical stack

| Area | Technologies |
| --- | --- |
| Language | Python |
| Web framework | Django 5.2.7 |
| UI | Django Templates, HTML5, CSS3, Bootstrap 5, Font Awesome, vanilla JavaScript |
| Database in current configuration | SQLite |
| Data access | Django ORM |
| AI integration | OpenAI Python SDK, `omni-moderation-latest` |
| Image/media integration | Django `ImageField`, Pillow, Cloudinary (`CloudinaryField` for profiles) |
| Static assets | Django staticfiles, WhiteNoise dependency |
| Application server | Gunicorn; WSGI entry point |
| Configuration | `python-dotenv` dependency and `.env`-loading startup script |

**Important:** PostgreSQL is not configured in the reviewed project. It would be inaccurate to list it as the current database. Likewise, the project does not presently use React, Vue, a REST API backend, Celery, Docker or an AI chatbot.

## Architecture and source structure

```text
petstagram-main/
├── accounts/                 # Custom user, profiles, forms, authentication and signals
├── gallery/
│   ├── models.py             # Post, PostComment, PostLike and PostDislike
│   ├── forms.py              # Post and comment ModelForms
│   ├── views.py              # Gallery, detail, CRUD and reaction views
│   ├── services/
│   │   └── moderation.py     # OpenAI image and text moderation
│   ├── templates/gallery/    # Server-rendered social pages
│   └── static/gallery/       # Gallery styles and assets
├── home/                     # Landing, Explore and Contact pages
├── core/                     # Project settings, URL routing, WSGI/ASGI
├── templates/                # Shared base/navigation/footer templates
├── static/                   # Shared frontend CSS
├── manage.py
├── requirements.txt
└── start.sh                  # Local Gunicorn startup workflow
```

### Data model relationships

- `AppUser` **1:1** `UserProfile`.
- `AppUser` **1:N** `Post`.
- `Post` **1:N** `PostComment`.
- `AppUser` **1:N** `PostComment`.
- `Post` **1:N** `PostLike` and `PostDislike`, each associated with a user.

Deleting a post cascades to related database rows through `on_delete=models.CASCADE`. Deletion of the **physical image file** is a separate concern and is not yet implemented end to end.

### ORM and request processing

`Gallery` uses `select_related('user', 'user__userprofile')` to load authors and their profiles together with posts, and `annotate(Count(..., distinct=True))` to calculate engagement counts. `PostDetails` similarly loads the post and its aggregate counts, then fetches comments with `select_related('user', 'user__userprofile')`.

Class-based Django views handle HTTP methods explicitly. Forms provide model binding and validation; the moderation service performs external policy checks; templates render form errors. Resource ownership is enforced server-side rather than relying solely on hidden interface buttons.

## Security and correctness considerations

Implemented safeguards include authenticated access (`LoginRequiredMixin`) for protected gallery actions, ownership filtering on post/comment editing and deletion, CSRF tokens for relevant POST forms, and server-side validation.

**This is not yet a production-hardened application.** Before public deployment:

- Remove **all hard-coded or exposed secrets**, rotate affected Django/Cloudinary credentials, configure settings via environment variables and check Git history for leaked values.
- Set `DEBUG=False`, restrict `ALLOWED_HOSTS`, and configure appropriate HTTPS/security settings.
- Review profile edit/detail permissions: the current `UserProfileEditView` fetches profiles by URL ID without an ownership filter.
- Review account logout behaviour: the current logout view handles GET; a POST form would be more suitable for a state-changing action.
- Review the failed-profile-edit response and replace the invalid `redirect(request, template, ...)` pattern with a normal `render(...)` preserving form errors.
- Add database uniqueness constraints for user/post reactions and test concurrent requests.
- Handle OpenAI API timeouts/unavailability explicitly and determine a fail-closed moderation policy.
- Implement reliable storage cleanup for replaced and deleted images, with appropriate error handling.
- Verify static/media storage settings and media serving in the actual deployment environment.

## Running locally

The project is currently configured for local development and has **not** been documented as a completed public deployment.

1. Clone the repository and enter the project directory.
2. Create a virtual environment and install the pinned dependencies.
3. Configure required settings and credentials **securely**, without committing `.env` or real keys.
4. Apply migrations and run the Django development server.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The source includes `start.sh`, which loads `.env`, runs migrations and `collectstatic`, then starts **Gunicorn with three workers** on port 8000. It is an operational convenience script, not a complete production deployment configuration.

> **Configuration notice:** The reviewed `core/settings.py` contains environment-sensitive settings that need cleanup. Do not publish real application secrets or assume a fresh clone is safe to deploy unchanged. Provide an `.env.example` with placeholders when configuration is standardised.

## Roadmap

### Highest priority — backend correctness and media lifecycle

- Remove old post images when users successfully replace them.
- Remove associated media files when posts are deleted.
- Decide how profile image replacement and deletion should behave with Cloudinary.
- Add safe cleanup rules, storage abstractions and tests for failed saves/moderation.
- Address security/configuration issues listed above.

### AI features

- **Animal-presence validation**: reject uploaded photos that do not contain an animal, with well-defined behaviour for ambiguous images.
- **AI chatbot**: add a useful assistant within the app, with clear scope, safeguards and user-facing interactions.
- Improve moderation resilience, observability and testability (mock external calls).

### Quality, usability and deployment

- Add unit/integration tests for models, forms, ownership rules, HTTP methods and moderation.
- Improve accessibility and frontend consistency.
- Add screenshots or a short demo of key user journeys.
- Prepare production settings, managed media/static hosting and a documented deployment process.
- Consider PostgreSQL when moving to a deployment-oriented architecture.

## What this project demonstrates

**Backend engineering:** custom user and manager, Django ORM relations, annotated aggregates, eager loading, class-based views, forms, permissions, signals, external service integration and validation.

**Frontend engineering:** responsive interfaces built with semantic HTML, reusable Django templates, CSS, Bootstrap and targeted JavaScript, with no requirement for a single-page framework.

**Full-stack ownership:** designing data structures and backend workflows, integrating third-party services, presenting interactive user journeys and documenting deployment considerations in one coherent project.

## License

MIT — see [`LICENSE`](LICENSE).
