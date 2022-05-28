from typing import List
import requests
import pathlib


from common.model.project import (
    CreateProjectArgs,
    Project,
)



class Client:
    endpoint: str = "http://localhost:5000"
    # root: str = pathlib.Path("/")
    
    def create_project(self, name: str) -> Project:
        c = CreateProjectArgs(name=name)
        r = requests.post(
            f"{self.endpoint}/projects", 
            json=c.dict(),
        )
        return Project(**r.json())
        
    
    def get_projects(self) -> List[Project]:
        r = requests.get(f"{self.endpoint}/projects")
        return list(
            Project(**project) for project in r.json()
        )
    
    def get_project(self, id) -> Project:
        r = requests.get(f"{self.endpoint}/projects/{id}")
        j = r.json()
        if 'detail' in j and j['detail'] == 'Not Found':
            raise Exception(f"Project {id} not found.")
        return Project(**r.json())
    
    def delete_project(self, id) -> bool:
        r = requests.delete(f"{self.endpoint}/projects/{id}")
        return r.status_code == 204


def main():
    client = Client()
    created = client.create_project(name="new project")
    print('created', created)
    projects = client.get_projects()
    print('projects', projects)
    project = client.get_project(projects[0].id)
    print('project', project)
    ret = client.delete_project(id=projects[0].id)
    print("deleted:", ret)



if __name__ == "__main__":
    main()
