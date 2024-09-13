# Developer Guidelines
This guidelines is for developers who can run the app using code.

## Clone the repository
```bash
git clone https://github.com/amine0110/scan-duplicate-checker
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run the app
```bash
python app.py
```

## Run the checker
If you are not interested in the app, you can run the checker directly from the checker.py file. Here is an example:

```Python
# For checking all scans in a folder:
path_to_folder = 'path/to/your/folder'
checker = ScanDuplicateChecker(path_to_folder)
duplicates = checker.check_folder_for_duplicates()
print(duplicates)
```

```Python
# For comparing two specific scans:
scan_1 = 'path/to/scan1'
scan_2 = 'path/to/scan2'
checker = ScanDuplicateChecker()
is_duplicate = checker.check_duplicate(scan_1, scan_2)
print("Are the scans duplicates?", is_duplicate)
```
