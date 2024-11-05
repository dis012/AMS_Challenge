import torch
import matplotlib.pyplot as plt
import nibabel as nib
import torch.nn.functional as F

def get_common_bounding_box(data1, data2, threshold1=-900, threshold2=10):
    """
    Compute a common bounding box that includes non-background regions of both images.
    :param data1: 3D tensor (e.g., CT image)
    :param data2: 3D tensor (e.g., MR image)
    :param threshold1: threshold for identifying background in data1
    :param threshold2: threshold for identifying background in data2
    :return: cropped data1 and data2 using the common bounding box
    """

    # Conver to long
    data1 = data1.long()
    data2 = data2.long()

    # Create masks for non-background regions
    mask1 = data1 > threshold1
    mask2 = data2 > threshold2
    
    # Combine masks to find the union of non-background regions
    combined_mask = mask1 | mask2
    
    # Get non-zero coordinates in each dimension for the combined mask
    non_zero_indices = torch.nonzero(combined_mask, as_tuple=True)
    min_x, max_x = non_zero_indices[0].min(), non_zero_indices[0].max()
    min_y, max_y = non_zero_indices[1].min(), non_zero_indices[1].max()
    min_z, max_z = non_zero_indices[2].min(), non_zero_indices[2].max()
    
    # Crop both data1 and data2 using the common bounding box
    cropped_data1 = data1[min_x:max_x+1, min_y:max_y+1, min_z:max_z+1]
    cropped_data2 = data2[min_x:max_x+1, min_y:max_y+1, min_z:max_z+1]
    
    return cropped_data1, cropped_data2

def adjust_values(image_ct, image_mr):
    '''
    Adjust the intensity of images from 0 to 255.
    :param image_ct: 3D tensor (CT image)
    :param image_mr: 3D tensor (MR image)
    :return: adjusted CT image
    '''

    # Slope calculation
    #slope = (image_mr.max() - image_mr.min()) / (image_ct.max() - image_ct.min())
    slope_ct = 255 / (image_ct.max() - image_ct.min())
    slope_mr = 255 / (image_mr.max() - image_mr.min())

    # Adjust and round the intensities
    adjusted_image_ct = torch.round(slope_ct * (image_ct - image_ct.min()))
    adjusted_image_mr = torch.round(slope_mr * (image_mr - image_mr.min()))

    # Clip values to ensure they are within [0, 255]
    adjusted_image_ct = torch.clamp(adjusted_image_ct, 0, 255)
    adjusted_image_mr = torch.clamp(adjusted_image_mr, 0, 255)

    return adjusted_image_ct, adjusted_image_mr

def downsample_image(image, scale_factor=None, target_size=None, mode='trilinear'):
    """
    Downsample a 3D image tensor.
    
    :param image: 3D tensor of shape (H, W, D)
    :param scale_factor: Factor to scale the image (e.g., 0.5 for half the size)
    :param target_size: Tuple of target dimensions (H, W, D)
    :param mode: Interpolation mode, 'trilinear' or 'nearest' for binary masks
    :return: Downsampled 3D tensor
    """
    # Add batch and channel dimensions to use with F.interpolate
    image = image.unsqueeze(0).unsqueeze(0)  # Shape becomes (1, 1, H, W, D)
    
    # Downsample using scale_factor or target_size
    if scale_factor is not None:
        downsampled_image = F.interpolate(image, scale_factor=scale_factor, mode=mode, align_corners=False)
    elif target_size is not None:
        downsampled_image = F.interpolate(image, size=target_size, mode=mode, align_corners=False)
    else:
        raise ValueError("Either scale_factor or target_size must be provided.")
    
    # Remove batch and channel dimensions
    downsampled_image = downsampled_image.squeeze(0).squeeze(0)
    return downsampled_image

'''
test_image_CT = torch.from_numpy(nib.load('/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/Abdomen/imagesTr/img0016_tcia_CT.nii.gz').get_fdata())
test_image_MR = torch.from_numpy(nib.load('/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/Abdomen/imagesTr/img0016_tcia_MR.nii.gz').get_fdata())

print("CT image shape:", test_image_CT.shape)
print("CT min value:", test_image_CT.min())
print("CT max value:", test_image_CT.max())
print("MR image shape:", test_image_MR.shape)
print("MR min value:", test_image_MR.min())
print("MR max value:", test_image_MR.max())

# Crop the background from the CT and MR images
cropped_CT, cropped_MR = get_common_bounding_box(test_image_CT, test_image_MR, -900, 10)

print("Cropped CT image shape:", cropped_CT.shape)
print("Cropped CT min value:", cropped_CT.min())
print("Cropped MR image shape:", cropped_MR.shape)
print("Cropped MR min value:", cropped_MR.min())

slice_index_axial = cropped_CT.shape[0] // 2

# Display the cropped images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cropped_CT[slice_index_axial, :, :], cmap='gray')
plt.title('Cropped CT Image')
plt.axis('off')
plt.subplot(1, 2, 2)
plt.imshow(cropped_MR[slice_index_axial, :, :], cmap='gray')
plt.title('Cropped MR Image')
plt.axis('off')
plt.savefig("cropped_images.png")


img = nib.load('/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/Abdomen/imagesTr/img0016_tcia_CT.nii.gz')
data = img.get_fdata()

# Convert to PyTorch tensor and perform the operation
test_image_CT = torch.from_numpy(data)
test_image_CT -= test_image_CT.min()

# Convert back to NumPy array
test_image_CT_np = test_image_CT.numpy()

# Save the modified image using the original affine
nib.save(nib.Nifti1Image(test_image_CT_np, img.affine), 'test_image_CT.nii.gz')

test_image_CT = torch.from_numpy(nib.load('/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/Abdomen/imagesTr/img0016_tcia_CT.nii.gz').get_fdata())
test_image_MR = torch.from_numpy(nib.load('/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/Abdomen/imagesTr/img0016_tcia_MR.nii.gz').get_fdata())

print("CT min value:", test_image_CT.min())
print("CT max value:", test_image_CT.max())
print("MR min value:", test_image_MR.min())
print("MR max value:", test_image_MR.max())

# Adjust the intensity of the CT image to match the intensity of the MR image
adjusted_CT, adjusted_MR = adjust_values(test_image_CT, test_image_MR)
print("Adjusted CT min value:", adjusted_CT.min())
print("Adjusted CT max value:", adjusted_CT.max())
print("Adjusted MR min value:", adjusted_MR.min())
print("Adjusted MR max value:", adjusted_MR.max())
'''