

from typing import List, Optional
from pydantic import BaseModel


class SearchTerm(BaseModel):
    key: str
    value: str


class Search(BaseModel):
    terms: List[SearchTerm]
    
    def get_id_term(self) -> Optional[str]:
        for term in self.terms:
            if term.key == "id":
                return term.value
        return None
    
    def construct_query(self):
        query = dict()
        for term in self.terms:
            if term.key == "id":
                continue
            # sql injection?
            query[term.key] = {"$regex": term.value}
        return query

    @staticmethod
    def construct_search(
        # id: Optional[str] = None,
        **kwargs,
    ) -> "Search":
        terms = []
        # if id is not None:
        #     terms.append(SearchTerm(
        #         key="_id", value=id))
        for key, value in kwargs.items():
            if value is None:
                continue
            terms.append(SearchTerm(
                key=key, value=value))
        return Search(terms=terms)
    
    
# def build_query(id: Optional[str] = None, name: Optional[str] = None):
#     query = dict()
#     # sql injection?
#     if id is not None:
#         query["_id"] = {
#             # Should this be only the ends with
#             "$regex": f"{id}" 
#         }
#     if name is not None:
#         query["name"] = {
#             "$regex": f"{name}"
#         }
#     return query