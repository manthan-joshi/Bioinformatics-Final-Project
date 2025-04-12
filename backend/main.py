from fastapi import FastAPI, HTTPException, Query
from sqlmodel import select
from backend.models import Taxon, TaxonName
from backend.database import get_session

app = FastAPI()

@app.get("/taxa")
def get_taxon(tax_id: int):
    session = get_session()

    taxon = session.get(Taxon, tax_id)
    if not taxon:
        raise HTTPException(status_code=404, detail="Taxon not found")

    parent = session.get(Taxon, taxon.parent_id) if taxon.parent_id else None
    children = session.exec(select(Taxon).where(Taxon.parent_id == tax_id)).all()
    names = session.exec(select(TaxonName).where(TaxonName.taxon_id == tax_id)).all()

    return {
        "id": taxon.id,
        "rank": taxon.rank,
        "parent": {"id": parent.id, "name": next((n.name for n in parent.names if n.name_class == "scientific name"), None)} if parent else None,
        "children": [{"id": c.id, "rank": c.rank, "name": next((n.name for n in c.names if n.name_class == "scientific name"), None)} for c in children],
        "names": [{"name": n.name, "class": n.name_class} for n in names],
    }

@app.get("/search")
def search_taxa(
    keyword: str,
    mode: str = Query("contains", enum=["contains", "starts with", "ends with"]),
    page: int = 1,
    items_per_page: int = 10
):
    session = get_session()
    stmt = select(TaxonName)

    if mode == "contains":
        stmt = stmt.where(TaxonName.name.contains(keyword))
    elif mode == "starts with":
        stmt = stmt.where(TaxonName.name.startswith(keyword))
    elif mode == "ends with":
        stmt = stmt.where(TaxonName.name.endswith(keyword))

    total = session.exec(stmt).count()
    stmt = stmt.offset((page - 1) * items_per_page).limit(items_per_page)

    results = session.exec(stmt).all()

    return {
        "total": total,
        "page": page,
        "results": [
            {"taxon_id": r.taxon_id, "name": r.name, "class": r.name_class}
            for r in results
        ],
    }
