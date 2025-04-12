from models import Taxon, TaxonName
from database import create_db_and_tables, get_session

def load_data():
    create_db_and_tables()
    session = get_session()

    # Replace this with actual parsing from nodes.dmp and names.dmp
    tax1 = Taxon(id=1, parent_id=None, rank="root")
    tax2 = Taxon(id=2, parent_id=1, rank="species")
    name1 = TaxonName(taxon_id=1, name="Life", name_class="scientific name")
    name2 = TaxonName(taxon_id=2, name="Homo sapiens", name_class="scientific name")

    session.add_all([tax1, tax2, name1, name2])
    session.commit()
    session.close()

if __name__ == "__main__":
    load_data()
