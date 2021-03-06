import os
import torch
from torch.utils.data import Dataset
from PIL import Image
import numpy as np


class LIP(Dataset):

    def __init__(self, par_path, transform, train=True):
        self.par_path = par_path # Setting parent directory
        self.transform = transform # Setting transform object
        self.train = train # Setting train / eval

        # Setting image paths
        self.img_path, self.gt_path = self.get_image_paths()

        # Dataset size
        self.len = len(self.img_path)

    def __getitem__(self, index):
        return self.get_sample_at_index(index)
    
    def __len__(self):
        return self.len

    # Returns training example at index 'index'
    def get_sample_at_index(self, index): 
        img = Image.open(self.img_path[index])
        if img.mode == 'L': # If image is greyscale convert to RGB
            img = img.convert('RGB')

        gt = Image.open(self.gt_path[index])
        if gt.mode == 'RGB': # If ground truth is RGB convert to greyscale (L)
            gt = gt.convert('L')

        # Run transforms on training example
        img = self.transform['img'](img)
        gt = self.transform['gt'](gt)

        return img, gt

    # Returns list of all training examples
    def get_image_paths(self):
        if self.train:
            img_dir = os.path.join(self.par_path, 'TrainVal_images', 'train_images')
        else:
            img_dir = os.path.join(self.par_path, 'TrainVal_images', 'val_images')

        if self.train:
            gt_dir = os.path.join(self.par_path, 'TrainVal_parsing_annotations', 'train_segmentations')
        else:   
            gt_dir = os.path.join(self.par_path, 'TrainVal_parsing_annotations', 'val_segmentations')

        if self.train:
            id_path = os.path.join(self.par_path, 'TrainVal_images', 'train_id.txt')
        else:
            id_path = os.path.join(self.par_path, 'TrainVal_images', 'val_id.txt')

        img_paths = []
        gt_paths = []

        f = open(id_path, 'r')

        for line in f:
            img_paths.append(os.path.join(img_dir, line.rstrip() + '.jpg'))
            gt_paths.append(os.path.join(gt_dir, line.rstrip() + '.png'))

        return img_paths, gt_paths


class LIPWithClass(Dataset):

    def __init__(self, par_path, transform, num_class, train=True):
        self.par_path = par_path # Setting parent directory
        self.transform = transform # Setting transform object
        self.train = train # Setting train / eval
        self.num_class = num_class # Setting the number of classes

        # Setting image paths
        self.img_path, self.gt_path = self.get_image_paths()

        # Dataset size
        self.len = len(self.img_path)

    def __getitem__(self, index):
        return self.get_sample_at_index(index)
    
    def __len__(self):
        return self.len

    # Returns training example at index 'index'
    def get_sample_at_index(self, index): 
        img = Image.open(self.img_path[index])
        if img.mode == 'L': # If image is greyscale convert to RGB
            img = img.convert('RGB')

        gt = Image.open(self.gt_path[index])
        if gt.mode == 'RGB': # If ground truth is RGB convert to greyscale (L)
            gt = gt.convert('L')

        gt_cls = [True if i in np.unique(gt) else False for i in range(self.num_class)] # True if class present in gt else False
        gt_cls = torch.tensor(gt_cls)

        # Run transforms on training example
        img = self.transform['img'](img)
        gt = self.transform['gt'](gt)

        return img, gt, gt_cls

    # Returns list of all training examples
    def get_image_paths(self):
        if self.train:
            img_dir = os.path.join(self.par_path, 'TrainVal_images', 'train_images')
        else:
            img_dir = os.path.join(self.par_path, 'TrainVal_images', 'val_images')

        if self.train:
            gt_dir = os.path.join(self.par_path, 'TrainVal_parsing_annotations', 'train_segmentations')
        else:   
            gt_dir = os.path.join(self.par_path, 'TrainVal_parsing_annotations', 'val_segmentations')

        if self.train:
            id_path = os.path.join(self.par_path, 'TrainVal_images', 'train_id.txt')
        else:
            id_path = os.path.join(self.par_path, 'TrainVal_images', 'val_id.txt')

        img_paths = []
        gt_paths = []

        f = open(id_path, 'r')

        for line in f:
            img_paths.append(os.path.join(img_dir, line.rstrip() + '.jpg'))
            gt_paths.append(os.path.join(gt_dir, line.rstrip() + '.png'))

        return img_paths, gt_paths


