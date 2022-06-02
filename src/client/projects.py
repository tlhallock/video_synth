from typing import Any, Dict

from client.base import BaseClient

from common.model.project import (
    CreateProjectArgs,
    Project,
)


class ProjectsClient(BaseClient[Project]):
    def constructor(self, js: Dict[str, Any]) -> Project:
        return Project(**js)
    
    def create_project(self, name: str) -> Project:
        args = CreateProjectArgs(name=name)
        return self.create(js=args.json())
    
    @staticmethod
    def create_client() -> "ProjectsClient":
        return ProjectsClient(
            endpoint="http://localhost:5000",
            route="projects",
        )





# def main():
#     client = Client()
#     created = client.create_project(name="new project")
#     print('created', created)
#     projects = client.get_projects()
#     print('projects', projects)
#     project = client.get_project(projects[0].id)
#     print('project', project)
#     ret = client.delete_project(id=projects[0].id)
#     print("deleted:", ret)



# if __name__ == "__main__":
#     main()
