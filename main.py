from src.utils.u1 import exe_sql, lister_contenu_tables, supprimer_tables,  creer_table_evenement
from src.core.variables_metier import tables_metier

exe_sql('requetes/vider_tables_metier.sql')

lister_contenu_tables(tables_metier)

supprimer_tables(tables_metier)

creer_table_evenement()
    