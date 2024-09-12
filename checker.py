import os
import hashlib
import numpy as np
import pydicom
import nibabel as nib
import nrrd

class ScanDuplicateChecker:
    def __init__(self, folder_path=None):
        """
        Initialize the class with an optional folder path.
        """
        self.folder_path = folder_path
        self.supported_formats = ['.dcm', '.nii', '.nrrd', '.nhdr', '.nii.gz', '.gz']

    def get_image_data(self, file_path):
        """
        Load image data based on file type.
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.dcm':  # DICOM
            ds = pydicom.dcmread(file_path)
            return ds.pixel_array
        
        elif ext == '.nii' or ext == '.nii.gz' or ext == '.gz':  # NIfTI
            img = nib.load(file_path)
            return img.get_fdata()

        elif ext in ['.nrrd', '.nhdr']:  # NRRD
            data, header = nrrd.read(file_path)
            return data
        
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def preprocess_image(self, image_data):
        """
        Preprocess image data to ensure consistent comparison.
        This includes normalization and data type consistency.
        """
        # Convert to float and normalize values if needed
        image_data = np.asarray(image_data, dtype=np.float32)
        image_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data))
        return image_data

    def compute_hash(self, image_data):
        """
        Compute a hash of the preprocessed image data for comparison.
        """
        # Preprocess the image data
        preprocessed_data = self.preprocess_image(image_data)
        # Convert the image data to a bytes representation, using np.tobytes()
        image_bytes = preprocessed_data.tobytes()
        # Generate a hash of the bytes using SHA256
        return hashlib.sha256(image_bytes).hexdigest()

    def check_duplicate(self, file1, file2):
        """
        Check if two files are duplicates.
        """
        # Load image data
        img_data1 = self.get_image_data(file1)
        img_data2 = self.get_image_data(file2)
        
        # Compute hashes
        hash1 = self.compute_hash(img_data1)
        hash2 = self.compute_hash(img_data2)
        
        # Return whether the hashes are the same
        return hash1 == hash2

    def check_folder_for_duplicates(self):
        """
        Check a folder for duplicate scans.
        """
        if not self.folder_path:
            raise ValueError("No folder path provided")

        # Dictionary to store file hashes
        file_hashes = {}
        duplicates = []

        # Walk through the folder and check each file
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext in self.supported_formats:
                    # Get image data
                    try:
                        img_data = self.get_image_data(file_path)
                        # Compute hash
                        img_hash = self.compute_hash(img_data)

                        if img_hash in file_hashes:
                            duplicates.append((file_path, file_hashes[img_hash]))
                        else:
                            file_hashes[img_hash] = file_path
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

        if duplicates:
            return duplicates
        else:
            return "No duplicates found"

if __name__ == "__main__":
    # For checking all scans in a folder:
    path_to_folder = 'c:/Users/pycad/Documents/PYCAD/datasets/spleen200/split/train/images'
    checker = ScanDuplicateChecker(path_to_folder)
    duplicates = checker.check_folder_for_duplicates()
    print(duplicates)


    # For comparing two specific scans:
    # scan_1 = 'c:/Users/pycad/Documents/PYCAD/datasets/spleen200/split/train/images/case_0199.nii.gz'
    # # scan_2 = 'c:/Users/pycad/Documents/PYCAD/datasets/spleen200/split/train/images/case_0005.nii.gz'
    # scan_2 = 'c:/Users/pycad/Documents/PYCAD/datasets/spleen200/split/train/images/case_0200.nrrd'
    
    # checker = ScanDuplicateChecker()
    # is_duplicate = checker.check_duplicate(scan_1, scan_2)
    # print("Are the scans duplicates?", is_duplicate)
