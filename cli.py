import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from self_configuring.convex_run_withconfig import *
from self_configuring.adam_run_withconfig_shiftSpline import *
from self_configuring.infer_convexadam import *
import cmd

class MyPrompt(cmd.Cmd):
    prompt = "AMSIzziv>> "
    intro = "Welcome! Type help to list commands.\n"

    def __init__(self):
        super().__init__()
        
    def do_help(self, arg):
        """Display help for available commands."""
        print("Commands:\n")
        print("Two optimization methods are available: Convex and Adam. One will return course displacement field and the other will return fine displacement field.")
        print("Both methods will also return how well the two images are aligned using Dice coefficient, HD 95 and jacobi determinant.")
        print("  convex_run(gpu_id, path_to_config_file) - Run Convex optimization")
        print("  adam_run(gpu_id, path_to_config_file, convex_s) - Run Adam optimization")
        print("\n")
        print("After running the optimization, you can get the displacement field using the following command:")
        print("  get_displacement_field(gpu_id, path_to_config_file, convex_s, adam_s1, adam_s2) - Get displacement field")
        print("\n")
        print("Other commands:")
        print("  generate_config_file(method) - Generate a configuration file for Convex or Adam optimization")
        print("  apply_displacement_field(path_to_img1, path_to_img2, path_to_displacement_field, path_to_result_folder) - Apply displacement field to an image")
        print("  display_parameters() - Show meaning of parameters needed for each function")
        print("  exit - Exit the program")

    def do_exit(self, arg):
        """Exit the program."""
        print("Exiting...")
        return True


if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.cmdloop()