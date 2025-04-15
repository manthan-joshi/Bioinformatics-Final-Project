from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List


class TaxonName(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    taxon_id: int = Field(foreign_key="taxon.id")
    name: str
    name_class: str

    taxon: Optional["Taxon"] = Relationship(back_populates="names")


class Taxon(SQLModel, table=True):
    id: int = Field(primary_key=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="taxon.id")
    rank: Optional[str] = None

    parent: Optional["Taxon"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "Taxon.id"})
    children: List["Taxon"] = Relationship(back_populates="parent")

    names: List[TaxonName] = Relationship(back_populates="taxon")
