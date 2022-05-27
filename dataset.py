import os
import pandas as pd
from torchvision.io import read_image
from torch.utils.data import Dataset
import pickle
from PIL import Image
import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        with open(img_path, 'rb') as handle:
            frame_data = pickle.load(handle)
            image = rgb2gray(frame_data['rgb'])
        label = self.img_labels.iloc[idx, 1:].to_numpy(dtype=float)
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label