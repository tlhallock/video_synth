from typing import Any, Dict, List

from cli.client.base import BaseClient

from common.model.thing import (
    AddThingArgs,
    Thing,
)


class ThingsClient(BaseClient[Thing]):
    def constructor(self, js: Dict[str, Any]) -> Thing:
        return Thing(**js)
    
    def create_thing(self, args: AddThingArgs) -> Thing:
        # import pdb; pdb.set_trace()
        return self.create(js=args.json())
    
    def list_under(self, project: str) -> List[Thing]:
        override = f"projects/{project}/things"
        return self.list(override=override)
    
    @staticmethod
    def create_client() -> "ThingsClient":
        return ThingsClient(
            endpoint="http://localhost:5000",
            route="things",
        )
