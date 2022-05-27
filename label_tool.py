import cv2, csv
import pickle
import numpy as np
import os
import os.path as osp

cwd = os.getcwd()
file_names = os.listdir(cwd + "/frames/")
fields = ['img', 'label']

for file_name in file_names:
    with open("frames/" + file_name, 'rb') as handle:
        frame_data = pickle.load(handle)
        color_image = frame_data['rgb']

    global click_count
    click_count = 0
    global gripper_pose
    gripper_pose = []

    def click_event(event, x, y, flags, params):
        global click_count
        global gripper_pose
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(color_image, (x, y), 10, (0, 0, 255), -1)
            cv2.imshow('image', color_image)
            click_count += 1
            gripper_pose.append([x, y])
            print([x, y])
        if click_count == 2:
            # with open('{}/frames_labeled/{}_gripper.npy'.format(file_name), 'wb') as f:
            #     np.save(f, gripper_pose)
            
            newrow = {'img': file_name, 'label': gripper_pose}
            with open('labels.csv', "a", newline='') as file:
                writer = csv.DictWriter(file, fieldnames = fields) 
                writer.writerow(newrow)
            cv2.destroyAllWindows()

    cv2.namedWindow('image')
    cv2.imshow('image', color_image)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)