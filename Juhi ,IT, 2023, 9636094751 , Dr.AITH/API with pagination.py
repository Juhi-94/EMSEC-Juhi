import requests
from bezalel import PaginatedApiIterator

for page in PaginatedApiIterator(requests.Session(), url=f"https://your/api",
                                                   request_page_number_param_name="pageNumber",
                                                   response_page_count_field_name="pageCount",
                                                   response_records_field_name="entities"):
    print(f"Page: {page}")