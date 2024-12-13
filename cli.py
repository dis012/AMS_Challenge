import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from self_configuring.convex_run_withconfig import main as convex_run_Unet
from self_configuring.adam_run_withconfig_shiftSpline import main as adam_run_Unet
from self_configuring.infer_convexadam import main as get_displacement_field_Unet
from self_configuring.convex_run_paired_mind import main as convex_run_MIND
from self_configuring.adam_run_paired_mind_shiftSpline import main as adam_run_MIND
from self_configuring.main_for_l2r3_MIND_testset import main as get_displacement_field_MIND
from self_configuring.helper_functions import apply_displacement_field 
import cmd


class MyPrompt(cmd.Cmd):
    prompt = "AMSIzziv>> "
    intro = "Welcome! Type help to list commands.\n"

    def __init__(self):
        super().__init__()

    def do_help(self, arg):
        """Display help for available commands."""
        print("Commands:\n")
        print(
            "Two optimization methods are available: Convex and Adam. One will return course displacement field and the other will return fine displacement field."
        )
        print(
            "Both methods will also return how well the two images are aligned using Dice coefficient, HD 95 and jacobi determinant."
        )
        print(
            "  convex_run_Unet(gpu_id, path_to_config_file) - Run Convex optimization"
        )
        print(
            "  adam_run_Unet(gpu_id, path_to_config_file, convex_s) - Run Adam optimization"
        )
        print(
            "  convex_run_MIND(gpu_id, path_to_config_file) - Run Convex optimization"
        )
        print(
            "  adam_run_MIND(gpu_id, path_to_config_file, convex_s) - Run Adam optimization"
        )
        print("\n")
        print(
            "After running the optimization, you can get the displacement field using the following command:"
        )
        print(
            "  get_displacement_field_Unet(gpu_id, path_to_config_file, convex_s, adam_s1, adam_s2) - Get displacement field"
        )
        print(
            "  get_displacement_field_MIND(task, mindr, mindd, usemask, lambda, gridsp, disphw, iterations, smoothnes, data, results) - Get displacement field"
        )
        print("\n")
        print("Other commands:")
        print(
            "  apply_displacement_field(path_to_fixed, path_to_moving, path_to_displacement_field, path_to_result_folder) - Apply displacement field to an image"
        )
        print(
            "  display_parameters() - Show meaning of parameters needed for each function"
        )
        print("  exit - Exit the program")

    def do_exit(self, arg):
        """Exit the program."""
        print("Exiting...")
        return True

    def do_display_parameters(self, arg):
        """Display the meaning of parameters needed for each function."""
        print("Parameters:\n" "")
        print("disp_hw: Determines the maximum number of voxels the moving image can shihft in each direction during registration.")
        print("grid_sp: Determines the downsampling factor.")
        print("n_ch: Number of feature channels in MIND descriptors.")
        print("H, W, D: Dimensions of the input image.")
        print("nn_mult: Determines the number of feature channels in the fixed image.")
        print("convex_s: Determines parameters index that you get by running convex optimization.")
        print("adam_s1: Determines parameters index that you get by running adam optimization.")
        print("adam_s2: Determines parameters index that you get by running adam optimization.")
        print("gpu_id: Determines the GPU that will be used for the optimization.")
        print("path_to_config_file: Path to the configuration file.")
        print("mind_r: Determines the radius of the MIND descriptor.")
        print("mind_d: Determines the distance between the two MIND descriptors.")
        print("use_mask: Determines whether to use mask.")
        print("grid_sp_adam: Determines the downsampling factor for Adam optimization.")

    def do_convex_run_Unet(self, arg):
        """Run Convex optimization."""
        gpu_id = int(input("Enter GPU ID: "))
        path_to_config_file = "/app/Data/AMS_Images/ThoraxCBCT_OncoRegRelease_06_12_23/Release_06_12_23/convex_config_unet.json"
        convex_run_Unet(gpu_id, path_to_config_file)

    def do_adam_run_Unet(self, arg):
        """Run Adam optimization."""
        gpu_id = int(input("Enter GPU ID: "))
        path_to_config_file = "/app/Data/AMS_Images/ThoraxCBCT_OncoRegRelease_06_12_23/Release_06_12_23/convex_config_unet.json"
        convex_s = int(input("Enter convex_s: "))
        adam_run_Unet(gpu_id, path_to_config_file, convex_s)

    def do_get_displacement_field_Unet(self, arg):
        """Get displacement field."""
        gpu_id = int(input("Enter GPU ID: "))
        path_to_config_file = "/app/Data/AMS_Images/ThoraxCBCT_OncoRegRelease_06_12_23/Release_06_12_23/ConfigDisplacementFieldUNet.json"
        convex_s = int(input("Enter convex_s: "))
        adam_s1 = int(input("Enter adam_s1: "))
        adam_s2 = int(input("Enter adam_s2: "))
        get_displacement_field_Unet(gpu_id, path_to_config_file, convex_s, adam_s1, adam_s2)

    def do_convex_run_MIND(self, arg):
        """Run Convex optimization."""
        gpu_id = int(input("Enter GPU ID: "))
        path_to_config_file = "/app/Data/AMS_Images/ThoraxCBCT_OncoRegRelease_06_12_23/Release_06_12_23/convex_config.json"
        convex_run_MIND(gpu_id, path_to_config_file)

    def do_adam_run_MIND(self, arg):
        """Run Adam optimization."""
        gpu_id = int(input("Enter GPU ID: "))
        path_to_config_file = "/app/Data/AMS_Images/ThoraxCBCT_OncoRegRelease_06_12_23/Release_06_12_23/adam_config.json"
        convex_s = int(input("Enter convex_s: "))
        adam_run_MIND(gpu_id, path_to_config_file, convex_s)

    def do_get_displacement_field_MIND(self, arg):
        """Get displacement field."""
        task_name = input("Enter task name: ")
        mind_r = int(input("Enter mind_r: "))
        mind_d = int(input("Enter mind_d: "))
        use_mask = bool(input("Enter use_mask: "))
        lambda_weight = float(input("Enter lambda_weight: "))
        grid_sp = int(input("Enter grid_sp: "))
        disp_hw = int(input("Enter disp_hw: "))
        selected_niter = int(input("Enter selected_niter: "))
        selected_smooth = int(input("Enter selected_smooth: "))
        data_dir = "app/Data/"
        result_path = "/app/Results/DisplacementFieldMIND/"
        get_displacement_field_MIND(
            task_name,
            mind_r,
            mind_d,
            use_mask,
            lambda_weight,
            grid_sp,
            disp_hw,
            selected_niter,
            selected_smooth,
            data_dir,
            result_path,
        )

    def do_apply_displacement_field(self, arg):
        """Apply displacement field to an image."""
        path_to_fixed = input("Enter path to fixed image: ")
        path_to_moving = input("Enter path to moving image: ")
        path_to_displacement_field = input("Enter path to displacement field: ")
        path_to_result_folder = "/app/Results/WarpedImages/"
        apply_displacement_field(
            path_to_fixed, path_to_moving, path_to_displacement_field, path_to_result_folder
        )

if __name__ == "__main__":
    prompt = MyPrompt()
    prompt.cmdloop()
