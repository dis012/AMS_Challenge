import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

# Normalize images for visualization
def normalize_image(img):
    img = img.astype(np.float32)
    return (img - np.min(img)) / (np.max(img) - np.min(img))

# Paths to the images and displacement field
moving_image_path = "/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/imagesTr/img0006_tcia_CT.nii.gz"
fixed_image_path = "/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/imagesTr/img0006_tcia_MR.nii.gz"
disp_field_path = "/home/adis/Desktop/Faks/AMS/AMS_Challenge/Results/Optimization_test_aligment/OptimizedAligment/results_testset/disp_06_06.nii.gz"

# Load the images
ct_image = sitk.ReadImage(moving_image_path)
mr_image = sitk.ReadImage(fixed_image_path)

# Load the displacement field as a scalar image
displacement_field_img = sitk.ReadImage(disp_field_path)

# Check the dimension and size
dimension = displacement_field_img.GetDimension()
size = displacement_field_img.GetSize()
print("Displacement field dimension:", dimension)
print("Displacement field size:", size)
print("Displacement field pixel type:", displacement_field_img.GetPixelIDTypeAsString())
print("Number of components per pixel:", displacement_field_img.GetNumberOfComponentsPerPixel())

# Convert displacement field to numpy array
displacement_field_array = sitk.GetArrayFromImage(displacement_field_img)
print("Displacement field array shape:", displacement_field_array.shape)

# Determine if the displacement field is 4D
if displacement_field_array.ndim == 4:
    # Assuming the displacement components are along the last axis
    # Reorder axes to match SimpleITK's expectations (z, y, x, c)
    displacement_field_array = np.transpose(displacement_field_array, (3, 2, 1, 0))
    
    # Now, create a vector image from the numpy array
    # Note: We need to ensure that the array shape is (z, y, x, c)
    displacement_field_vector = sitk.GetImageFromArray(displacement_field_array, isVector=True)
    
    # Copy spatial information from the fixed image
    displacement_field_vector.CopyInformation(ct_image)
    
    # Cast to the appropriate vector pixel type
    displacement_field_vector = sitk.Cast(displacement_field_vector, sitk.sitkVectorFloat64)
    
    # Convert the displacement field to a transform
    displacement_transform = sitk.DisplacementFieldTransform(displacement_field_vector)
    
    # Resample (warp) the MR image to align with the CT image
    warped_ct_image = sitk.Resample(
        ct_image,
        mr_image,  # Use the MR image as a reference
        displacement_transform,  # Displacement field transform
        sitk.sitkLinear,  # Interpolation method
        0.0,  # Default pixel value for areas outside the image
        mr_image.GetPixelID()  # Ensure output image type matches the MR image
    )
    
    # Save the warped MR image
    sitk.WriteImage(warped_ct_image, "warped_ct_image.nii.gz")
    print("Warped MR image saved as 'warped_ct_image.nii.gz'")
else:
    print("Displacement field is not 4D. Cannot proceed.")



# Convert images to numpy arrays
mr_image_array = sitk.GetArrayFromImage(mr_image)
warped_ct_image_array = sitk.GetArrayFromImage(warped_ct_image)
ct_image_array = sitk.GetArrayFromImage(ct_image)

mr_norm = normalize_image(mr_image_array)
warped_ct_norm = normalize_image(warped_ct_image_array)
ct_norm = normalize_image(ct_image_array)

# Define slice indices for each orientation
slice_index_axial = mr_image_array.shape[0] // 2    # Axial plane (depth)
slice_index_sagittal = mr_image_array.shape[2] // 2  # Sagittal plane (width)
slice_index_coronal = mr_image_array.shape[1] // 2   # Coronal plane (height)

# Axial slices
mr_axial = mr_norm[slice_index_axial, :, :]
warped_ct_axial = warped_ct_norm[slice_index_axial, :, :]
ct_axial = ct_norm[slice_index_axial, :, :]

# Sagittal slices (need to transpose for correct orientation)
ct_sagittal = np.transpose(ct_norm[:, :, slice_index_sagittal], (1, 0))
warped_ct_sagittal = np.transpose(warped_ct_norm[:, :, slice_index_sagittal], (1, 0))
mr_sagittal = np.transpose(mr_norm[:, :, slice_index_sagittal], (1, 0))

