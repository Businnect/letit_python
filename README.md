# LetIt Python

The official Python SDK for the [LetIt](https://letit.com) API.

## Installation

```bash
pip install letit
```

## Setup

Find your API token at [https://letit.com/settings/developer](https://letit.com/settings/developer) after creating an account at [https://letit.com/register](https://letit.com/register).

```python
from letit import LetIt

client = LetIt(api_token="your_api_token_here")
```

---

## Micropost

### Create a post

```python
from letit.schemas.micropost import PostType

# Text post
post = client.micropost.client_create_micropost(
    title="Hello World",
    body="This is my first post.",
)
print(post.public_id)
print(post.link)

# Media post
with open("photo.png", "rb") as f:
    post = client.micropost.client_create_micropost(
        title="My photo",
        body="Check this out",
        post_type=PostType.MEDIA,
        file=("photo.png", f, "image/png"),
    )

# Reply to a post
reply = client.micropost.client_create_micropost(
    body="Great post!",
    parent_micropost_public_id="post_public_id_here",
)

# Nested reply (reply to a comment)
nested = client.micropost.client_create_micropost(
    body="I agree!",
    parent_micropost_public_id="post_public_id_here",
    parent_micropost_comment_public_id="comment_public_id_here",
)
```

### Delete a post

```python
client.micropost.client_delete_micropost(public_id="post_public_id_here")
```

### Vote on a post (toggle)

```python
result = client.micropost.client_vote_micropost(public_id="post_public_id_here")
print(result.user_voted)  # True or False
```

---

## Job

### Create a job post

```python
from letit.schemas.job import JobLocation, JobType, JobCategory, JobExperienceLevel

job = client.job.client_create_user_job_with_company(
    company_name="LetIt",
    company_description="We build things.",
    company_website="https://letit.com",
    job_title="Rust Engineer",
    job_description="Build backend services in Rust.",
    job_how_to_apply="https://letit.com/careers",
    job_location=JobLocation.REMOTE,
    job_type=JobType.FULLTIME,
    job_category=JobCategory.PROGRAMMING,
    job_experience_level=JobExperienceLevel.SENIOR,
    job_skills="Rust, SQL",
)
print(job.slug)

# With company logo
with open("logo.png", "rb") as f:
    job = client.job.client_create_user_job_with_company(
        company_name="LetIt",
        company_description="We build things.",
        company_website="https://letit.com",
        company_logo=("logo.png", f, "image/png"),
        job_title="Rust Engineer",
        job_description="Build backend services in Rust.",
        job_how_to_apply="https://letit.com/careers",
    )
```

### Delete a job post

```python
client.job.client_delete_job(slug="rust-engineer-letit")
```

---

## Blog

### Get admin article

```python
article = client.blog.client_get_admin_blog()
if article:
    print(article.title)
    print(article.body)
```

### List admin articles

```python
result = client.blog.client_list_admin_blogs()
print(result.total_list)
for article in result.list:
    print(article.title, article.slug)
```

---

## API Reference

### `LetIt(api_token, base_url?)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | `str` | Your API token |
| `base_url` | `str` | API base URL (default: `https://api.letit.com`) |

---

### `client.micropost.client_create_micropost(...)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `body` | `str` | required | Content of the post |
| `title` | `str` | `None` | Required for original posts |
| `post_type` | `PostType` | `PostType.TEXT` | `TEXT` or `MEDIA` |
| `community_name` | `str` | `None` | Community to post in |
| `parent_micropost_public_id` | `str` | `None` | For replies |
| `parent_micropost_comment_public_id` | `str` | `None` | For nested replies |
| `allow_comments` | `bool` | `True` | Whether comments are allowed |
| `is_draft` | `bool` | `False` | Save as draft |
| `file` | `tuple` | `None` | `(filename, file_object, mime_type)` for MEDIA posts |

**Returns:** `CreatedWithPublicIdAndLinkResponse` with `public_id` and `link`

---

### `client.micropost.client_delete_micropost(public_id)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `public_id` | `str` | Public ID of the post to delete |

**Returns:** `None` (204 on success)

---

### `client.micropost.client_vote_micropost(public_id)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `public_id` | `str` | Public ID of the post to vote on |

**Returns:** `VoteResponse` with `user_voted` (bool)

---

### `client.job.client_create_user_job_with_company(...)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `company_name` | `str` | required | Name of the company |
| `company_description` | `str` | required | Description of the company |
| `company_website` | `str` | required | Company website URL |
| `job_title` | `str` | required | Title of the job |
| `job_description` | `str` | required | Full job description |
| `job_how_to_apply` | `str` | required | URL or instructions to apply |
| `company_logo` | `tuple` | `None` | `(filename, file_object, mime_type)` |
| `company_location` | `str` | `None` | Company location |
| `job_location` | `JobLocation` | `REMOTE` | `REMOTE`, `ONSITE`, `HYBRID` |
| `job_type` | `JobType` | `FULLTIME` | `FULLTIME`, `PARTTIME`, `CONTRACT`, `FREELANCE`, `INTERNSHIP` |
| `job_category` | `JobCategory` | `PROGRAMMING` | `PROGRAMMING`, `BLOCKCHAIN`, `DESIGN`, `MARKETING`, `CUSTOMERSUPPORT`, `WRITING`, `PRODUCT`, `SERVICE`, `HUMANRESOURCE`, `ELSE` |
| `job_experience_level` | `JobExperienceLevel` | `ALL` | `ALL`, `JUNIOR`, `MID`, `SENIOR`, `NOEXPERIENCEREQUIRED` |
| `job_minimum_salary` | `int` | `None` | Minimum salary |
| `job_maximum_salary` | `int` | `None` | Maximum salary |
| `job_pay_in_cryptocurrency` | `bool` | `False` | Pay in cryptocurrency |
| `job_skills` | `str` | `None` | Comma-separated skills |

**Returns:** `UserJobCreatedByUserResponse` with `slug`

---

### `client.job.client_delete_job(slug)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `slug` | `str` | Slug of the job post to delete |

**Returns:** `None` (204 on success)

---

### `client.blog.client_get_admin_blog()`

**Returns:** `BlogResponse` or `None`

---

### `client.blog.client_list_admin_blogs()`

**Returns:** `BlogListResponse` with `list`, `total_list` and `total_pages`

---

## Development

```bash
# Install in editable mode
pip install -e .

# Run unit tests
python -m pytest letit/tests/test_letit_unit.py -v

# Run integration tests (requires real API token)
LETIT_API_TOKEN=your_token python -m pytest letit/tests/test_letit_integration.py -v -s
```

## License

MIT