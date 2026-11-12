from src.database.definition.create_staff_table import create_staff_table
from src.database.definition.create_case_table import create_case_table 
from src.database.definition.create_suspect_table import create_suspect_table
from src.database.definition.create_arrested_table import create_arrested_table 

from src.database.definition.create_alters_table import create_alters_table
from src.database.definition.create_linked_table import create_linked_table 
from src.database.definition.create_arrestfromcase_table import create_ArrestFromCase_table 

def create_database():

    create_staff_table()
    create_case_table()
    create_suspect_table()
    create_arrested_table()

    create_alters_table()
    create_linked_table()
    create_ArrestFromCase_table()

if __name__ == "__main__":
    create_database()