# Coronal slices (need to transpose for correct orientation)
mr_coronal = np.transpose(mr_norm[:, slice_index_coronal, :], (1, 0))
warped_ct_coronal = np.transpose(warped_ct_norm[:, slice_index_coronal, :], (1, 0))
ct_coronal = np.transpose(ct_norm[:, slice_index_coronal, :], (1, 0))

# Create a figure with 3 rows and 2 columns
fig, axs = plt.subplots(3, 2, figsize=(12, 18))

# Adjust spacing between subplots
plt.tight_layout()

# Axial plane
# Original MR and CT overlay
axs[0, 0].imshow(ct_axial, cmap='gray')
axs[0, 0].imshow(mr_axial, cmap='hot', alpha=0.5)
axs[0, 0].set_title('Axial Plane: MR and CT Overlay')
axs[0, 0].axis('off')

# Warped MR and CT overlay
axs[0, 1].imshow(mr_axial, cmap='gray')
axs[0, 1].imshow(warped_ct_axial, cmap='hot', alpha=0.5)
axs[0, 1].set_title('Axial Plane: Warped MR and CT Overlay')
axs[0, 1].axis('off')

# Sagittal plane
# Original MR and CT overlay
axs[1, 0].imshow(mr_sagittal, cmap='gray', aspect='auto')
axs[1, 0].imshow(ct_sagittal, cmap='hot', alpha=0.5, aspect='auto')
axs[1, 0].set_title('Sagittal Plane: MR and CT Overlay')
axs[1, 0].axis('off')

# Warped MR and CT overlay
axs[1, 1].imshow(mr_sagittal, cmap='gray', aspect='auto')
axs[1, 1].imshow(warped_ct_sagittal, cmap='hot', alpha=0.5, aspect='auto')
axs[1, 1].set_title('Sagittal Plane: Warped MR and CT Overlay')
axs[1, 1].axis('off')

# Coronal plane
# Original MR and CT overlay
axs[2, 0].imshow(ct_coronal, cmap='gray', aspect='auto')
axs[2, 0].imshow(mr_coronal, cmap='hot', alpha=0.5, aspect='auto')
axs[2, 0].set_title('Coronal Plane: MR and CT Overlay')
axs[2, 0].axis('off')

# Warped MR and CT overlay
axs[2, 1].imshow(mr_coronal, cmap='grey', aspect='auto')
axs[2, 1].imshow(warped_ct_coronal, cmap='hot', alpha=0.5, aspect='auto')
axs[2, 1].set_title('Coronal Plane: Warped MR and CT Overlay')
axs[2, 1].axis('off')

# Save and display the figure
plt.savefig("overlapping_slices.png")
plt.show()


'''
# Testing
seg_path = "/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/masksTr/segxxxx_tcia_CT.nii.gz"
labels = ['0002', '0004', '0006', '0008', '0010', '0012', '0014', '0016']


for label in labels:
    seg_mask = nib.load(seg_path.replace('xxxx', label)).get_fdata()
    unique_labels = np.unique(seg_mask)
    #print("Unique labels in the segmentation mask:", unique_labels)

    num_labels = len(unique_labels)
    print(f'Number of labels in the segmentation mask {label}:', num_labels)
    print(f'Maximum value in the segmentation mask {label}:', np.max(seg_mask))
    print(f'Minimum value in the segmentation mask {label}:', np.min(seg_mask))


# Load the saved file with ranking
metrics_data = torch.load("/home/adis/Desktop/Faks/AMS/AMS_Challenge/Results/Output/optimized_params.pt")

# Access each metric by index
ranking = metrics_data[0]  # Ranked performance of parameter settings
dice_scores = metrics_data[1]  # Dice coefficients
jacobian_std_dev = metrics_data[2]  # Jacobian standard deviation
hausdorff_95 = metrics_data[3]  # HD95 values
computation_time = metrics_data[4]  # Computation time per run

best_ranking_index = ranking.argmax()

# Analyze each metric
print("Best ranking index:", best_ranking_index + 1)
print("Best ranking:", ranking[best_ranking_index])
print("Best Dice score:", dice_scores[best_ranking_index])
print("Best Jacobian standard deviation:", jacobian_std_dev[best_ranking_index])
print("Best HD95 value:", hausdorff_95[best_ranking_index])
print("Best computation time:", computation_time[best_ranking_index])
'''