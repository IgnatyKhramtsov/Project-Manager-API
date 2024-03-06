from tasks.models import Project
from utils.repository import SQLAlchemyProjectRepository


class ProjectRepository(SQLAlchemyProjectRepository):
    model = Project
