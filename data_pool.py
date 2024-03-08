
from datasets import load_dataset, concatenate_datasets

def process_bacterian(sample):
    if sample['input']:
        sample['instruction'] = sample['instruction']+ ' '+sample['input']
    sample['id'] = sample['id'] 
    return sample

def process_cidar(sample):
    sample['id'] = f"cidar-v1-{sample['index']}"
    return sample

class Datasets:
    def __init__(self):
        bacterian_ar = load_dataset('MBZUAI/Bactrian-X', 'ar', split='train[:5000]', verification_mode='no_checks') 
        bacterian_ar = bacterian_ar.map(process_bacterian)
        self.bacterian_ar = self.remove_columns(bacterian_ar)

        cidar = load_dataset('arbml/cidar', split='train[:5000]', verification_mode='no_checks')
        cidar = cidar.map(process_cidar)
        self.cidar = self.remove_columns(cidar) 

    def remove_columns(self, data):
        columns_to_remove = [c for c in data.column_names if c not in ['instruction', 'output', 'id']]
        data = data.remove_columns(columns_to_remove)
        return data

    def get_data(self):
        return  concatenate_datasets([self.cidar, self.bacterian_ar])

