# letit/resources/job.py
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from requests_toolbelt.multipart.encoder import MultipartEncoder

# import sys
# import os
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from letit.schemas.job import JobCategory, JobExperienceLevel, JobLocation, JobType, UserJobCreatedByUserResponse

if TYPE_CHECKING:
    from ..client import Letit


@dataclass
class JobResponse:
    slug: str

    @classmethod
    def from_dict(cls, data: dict) -> "JobResponse":
        return cls(slug=data["slug"])


class JobResource:
    def __init__(self, client: "Letit"):
        self._client = client

    def client_create_user_job_with_company(
        self,
        company_name: str,
        company_description: str,
        company_logo: tuple,  # ("logo.png", open(..., "rb"), "image/png")
        company_website: str,
        job_title: str,
        job_description: str,
        job_how_to_apply: str,
        company_location: Optional[str] = None,
        job_location: JobLocation = JobLocation.REMOTE,
        job_type: JobType = JobType.FULLTIME,
        job_category: JobCategory = JobCategory.PROGRAMMING,
        job_experience_level: JobExperienceLevel = JobExperienceLevel.ALL,
        job_minimum_salary: Optional[int] = None,
        job_maximum_salary: Optional[int] = None,
        job_pay_in_cryptocurrency: bool = False,
        job_skills: Optional[str] = None,
    ) -> UserJobCreatedByUserResponse:
        """
        Create a job post with a company.

        Args:
            company_name: Name of the company.
            company_description: Description of the company.
            company_logo: Tuple of (filename, file_object, mime_type). Optional.
            company_website: Company website URL.
            job_title: Title of the job.
            job_description: Full job description.
            job_how_to_apply: URL or instructions to apply.
            company_location: Optional company location.
            job_location: Defaults to JobLocation.REMOTE.
            job_type: Defaults to JobType.FULLTIME.
            job_category: Defaults to JobCategory.PROGRAMMING.
            job_experience_level: Defaults to JobExperienceLevel.ALL.
            job_minimum_salary: Optional minimum salary.
            job_maximum_salary: Optional maximum salary.
            job_pay_in_cryptocurrency: Defaults to False.
            job_skills: Comma-separated skills string.

        Returns:
            UserJobCreatedByUserResponse with slug.

        Example:
            job = client.job.client_create_user_job_with_company(
                company_name="LetIt",
                company_description="We build things.",
                company_website="https://letit.com",
                job_title="Rust Engineer",
                job_description="Build backend services.",
                job_how_to_apply="https://letit.com/careers",
                job_skills="Rust, SQL, Docker",
            )
        """
        
        fields = {
            "company_name": company_name,
            "company_description": company_description,
            "company_website": company_website,
            "job_title": job_title,
            "job_description": job_description,
            "job_how_to_apply": job_how_to_apply,
            "job_location": job_location,
            "job_type": job_type,
            "job_category": job_category,
            "job_experience_level": job_experience_level,
            "job_pay_in_cryptocurrency": str(job_pay_in_cryptocurrency).lower(),
            "company_logo": company_logo,
        }

        if company_location:
            fields["company_location"] = company_location
        if job_minimum_salary is not None:
            fields["job_minimum_salary"] = str(job_minimum_salary)
        if job_maximum_salary is not None:
            fields["job_maximum_salary"] = str(job_maximum_salary)
        if job_skills:
            fields["job_skills"] = job_skills

        m = MultipartEncoder(fields=fields)

        response = self._client._request(
            "POST",
            "/api/v1/client/job",
            data=m,
            headers={"Content-Type": m.content_type},
        )

        return UserJobCreatedByUserResponse(**response.json())