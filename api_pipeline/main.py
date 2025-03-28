import traceback


from scripts.extract_data import extract_data
from scripts.transform_data import transform_data

try:
    extract_data()
    transform_data()

except:
    traceback.print_exc()
