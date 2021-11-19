'''
Author: Shuailin Chen
Created Date: 2021-09-28
Last Modified: 2021-11-19
	content: 1. original and extend SN6 data
             2. using masks generated by FH method
             3. using color jitter
'''

from copy import deepcopy
                             
# dataset settings
data_source_cfg = dict(
    root = 'data',
    img_dir = ['SN6_sup',
            'SN6_extend/tile_sinclairv2_rotated/900'],
    ann_dir = ['SN6_sup/fh_mask_rotated',
            'SN6_sup/extend_fh_mask_rotated'],
    type='SpaceNet6Extend',
    memcached=False,
    return_label=True,
)
data_train_list = ['data/SN6_sup/split/labeled_and_unlabeled_rotated.txt', 
                    'data/SN6_sup/split/extend_train_GT02.txt',
                    ]
                    
dataset_type = 'PixBYOLDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
train_pipeline = [
    # dict(type='ViewImgLabels'),
    # dict(type='IMRandomResizedCrop', size=224, min_valid_ratio=0.05),
    dict(type='IMResize', img_scale=(900, 900), ratio_range=(0.5, 2.0)),
    dict(type='IMRandomCrop', crop_size=(224, 224)),
    # dict(type='ViewImgLabels'),
    dict(type='RandomHorizontalFlip'),
    # dict(type='ViewImgLabels'),
    dict(
        type='RandomAppliedTransOnlyImg',
        transforms=[
            dict(
                type='ColorJitter',
                brightness=0.4,
                contrast=0.4,
                saturation=0.2,
                hue=0.1)
        ],
        p=0.8),
    dict(type='IMRandomGrayscale', p=0.2),
    # dict(type='ViewImgLabels'),
    dict(
        type='RandomAppliedTransOnlyImg',
        transforms=[
            dict(
                type='GaussianBlur',
                sigma_min=0.1,
                sigma_max=2.0),
            # dict(
            #     type='BoxBlur',
            #     radius_min=0,
            #     radius_max=3,
            #     )
        ],
        p=1.),
    # dict(type='ViewImgLabels'),
    # dict(type='RandomAppliedTrans',
    #      transforms=[dict(type='Solarization')], p=0.),
]

# prefetch
prefetch = False
if not prefetch:
    train_pipeline.extend([dict(type='IMToTensor'), 
                    dict(type='IMNormalize', **img_norm_cfg),
                    # dict(type='ViewImgLabels', **img_norm_cfg),
    ])

train_pipeline1 = deepcopy(train_pipeline)
train_pipeline2 = deepcopy(train_pipeline)
train_pipeline2[4]['p'] = 0.1 # gaussian blur
# train_pipeline2[5]['p'] = 0.2 # solarization
    
data = dict(
    imgs_per_gpu=32,    # total 32
    workers_per_gpu=12,
    train=dict(
        # if_visualize=True, 
        type=dataset_type,
        data_source=dict(
            list_file=data_train_list,
            **data_source_cfg),
        pipeline1=train_pipeline1,
        pipeline2=train_pipeline2,
        prefetch=prefetch,
    ))