import torch
import nibabel as nib
import torch.nn.functional as F
import matplotlib.pyplot as plt

# Images to be registered
moving_image_path = (
    "/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/imagesTr/img0002_tcia_MR.nii.gz"
)
fixed_image_path = (
    "/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/imagesTr/img0002_tcia_CT.nii.gz"
)

# Displacement field
disp_field_path = "/home/adis/Desktop/Faks/AMS/AMS_Challenge/Results/initial_test/results_testset/disp_2_tc_2_tc.nii.gz"

# Load images
moving_image = nib.load(moving_image_path)
fixed_image = nib.load(fixed_image_path)
disp_field = nib.load(disp_field_path)

print("Moving image shape:", moving_image.shape)
print("Fixed image shape:", fixed_image.shape)
print("Displacement field shape:", disp_field.shape)

# Convert images to tensors
moving_image_tensor = (
    torch.tensor(moving_image.get_fdata()).unsqueeze(0).unsqueeze(0).float()
)
disp_field_tensor = torch.tensor(disp_field.get_fdata()).float()

print("Moving image tensor shape:", moving_image_tensor.shape)
print("Displacement field tensor shape:", disp_field_tensor.shape)

# Create grid based on displacement field
D, H, W = disp_field_tensor.shape[:3]
grid = torch.meshgrid(torch.arange(D), torch.arange(H), torch.arange(W), indexing="ij")
grid = torch.stack(grid, dim=-1).float() + disp_field_tensor

# Normalize grid
grid[..., 0] = 2 * grid[..., 0] / (D - 1) - 1 # Normalize along the z-axis
grid[..., 1] = 2 * grid[..., 1] / (H - 1) - 1 # Normalize along the y-axis
grid[..., 2] = 2 * grid[..., 2] / (W - 1) - 1 # Normalize along the x-axis

# Reshape grid to match grid expected by grid_sample and apply transformation
grid = grid.unsqueeze(0)
aligned_image_tensor = F.grid_sample(
    moving_image_tensor, grid, align_corners=True, mode="bilinear"
)  # Interpolation method

# Convert to numpy array and save
aligned_image = aligned_image_tensor.squeeze().cpu().numpy()
# nib.save(
#    nib.Nifti1Image(aligned_image, nib.load(moving_image_path).affine),
#    "aligned_image.nii.gz",
# )

# Choose a specific slice index (e.g., middle slice along z-axis)
slice_index = moving_image.shape[2] // 2  # Adjust to use the middle slice

# Plot all images side by side with the specified slice
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(moving_image.get_fdata()[..., slice_index], cmap="gray")
plt.title("Moving image")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(aligned_image[..., slice_index], cmap="gray")
plt.title("Aligned image")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(fixed_image.get_fdata()[..., slice_index], cmap="gray")
plt.title("Fixed image")
plt.axis("off")

# Save the figure
# plt.savefig("displacement_field_visualization.png")
