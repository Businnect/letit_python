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

## Usage

### Create a micropost

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
```

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
```

## API Reference

### `LetIt(api_token, base_url?)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | `str` | Your API token |
| `base_url` | `str` | API base URL (default: `https://api.letit.com`) |

### `client.micropost.client_create_micropost(...)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `body` | `str` | required | Content of the post |
| `title` | `str` | `None` | Required for original posts |
| `post_type` | `PostType` | `PostType.TEXT` | `PostType.TEXT` or `PostType.MEDIA` |
| `community_name` | `str` | `None` | Community to post in |
| `parent_micropost_public_id` | `str` | `None` | For replies |
| `parent_micropost_comment_public_id` | `str` | `None` | For nested replies |
| `allow_comments` | `bool` | `True` | Whether comments are allowed |
| `is_draft` | `bool` | `False` | Save as draft |
| `file` | `tuple` | `None` | `(filename, file_object, mime_type)` for MEDIA posts |

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
| `job_location` | `JobLocation` | `JobLocation.REMOTE` | `REMOTE`, `ONSITE`, `HYBRID` |
| `job_type` | `JobType` | `JobType.FULLTIME` | `FULLTIME`, `PARTTIME`, `CONTRACT`, `FREELANCE`, `INTERNSHIP` |
| `job_category` | `JobCategory` | `JobCategory.PROGRAMMING` | `PROGRAMMING`, `BLOCKCHAIN`, `DESIGN`, `MARKETING`, `CUSTOMERSUPPORT`, `WRITING`, `PRODUCT`, `SERVICE`, `HUMANRESOURCE`, `ELSE` |
| `job_experience_level` | `JobExperienceLevel` | `JobExperienceLevel.ALL` | `ALL`, `JUNIOR`, `MID`, `SENIOR`, `NOEXPERIENCEREQUIRED` |
| `job_minimum_salary` | `int` | `None` | Minimum salary |
| `job_maximum_salary` | `int` | `None` | Maximum salary |
| `job_pay_in_cryptocurrency` | `bool` | `False` | Pay in cryptocurrency |
| `job_skills` | `str` | `None` | Comma-separated skills |

## Development

```bash
# Install in editable mode
pip install -e .

# Run unit tests
python -m pytest letit/tests/test_letit.py -v

# Run integration tests (requires real API token)
LETIT_API_TOKEN=your_token python -m pytest letit/tests/test_letit_integration.py -v -s
```

## License

MIT
