from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from requests_toolbelt.multipart.encoder import MultipartEncoder

from letit.schemas.job import JobCategory, JobExperienceLevel, JobLocation, JobType, UserJobCreatedByUserResponse

if TYPE_CHECKING:
    from ..client import LetIt


class JobResource:
    def __init__(self, client: "LetIt"):
        self._client = client

    def client_create_user_job_with_company(
        self,
        company_name: str,
        company_description: str,
        company_website: str,
        job_title: str,
        job_description: str,
        job_how_to_apply: str,
        company_logo: Optional[tuple] = None,
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
        Cria uma vaga de emprego com empresa.

        Args:
            company_name: Nome da empresa.
            company_description: Descrição da empresa.
            company_website: Site da empresa.
            job_title: Título da vaga.
            job_description: Descrição completa da vaga.
            job_how_to_apply: URL ou instruções para candidatura.
            company_logo: Tuple (filename, file_object, mime_type). Opcional.
            company_location: Localização da empresa (opcional).
            job_location: REMOTE, ONSITE ou HYBRID. Padrão: REMOTE.
            job_type: FULLTIME, PARTTIME, CONTRACT, FREELANCE, INTERNSHIP. Padrão: FULLTIME.
            job_category: Categoria da vaga. Padrão: PROGRAMMING.
            job_experience_level: Nível de experiência. Padrão: ALL.
            job_minimum_salary: Salário mínimo (opcional).
            job_maximum_salary: Salário máximo (opcional).
            job_pay_in_cryptocurrency: Pagamento em cripto. Padrão: False.
            job_skills: Skills separadas por vírgula (opcional).

        Returns:
            UserJobCreatedByUserResponse com slug.
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
        }

        if company_logo:
            fields["company_logo"] = company_logo
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

    def client_delete_job(self, slug: str) -> None:
        """
        Deleta uma vaga de emprego pelo slug.

        Args:
            slug: Identificador único da vaga.

        Returns:
            None (204 No Content em caso de sucesso).
        """
        self._client._request(
            "DELETE",
            "/api/v1/client/job",
            json={"slug": slug},
        )
