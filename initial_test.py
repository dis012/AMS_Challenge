import sys

sys.path.append("/home/adis/Desktop/Faks/AMS/AMS_Challenge/src")

from self_configuring.main_for_l2r3_MIND_testset import main

task_name = "initial_test"
mind_r = 3
mind_d = 2
use_mask = True
lambda_weight = 1.0
grid_sp = 6
disp_hw = 6
selected_niter = 80
selected_smooth = 5
data_dir = "/home/adis/Desktop/Faks/AMS/AMS_Challenge/Data/"
result_path = "/home/adis/Desktop/Faks/AMS/AMS_Challenge/Results/"

main(
    task_name=task_name,
    mind_r=mind_r,
    mind_d=mind_d,
    use_mask=use_mask,
    lambda_weight=lambda_weight,
    grid_sp=grid_sp,
    disp_hw=disp_hw,
    selected_niter=selected_niter,
    selected_smooth=selected_smooth,
    data_dir=data_dir,
    result_path=result_path,
)
