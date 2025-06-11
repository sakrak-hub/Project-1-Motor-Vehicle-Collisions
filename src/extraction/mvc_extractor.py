import pandas as pd
import requests
import dlt
from extraction.base_extractor import BaseExtractor
from loading.dlt_loader import add_to_pipeline


class MVCExtractor(BaseExtractor):
    src_dict = {
        "https://data.cityofnewyork.us/resource/h9gi-nx95.json": "mvc_crashes",
        "https://data.cityofnewyork.us/resource/bm4k-52h4.json": "mvc_vehicles",
        "https://data.cityofnewyork.us/resource/f55k-p6yu.json": "mvc_persons"
    }

    def __init__(self, limit: int = 1000):
        super().__init__(base_url="", limit=limit)
        self.limit_param = "$limit"
        self.offset_param = "$offset"

    def extract_to_postgres(self):
        for source, name in self.src_dict.items():
            self.base_url = source
            page_offset = 0
            page_max_offset = 50000
            page = 1
            response = requests.get(f"{source}?{self.limit_param}=1000&{self.offset_param}={page_max_offset}")
            while len(response.json()) != 0:
                print(f"Loading page {page} from {name} with offset {page_offset}")
                data = self.load_from_source(
                    page_offset,
                    page_max_offset,
                    limit_param=self.limit_param,
                    offset_param=self.offset_param
                )
                self.add_to_pipeline(data, name)
                page_offset += 50000
                page += 1
                response = requests.get(f"{source}?{self.limit_param}=1000&{self.offset_param}={page_offset + 1000}")
                page_max_offset += 50000

    def extract_to_csv(self):
        for source, name in self.src_dict.items():
            self.base_url = source
            page_offset = 0
            page_max_offset = 50000
            page = 1
            response = requests.get(f"{source}?{self.limit_param}=1000&{self.offset_param}={page_max_offset}")
            while len(response.json()) != 0:
                data_list = []
                for page_data in self.load_from_source(
                    page_offset,
                    page_max_offset,
                    limit_param=self.limit_param,
                    offset_param=self.offset_param
                ):
                    data_list.extend(page_data)
                df = pd.DataFrame(data_list)
                df.to_csv(f"./data/raw/{name}/{name}_{page}.csv", index=False)
                page_offset += 50000
                page += 1
                response = requests.get(f"{source}?{self.limit_param}=1000&{self.offset_param}={page_offset + 1000}")
                page_max_offset += 50000
