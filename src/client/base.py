


from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel
import requests
import click
import json

from requests import Response

from common.model.search import Search


T = TypeVar('T')

# TODO: pydantic requests

class BaseClient(BaseModel, Generic[T]):
    endpoint: str = "http://localhost:5000"
    route: str
    
    def get_route(self) -> str:
        return f"{self.endpoint}/{self.route}/"
    
    def constructor(self, json: Dict[str, Any]) -> T:
        raise Exception("Not implemented")
    
    def create(self, js: str) -> T:
        r = requests.post(
            f"{self.get_route()}", 
            json=json.loads(js),
            # headers={"Content-type": "application/json"},
        )
        if r.status_code not in [201]:
            raise Exception(
                f"Recieved unexpected code {r.status_code}.\n {r.content}"
            )
        return self.constructor(r.json())
    
    def search(self, search: Search) -> List[T]:
        r = requests.get(
            f"{self.get_route()}search",
            json=json.loads(search.json()),
        )
        if r.status_code not in [200]:
            raise Exception(
                f"Recieved unexpected code {r.status_code}.\n {r.content}"
            )
        return list(self.constructor(entry) for entry in r.json())
    
    def find(self, **kwargs) -> T:
        results = self.search(Search.construct_search(**kwargs))
        if len(results) == 0:
            raise click.ClickException(f"No matching id: query={id}")
        if len(results) > 1:
            raise click.ClickException(
                "Found multiple completions: [" + (
                    ", ".join(
                        str(result.id) for result in results
                    )
                ) + "]"
            )
        return results[0]
    
    def list(self, override: Optional[str] = None) -> List[T]:
        if override is None:
            url = f"{self.get_route()}"
        else:
            url = f"{self.endpoint}/{override}"
        r = requests.get(url)
        if r.status_code not in [200]:
            raise Exception(
                f"Recieved unexpected code {r.status_code}.\n {r.content}"
            )
        return list(
            self.constructor(result) for result in r.json()
        )
    
    def get(self, id: str) -> T:
        r = requests.get(f"{self.get_route()}{id}")
        if r.status_code not in [200]:
            raise Exception(
                f"Recieved unexpected code {r.status_code}.\n {r.content}"
            )
        j = r.json()
        if 'detail' in j and j['detail'] == 'Not Found':
            raise click.ClickException(f"Id {id} not found.")
        return self.constructor(r.json())
    
    def delete(self, id) -> None:
        r = requests.delete(f"{self.get_route()}{id}")
        if r.status_code not in [204]:
            raise Exception(
                f"Recieved unexpected code {r.status_code}.\n {r.content}"
            )
        # TODO
        return True


