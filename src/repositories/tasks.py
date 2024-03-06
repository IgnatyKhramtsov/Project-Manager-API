from tasks.models import Task
from utils.repository import SQLAlchemyProjectRepository


class TaskRepository(SQLAlchemyProjectRepository):
    model = Task
