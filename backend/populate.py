from models import Taxon, TaxonName
from database import create_db_and_tables, get_session
import os

DATA_DIR = "data"

def parse_nodes(file_path):
    taxa = []
    with open(file_path, "r") as f:
        for line in f:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                tax_id = int(parts[0])
                parent_id = int(parts[1])
                rank = parts[2]
                taxa.append(Taxon(id=tax_id, parent_id=parent_id, rank=rank))
    return taxa

def parse_names(file_path):
    names = []
    with open(file_path, "r") as f:
        for line in f:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                tax_id = int(parts[0])
                name = parts[1]
                name_class = parts[3]
                names.append(TaxonName(taxon_id=tax_id, name=name, name_class=name_class))
    return names

def load_data():
    create_db_and_tables()
    session = get_session()

    nodes_path = os.path.join(DATA_DIR, "nodes.dmp")
    names_path = os.path.join(DATA_DIR, "names.dmp")

    taxa = parse_nodes(nodes_path)
    taxon_names = parse_names(names_path)

    session.add_all(taxa)
    session.add_all(taxon_names)
    session.commit()
    session.close()
    print("Database populated successfully!")

if __name__ == "__main__":
    load_data()
