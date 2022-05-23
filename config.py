# constants for DB
excel_to_db_file_name = "raw_files/Arbitration_registry.xls"
dB_path = "sqlite:///data_base/procurement_monitoring.db"
db_file_name = "data_base/procurement_monitoring.db"
dB_table_name = "procurement_monitoring"
raw_files_full_path = '/Users/dmitrysolonnikov/PycharmProjects/procurementMonitoring/raw_files/'
docs_files_full_path = '/Users/dmitrysolonnikov/PycharmProjects/procurementMonitoring/docs/'
import_excel_table_name = 'Monitoring.xls'

# auto_docs names
doc_accept_complainant = 'Accept_complainant'
doc_reject_complainant = 'Reject_complainant'
doc_result_of_complaint = 'Result_of_complaint'

auto_doc_window = None

notif_manes = ''

# exception messages
value_error = "По выбранным параметрам сведения отсутствуют"

# links
dev_server_link = 'http://127.0.0.1:8050/'

# data_frame
data_frame = []