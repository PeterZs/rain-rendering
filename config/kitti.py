import os

import numpy as np


def _sequences(params):
    # Recursively find all children folders
    sequences = np.array([x[0][len(params.images_root) + 1:] for x in os.walk(os.path.join(params.images_root))])

    # Find directories that have subdirectory image_2 AND calib
    cond1 = [os.path.exists(os.path.join(params.images_root, p, 'image_2')) & os.path.exists(
        os.path.join(params.images_root, p, 'calib')) for p in sequences]
    # Find directories that have image_02 (typically, raw data)
    cond2 = [os.path.exists(os.path.join(params.images_root, p, 'image_02')) and p[-len("_sync"):] == "_sync" for p in sequences]

    return sequences[np.bitwise_or(cond1, cond2)]

def resolve_paths(params):
    params.sequences = _sequences(params)
    assert (len(params.sequences) > 0), "There are no valid sequences folder in the dataset root. Maybe you forgot to download calibration files ?"

    params.images = {}
    params.calib = {}
    params.depth = {}
    for sequence in params.sequences:
        # Setting path. Kitti paths depends on the nature of the sequence
        if sequence[:len('raw_data')] == 'raw_data':
            # Source images
            params.images[sequence] = os.path.join(params.dataset_root, sequence, 'image_02', 'data')

            # Setting dir of calib files of frames
            params.calib[sequence] = os.path.join(params.dataset_root, sequence, os.path.pardir, 'calib_cam_to_cam.txt')

            # Depth dir
            params.depth[sequence] = os.path.join(params.images[sequence], 'depth')
        else:
            # Source images
            params.images[sequence] = os.path.join(params.dataset_root, sequence, 'image_2')

            # Setting dir of calib files of frames
            calib_folder = os.path.join(params.dataset_root, sequence, 'calib')
            params.calib[sequence] = [os.path.join(calib_folder, calib_txt) for calib_txt in os.listdir(calib_folder) if calib_txt.endswith('.txt')]

            # Depth dir
            params.depth[sequence] = os.path.join(params.images[sequence], 'depth')

    return params

def settings():
    settings = {}

    # Camera intrinsic parameters
    settings["cam_hz"] = 10   # Camera Hz (aka FPS)
    settings["cam_CCD_WH"] = [1242, 375]  # Camera CDD Width and Height (pixels)
    settings["cam_CCD_pixsize"] = 4.65  # Camera CDD pixel size (micro meters)
    settings["cam_WH"] = [1242, 375]  # Camera image Width and Height (pixels)
    settings["cam_focal"] = 6  # Focal length (mm)
    settings["cam_gain"] = 20  # Camera gain
    settings["cam_f_number"] = 6.0  # F-Number
    settings["cam_focus_plane"] = 6.0  # Focus plane (meter)
    settings["cam_exposure"] = 2  # Camera exposure (ms)

    # Camera extrinsic parameters (right-handed coordinate system)
    settings["cam_pos"] = [1.5, 1.5, 0.3]  # Camera pos (meter)
    settings["cam_lookat"] = [1.5, 1.5, -1.]  # Camera look at vector (meter)
    settings["cam_up"] = [0., 1., 0.]  # Camera up vector (meter)

    # Sequence-wise settings
    # Note: sequence object and settings are merged, hence any setting can be overwriten sequence-wise
    settings["sequences"] = {}
    settings["sequences"]["data_object"] = {}
    settings["sequences"]["data_object"]["sim_mode"] = "steps"
    settings["sequences"]["data_object"]["sim_steps"] = {"cam_motion": np.arange(100., 0.-1, -1)}  # Since data_object sequence lack speed data, we assume random speed between 100km/hr and 0km/hr

    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0032_sync"] = {}
    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0032_sync"]["sim_mode"] = "steps"
    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0032_sync"]["sim_steps"] = {"cam_motion": [75.4540, 75.6891, 75.9360, 76.1820, 76.4361, 76.6756, 76.9000, 77.0922, 77.2566, 77.4022, 77.5339, 77.6448, 77.7297, 77.7848, 77.8145, 77.8282, 77.8263, 77.8171, 77.8142, 77.8432, 77.9221, 78.0430, 78.1868, 78.3444, 78.5180, 78.7042, 78.8982, 79.0898, 79.2715, 79.4376, 79.5860, 79.7165, 79.8358, 79.9341, 80.0264, 80.0856, 80.1453, 80.2359, 80.3747, 80.5243, 80.6461, 80.7681, 80.9085, 81.0547, 81.1737, 81.2837, 81.4050, 81.5445, 81.6745, 81.7937, 81.9314, 82.0943, 82.2716, 82.4320, 82.5741, 82.7058, 82.8268, 82.9780, 83.1517, 83.3503, 83.5417, 83.7235, 83.9011, 84.0857, 84.2741, 84.4564, 84.6409, 84.8429, 85.0455, 85.2050, 85.3298, 85.4478, 85.5689, 85.6770, 85.7638, 85.8354, 85.8991, 85.9650, 86.0274, 86.0901, 86.1589, 86.2402, 86.3293, 86.4122, 86.4890, 86.5422, 86.5813, 86.6098, 86.6261, 86.6186, 86.5838, 86.5378, 86.4966, 86.4480, 86.3771, 86.2995, 86.2277, 86.1755, 86.1250, 86.0819, 86.0430, 86.0133, 85.9841, 85.9627, 85.9506, 85.9468, 85.9430, 85.9312, 85.9130, 85.8940, 85.8669, 85.8325, 85.7884, 85.7283, 85.6536, 85.5769, 85.4971, 85.4189, 85.3232, 85.2088, 85.0844, 84.9609, 84.8493, 84.7405, 84.6311, 84.5360, 84.4564, 84.3930, 84.3368, 84.2781, 84.2195, 84.1554, 84.0883, 84.0188, 83.9432, 83.8507, 83.7402, 83.6164, 83.4972, 83.3895, 83.2928, 83.2006, 83.0789, 82.9152, 82.7003, 82.4674, 82.2010, 81.8991, 81.5291, 81.0809, 80.5659, 79.9905, 79.3672, 78.7036, 78.0080, 77.2237, 76.3697, 75.4267, 74.4810, 73.5443, 72.6262, 71.6750, 70.6485, 69.5232, 68.3872, 67.2810, 66.1733, 65.0571, 63.9679, 63.1249, 62.5838, 62.3247, 62.2058, 62.1093, 61.9767, 61.8230, 61.6714, 61.5337, 61.3964, 61.2614, 61.1358, 61.0162, 60.8841, 60.7434, 60.5983, 60.4632, 60.3280, 60.1952, 60.0698, 59.9471, 59.8092, 59.6603, 59.5122, 59.3772, 59.2565, 59.1356, 59.0130, 58.8892, 58.7622, 58.6344, 58.5064, 58.3813, 58.2525, 58.1022, 57.9470, 57.8138, 57.7171, 57.6189, 57.4853, 57.3030, 57.1138, 56.9217, 56.7202, 56.4967, 56.2742, 56.0782, 55.9221, 55.8004, 55.7038, 55.6115, 55.4953, 55.3671, 55.2217, 55.0633, 54.8733, 54.6726, 54.4811, 54.3232, 54.1790, 54.0428, 53.9147, 53.8024, 53.7003, 53.5983, 53.5167, 53.4623, 53.4264, 53.3799, 53.3317, 53.3024, 53.3338, 53.4060, 53.4943, 53.5662, 53.6416, 53.7564, 53.9226, 54.1357, 54.3796, 54.6584, 54.9706, 55.2796, 55.5475, 55.8167, 56.1180, 56.4649, 56.8137, 57.1426, 57.4523, 57.7370, 57.9921, 58.2258, 58.4301, 58.6241, 58.8111, 58.9844, 59.1460, 59.3119, 59.4924, 59.6498, 59.7721, 59.9036, 60.1127, 60.3832, 60.6874, 61.0075, 61.3408, 61.6745, 61.9850, 62.2699, 62.5813, 62.9387, 63.3446, 63.7634, 64.1623, 64.5408, 64.9065, 65.2887, 65.7003, 66.1246, 66.5255, 66.9032, 67.2842, 67.6863, 68.1036, 68.4778, 68.8048, 69.1077, 69.4087, 69.7017, 69.9548, 70.1446, 70.2917, 70.4242, 70.5493, 70.6351, 70.6820, 70.7336, 70.8321, 70.9554, 71.0766, 71.1698, 71.2436, 71.3371, 71.4926, 71.6924, 71.9001, 72.0907, 72.2849, 72.4813, 72.6879, 72.9259, 73.2060, 73.4735, 73.7003, 73.8931, 74.0949, 74.3153, 74.5472, 74.7738, 74.9811, 75.1558, 75.3067, 75.4321, 75.5314, 75.6046, 75.6575, 75.6934, 75.7421, 75.8063, 75.8910, 75.9697, 76.0560, 76.1940, 76.3788, 76.5685, 76.7127, 76.8435, 77.0002, 77.2178, 77.4520, 77.6793, 77.8775, 78.0738, 78.2833, 78.5188, 78.7711, 79.0374, 79.3065, 79.5373, 79.7177, 79.8667, 80.0220, 80.1723, 80.2781, 80.3384, 80.3741, 80.3844, 80.3766, 80.3488, 80.3111, 80.2514, 80.1690, 80.1048, 80.0534, 79.9894, 79.8701, 79.7231, 79.6071, 79.5283, 79.4717, 79.4145, 79.3508, 79.2897, 79.2318, 79.1816, 79.1491, 79.1254, 79.1114]}

    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0056_sync"] = {}
    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0056_sync"]["sim_mode"] = "steps"
    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0056_sync"]["sim_steps"] = {"cam_motion": [61.4892, 61.9218, 62.3442, 62.7895, 63.2573, 63.7361, 64.1694, 64.5797, 64.9629, 65.3412, 65.6958, 66.0225, 66.3107, 66.5847, 66.8496, 67.0967, 67.3008, 67.4664, 67.6073, 67.7322, 67.8445, 67.9545, 68.0744, 68.1954, 68.2868, 68.3240, 68.3038, 68.2510, 68.1904, 68.1204, 68.0388, 67.9480, 67.8571, 67.7770, 67.7063, 67.6436, 67.5817, 67.5195, 67.4698, 67.4556, 67.4906, 67.5789, 67.6960, 67.8268, 67.9731, 68.1446, 68.3449, 68.5622, 68.7754, 68.9931, 69.2300, 69.4946, 69.7687, 70.0146, 70.2370, 70.4297, 70.5861, 70.6947, 70.7756, 70.8547, 70.9636, 71.0806, 71.1437, 71.1145, 71.0279, 70.9810, 70.9973, 71.0385, 71.0635, 71.0774, 71.0950, 71.1255, 71.1759, 71.2478, 71.3371, 71.4344, 71.5318, 71.6008, 71.6711, 71.7850, 71.9544, 72.1269, 72.2846, 72.4541, 72.6339, 72.8049, 72.9797, 73.1841, 73.4176, 73.6617, 73.9036, 74.1516, 74.4024, 74.6505, 74.9064, 75.1846, 75.4904, 75.8101, 76.1225, 76.4032, 76.6426, 76.8369, 76.9916, 77.0877, 77.1099, 77.0766, 77.0061, 76.9108, 76.8037, 76.6847, 76.5606, 76.4127, 76.2538, 76.0985, 75.9576, 75.8108, 75.6225, 75.4063, 75.1738, 75.0066, 74.8997, 74.8043, 74.6800, 74.5321, 74.4140, 74.3343, 74.2854, 74.2687, 74.2454, 74.1925, 74.0974, 73.9609, 73.8106, 73.6457, 73.4840, 73.3298, 73.1768, 73.0117, 72.8379, 72.6622, 72.4827, 72.3002, 72.1340, 71.9934, 71.8608, 71.7285, 71.5918, 71.4556, 71.3002, 71.1410, 71.0193, 70.9328, 70.8246, 70.6757, 70.5224, 70.4136, 70.3165, 70.2219, 70.1148, 69.9976, 69.8787, 69.8015, 69.7652, 69.7545, 69.7499, 69.7722, 69.8389, 69.9312, 70.0297, 70.1307, 70.2446, 70.3863, 70.5535, 70.7214, 70.8539, 70.9194, 70.9316, 70.9098, 70.8620, 70.7920, 70.6972, 70.5990, 70.4867, 70.3581, 70.1761, 69.9611, 69.7106, 69.4514, 69.1779, 68.9115, 68.6549, 68.4297, 68.2369, 68.0654, 67.8939, 67.7102, 67.5206, 67.3352, 67.1691, 67.0150, 66.8781, 66.7836, 66.7432, 66.7488, 66.7585, 66.7882, 66.8329, 66.8988, 66.9725, 67.0604, 67.1608, 67.2538, 67.3203, 67.3445, 67.3404, 67.3072, 67.2449, 67.1560, 67.0426, 66.9287, 66.8257, 66.7532, 66.7166, 66.7216, 66.7699, 66.8533, 66.9449, 67.0393, 67.1462, 67.2738, 67.4113, 67.5519, 67.6943, 67.8388, 67.9813, 68.1259, 68.2758, 68.4336, 68.5938, 68.7556, 68.9088, 69.0576, 69.2125, 69.3713, 69.5335, 69.6861, 69.8433, 69.9991, 70.1592, 70.3209, 70.4859, 70.6548, 70.8144, 70.9670, 71.1188, 71.2815, 71.4491, 71.6098, 71.7619, 71.9060, 72.0545, 72.2001, 72.3339, 72.4483, 72.5515, 72.6516, 72.7434, 72.8245, 72.8992, 72.9754, 73.0445, 73.1009, 73.1345, 73.1452, 73.1391, 73.1172, 73.0764, 73.0134, 72.9402, 72.8642, 72.7807, 72.6849, 72.5779, 72.4655, 72.3520, 72.2254, 72.0881, 71.9401, 71.8055, 71.6867, 71.5821, 71.4881, 71.4048]}

    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0071_sync"] = {}
    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0071_sync"]["sim_mode"] = "steps"
    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0071_sync"]["sim_steps"] = {"cam_motion": [3.5558, 3.7076, 3.8410, 3.9435, 3.9807, 3.8975, 3.6913, 3.4416, 3.1922, 2.9523, 2.6961, 2.4206, 2.1408, 1.8996, 1.8145, 1.9249, 2.2126, 2.5618, 2.9137, 3.2536, 3.5846, 3.9193, 4.2504, 4.5850, 4.9552, 5.3649, 5.8397, 6.3930, 7.0152, 7.7178, 8.4195, 9.1227, 9.8022, 10.4715, 11.1301, 11.7290, 12.2862, 12.8106, 13.3268, 13.8812, 14.4191, 14.9095, 15.3065, 15.6315, 15.9183, 16.1639, 16.3872, 16.5969, 16.7781, 16.9467, 17.0962, 17.2362, 17.3551, 17.4391, 17.4940, 17.5210, 17.5463, 17.5734, 17.5991, 17.6087, 17.5978, 17.5849, 17.5684, 17.4905, 17.2358, 16.7271, 16.0301, 15.2358, 14.4112, 13.5773, 12.7115, 11.8430, 10.9353, 9.9869, 8.9992, 7.9695, 6.8885, 5.8217, 4.8951, 4.3038, 4.0365, 4.0106, 4.0771, 4.1700, 4.2611, 4.3484, 4.4330, 4.5246, 4.6394, 4.7977, 4.9997, 5.2619, 5.5745, 5.9522, 6.3873, 6.8522, 7.3560, 7.8692, 8.4070, 8.9537, 9.5002, 10.0470, 10.6002, 11.1672, 11.7892, 12.4387, 13.1364, 13.8644, 14.5991, 15.3583, 16.0897, 16.8067, 17.4859, 18.0945, 18.5903, 18.9282, 19.1417, 19.2852, 19.3948, 19.5060, 19.6298, 19.7648, 19.9075, 20.0386, 20.1602, 20.2605, 20.3191, 20.3283, 20.2755, 20.1918, 20.0777, 19.9693, 19.8513, 19.7226, 19.5840, 19.4447, 19.3103, 19.1668, 19.0237, 18.8953, 18.7959, 18.7527, 18.7775, 18.8622, 18.9596, 19.0398, 19.0990, 19.1627, 19.2359, 19.3285, 19.4249, 19.5238, 19.5808, 19.5777, 19.5080, 19.4095, 19.3081, 19.2176, 19.1328, 19.0513, 18.9893, 18.9313, 18.8604, 18.7611, 18.6517, 18.5593, 18.4742, 18.3808, 18.2723, 18.1449, 18.0064, 17.8527, 17.6845, 17.5118, 17.3321, 17.1612, 16.9946, 16.8224, 16.6268, 16.3787, 16.0876, 15.7680, 15.4681, 15.2138, 15.0057, 14.8200, 14.6522, 14.4989, 14.3605, 14.2078, 14.0156, 13.7910, 13.5631, 13.3706, 13.2171, 13.0836, 12.9632, 12.8506, 12.7521, 12.6670, 12.5938, 12.5284, 12.4622, 12.3964, 12.3389, 12.2956, 12.2655, 12.2419, 12.2221, 12.2055, 12.1931, 12.1836, 12.1744, 12.1595, 12.1372, 12.1035, 12.0615, 12.0209, 11.9859, 11.9626, 11.9493, 11.9431, 11.9391, 11.9326, 11.9269, 11.9231, 11.9279, 11.9376, 11.9510, 11.9643, 11.9755, 11.9819, 11.9848, 11.9854, 11.9784, 11.9614, 11.9542, 11.9744, 12.0146, 12.0573, 12.0865, 12.1018, 12.0979, 12.0893, 12.0947, 12.1075, 12.0913, 12.0426, 11.9868, 11.9549, 11.9471, 11.9485, 11.9729, 12.0073, 12.0467, 12.0925, 12.1353, 12.1920, 12.2370, 12.2577, 12.2646, 12.2797, 12.3359, 12.4184, 12.5077, 12.5838, 12.6551, 12.7068, 12.7580, 12.7910, 12.8382, 12.8647, 12.8933, 12.9496, 13.0647, 13.1980, 13.3303, 13.4460, 13.5974, 13.7565, 13.9109, 14.0205, 14.0775, 14.0930, 14.1006, 14.1034, 14.0449, 13.8716, 13.5535, 13.1325, 12.6942, 12.3665, 12.1975, 12.1360, 12.1077, 12.0758, 12.0429, 11.9987, 11.9472, 11.8840, 11.8277, 11.7878, 11.7715, 11.7546, 11.7421, 11.7186, 11.6142, 11.2434, 10.5534, 9.5773, 8.6104, 7.7821, 7.1582, 6.6435, 6.1482, 5.6683, 5.1853, 4.7225, 4.3248, 4.0210, 3.8154, 3.6610, 3.5425, 3.4693, 3.4270, 3.4038, 3.3807, 3.3785, 3.4170, 3.4930, 3.5675, 3.6030, 3.5861, 3.5274, 3.4537, 3.4091, 3.4053, 3.4278, 3.4376, 3.4091, 3.3361, 3.2588, 3.2151, 3.2435, 3.3393, 3.4985, 3.6897, 3.8919, 4.0950, 4.2963, 4.4924, 4.6791, 4.8566, 5.0312, 5.1974, 5.3631, 5.5430, 5.7545, 6.0238, 6.3323, 6.6639, 6.9944, 7.3104, 7.6032, 7.8573, 8.0843, 8.3206, 8.5733, 8.8472, 9.1302, 9.4154, 9.6988, 9.9574, 10.1959, 10.4162, 10.6160, 10.8077, 11.0064, 11.2138, 11.4112, 11.5772, 11.7222, 11.8491, 11.9337, 11.9782, 11.9977, 12.0193, 12.0345, 12.0383, 12.0367, 12.0340, 12.0232, 11.9983, 11.9731, 11.9513, 11.9238, 11.8933, 11.8605, 11.8291, 11.7731, 11.6901, 11.6036, 11.5340, 11.4801, 11.4247, 11.3574, 11.2912, 11.2316, 11.1981, 11.2416, 11.4150, 11.7334, 12.1100, 12.4742, 12.8090, 13.1417, 13.4905, 13.8192, 14.1230, 14.3978, 14.6608, 14.9451, 15.2497, 15.5872, 15.9601, 16.3501, 16.7505, 17.1197, 17.4833, 17.8529, 18.2216, 18.5982, 18.9642, 19.3282, 19.6914, 20.0453, 20.4086, 20.7603, 21.1089, 21.4558, 21.8003, 22.1381, 22.4683, 22.7451, 22.9430, 23.0430, 23.0752, 23.0603, 23.0205, 22.9793, 22.9285, 22.8634, 22.7582, 22.6274, 22.4756, 22.3311, 22.2185, 22.1143, 22.0016, 21.8714, 21.7259, 21.5918, 21.4555, 21.3232, 21.1806, 21.0228, 20.8558, 20.6857, 20.5055, 20.3191, 20.1089, 19.8805, 19.6213, 19.3228, 19.0043, 18.6656, 18.3403, 18.0265, 17.7215, 17.4067, 17.0603, 16.7068, 16.3505, 15.9963, 15.6409, 15.2885, 14.9411, 14.5961, 14.2372, 13.8883, 13.5427, 13.2097, 12.9008, 12.6358, 12.4285, 12.2659, 12.1301, 12.0063, 11.8828, 11.7606, 11.6527, 11.5558, 11.4653, 11.3733, 11.2837, 11.1961, 11.1073, 11.0120, 10.9042, 10.7810, 10.6539, 10.5242, 10.3977, 10.2801, 10.1878, 10.1230, 10.0623, 9.9827, 9.8849, 9.7856, 9.6934, 9.6122, 9.5377, 9.4727, 9.4052, 9.3316, 9.2576, 9.1852, 9.1223, 9.0670, 9.0117, 8.9435, 8.8433, 8.7107, 8.5419, 8.3441, 8.1400, 7.9351, 7.7445, 7.5560, 7.3625, 7.1734, 7.0017, 6.8693, 6.7606, 6.6665, 6.5905, 6.5365, 6.5035, 6.4825, 6.4653, 6.4456, 6.4189, 6.3893, 6.3691, 6.3628, 6.3638, 6.3693, 6.3739, 6.3826, 6.4001, 6.4289, 6.4631, 6.4895, 6.5051, 6.5168, 6.5260, 6.5296, 6.5278, 6.5154, 6.4989, 6.4826, 6.4714, 6.4487, 6.4023, 6.3324, 6.2443, 6.1455, 6.0306, 5.9075, 5.7979, 5.7076, 5.6380, 5.5718, 5.5316, 5.5367, 5.5586, 5.5712, 5.5922, 5.6427, 5.7346, 5.8373, 5.9371, 6.0451, 6.1585, 6.2907, 6.4222, 6.5246, 6.5899, 6.6295, 6.6490, 6.6501, 6.6399, 6.6299, 6.6259, 6.6173, 6.6173, 6.5412, 6.3263, 5.9416, 5.4846, 4.9976, 4.4718, 3.8993, 3.2615, 2.6022, 1.8978, 1.1201, 0.5961, 0.2585, 0.1897, 0.0939, 0.0745, 0.0604, 0.0475, 0.0402, 0.0639, 0.0736, 0.0657, 0.0687, 0.0774, 0.0815, 0.0866, 0.0957, 0.1008, 0.1006, 0.0997, 0.1004, 0.0965, 0.0976, 0.0977, 0.0967, 0.0958, 0.0970, 0.0975, 0.0968, 0.0977, 0.0987, 0.0996, 0.1013, 0.1010, 0.0983, 0.0916, 0.0839, 0.0757, 0.0693, 0.0641, 0.0578, 0.0517, 0.0471, 0.0428, 0.0378, 0.0333, 0.0281, 0.0231, 0.0185, 0.0154, 0.0117, 0.0088, 0.0068, 0.0046, 0.0026, 0.0012, 0.0028, 0.0039, 0.0038, 0.0027, 0.0027, 0.0032, 0.0032, 0.0025, 0.0019, 0.0019, 0.0023, 0.0039, 0.0062, 0.0080, 0.0098, 0.0110, 0.0123, 0.0131, 0.0133, 0.0139, 0.0140, 0.0145, 0.0150, 0.0156, 0.0166, 0.0174, 0.0186, 0.0194, 0.0200, 0.0355, 0.1316, 0.3179, 0.5768, 0.8583, 1.1504, 1.4905, 1.9164, 2.4925, 3.2412, 4.1122, 5.0751, 6.0268, 6.9457, 7.7930, 8.5668, 9.2919, 9.9511, 10.5549, 11.0451, 11.3776, 11.5566, 11.6151, 11.4879, 10.9749, 10.0419, 8.8260, 7.5387, 6.4304, 5.6881, 5.4037, 5.3876, 5.4301, 5.4774, 5.5239, 5.5829, 5.6439, 5.7077, 5.8744, 6.2163, 6.7722, 7.4487, 8.1849, 8.8964, 9.5912, 10.2601, 10.8973, 11.4755, 11.9472, 12.2981, 12.4808, 12.5393, 12.5368, 12.5182, 12.4992, 12.4797, 12.4839, 12.4952, 12.5313, 12.6187, 12.8203, 13.1127, 13.4422, 13.7386, 13.9611, 14.1373, 14.3187, 14.5721, 14.9281, 15.3416, 15.8158, 16.2842, 16.6963, 17.0726, 17.4046, 17.7146, 18.0102, 18.3523, 18.7868, 19.2492, 19.7330, 20.1785, 20.6038, 20.9985, 21.4042, 21.8454, 22.3114, 22.8081, 23.3121, 23.8094, 24.3012, 24.7557, 25.1797, 25.5490, 25.8704, 26.1690, 26.4457, 26.7055, 26.9369, 27.1509, 27.3704, 27.5913, 27.8090, 27.9978, 28.1460, 28.2564, 28.3424, 28.4216, 28.5084, 28.5921, 28.6528, 28.6778, 28.6883, 28.7036, 28.7250, 28.7434, 28.7536, 28.7481, 28.7501, 28.7766, 28.8307, 28.8832, 28.9325, 28.9937, 29.0676, 29.1323, 29.1674, 29.1725, 29.1504, 29.1143, 29.0709, 29.0128, 28.9378, 28.8430, 28.7500, 28.6601, 28.5781, 28.4873, 28.3435, 28.0543, 27.5930, 26.9602, 26.2636, 25.5147, 24.7286, 23.9267, 23.1675, 22.5818, 22.1938, 21.9905, 21.8716, 21.7627, 21.6387, 21.5017, 21.3517, 21.1839, 20.9948, 20.7982, 20.6213, 20.4529, 20.2953, 20.1316, 19.9622, 19.7882, 19.6164, 19.4571, 19.3094, 19.1568, 19.0017, 18.8508, 18.7187, 18.6037, 18.4903, 18.3721, 18.2671, 18.1817, 18.1148, 18.0499, 17.9956, 17.9660, 17.9627, 17.9811, 18.0026, 18.0277, 18.0504, 18.0742, 18.0814, 18.0745, 18.0610, 18.0550, 18.0597, 18.0785, 18.1005, 18.1175, 18.1276, 18.1430, 18.1596, 18.1519, 18.1179, 18.0542, 17.9798, 17.8453, 17.5656, 17.0769, 16.3423, 15.4843, 14.5695, 13.6424, 12.7112, 11.7303, 10.7323, 9.7690, 8.9047, 8.2063, 7.6316, 7.1844, 6.8347, 6.5326, 6.2630, 6.0074, 5.7931, 5.6485, 5.5655, 5.5105, 5.4335, 5.3111, 5.1483, 4.9415, 4.6703, 4.3437, 3.9919, 3.6987, 3.4711, 3.2779, 3.0686, 2.8205, 2.5300, 2.2185, 1.9103, 1.6563, 1.4592, 1.3155, 1.2022, 1.1040, 1.0190, 0.9421, 0.8962, 0.9145, 1.0135, 1.1767, 1.3584, 1.5465, 1.7271, 1.9092, 2.0744, 2.2133, 2.3349, 2.4628, 2.6292, 2.8486, 3.1038, 3.3644, 3.5881, 3.7522, 3.8674, 3.9731, 4.1229, 4.3230, 4.5229, 4.6980, 4.8381, 4.9555, 5.0388, 5.1169, 5.2168, 5.3427, 5.3553, 5.0894, 4.5453, 3.8405, 3.0916, 2.3136, 1.4395, 0.6912, 0.2406, 0.2092, 0.2886, 0.3273, 0.3140, 0.3310, 0.3392, 0.3242, 0.3278, 0.3438, 0.3433, 0.3429, 0.3480, 0.3485, 0.3417, 0.3369, 0.3337, 0.3246, 0.3168, 0.3141, 0.3072, 0.2972, 0.2902, 0.2850, 0.2775, 0.2702, 0.2644, 0.2575, 0.2507, 0.2462, 0.2417, 0.2360, 0.2321, 0.2292, 0.2262, 0.2244, 0.2238, 0.2224, 0.2211, 0.2215, 0.2220, 0.2218, 0.2218, 0.2226, 0.2228, 0.2227, 0.2229, 0.2229, 0.2231, 0.2234, 0.2238, 0.2237, 0.2237, 0.2243, 0.2248, 0.2252, 0.2253, 0.2104, 0.1654, 0.1002, 0.0454, 0.0236, 0.0434, 0.1372, 0.2912, 0.4863, 0.6649, 0.8334, 0.9955, 1.1613, 1.3399, 1.5283]}

    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0117_sync"] = {}
    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0117_sync"]["sim_mode"] = "steps"
    settings["sequences"]["raw_data/2011_09_26/2011_09_26_drive_0117_sync"]["sim_steps"] = {"cam_motion": [28.1944, 28.6918, 29.1930, 29.7091, 30.2046, 30.6834, 31.1142, 31.5393, 31.9592, 32.4243, 32.8966, 33.3547, 33.6975, 33.9484, 34.1622, 34.4235, 34.7297, 35.0460, 35.3167, 35.5362, 35.7185, 35.9125, 36.1217, 36.3296, 36.5040, 36.6422, 36.7554, 36.8699, 36.9968, 37.1215, 37.2408, 37.3703, 37.5075, 37.6461, 37.7888, 37.9295, 38.0799, 38.2535, 38.4554, 38.6781, 38.9028, 39.1025, 39.2816, 39.4320, 39.5573, 39.6279, 39.6253, 39.5801, 39.5204, 39.4555, 39.3653, 39.2423, 39.0944, 38.9486, 38.8109, 38.6784, 38.5555, 38.4591, 38.4020, 38.3912, 38.4214, 38.4953, 38.6073, 38.7518, 38.9021, 39.0194, 39.1035, 39.1786, 39.2425, 39.2902, 39.2945, 39.2799, 39.2560, 39.2265, 39.1888, 39.1333, 39.0724, 39.0228, 39.0241, 39.0681, 39.1338, 39.1800, 39.1970, 39.2028, 39.2076, 39.2354, 39.2944, 39.3818, 39.4496, 39.4523, 39.3674, 39.2730, 39.2152, 39.2088, 39.1982, 39.1413, 39.0270, 38.8901, 38.7701, 38.6816, 38.5853, 38.4222, 38.1670, 37.8186, 37.4153, 36.9898, 36.5246, 36.0127, 35.3953, 34.7247, 34.0233, 33.3470, 32.7622, 32.3185, 32.0416, 31.8706, 31.7413, 31.6215, 31.4843, 31.3531, 31.2538, 31.1814, 31.0956, 30.9561, 30.7701, 30.5517, 30.3245, 30.0856, 29.8003, 29.4431, 29.0023, 28.5013, 27.9638, 27.4027, 26.7871, 26.1186, 25.4355, 24.8971, 24.4958, 24.2052, 23.9147, 23.6242, 23.3337, 23.0431, 22.7526, 22.4621, 22.1715, 21.8810, 21.5905, 21.3000, 21.0094, 20.7189, 20.4284, 20.2023, 20.0327, 19.9076, 19.7543, 19.5752, 19.3961, 19.2299, 19.0744, 18.9253, 18.7810, 18.6458, 18.5031, 18.3394, 18.1388, 17.9219, 17.7045, 17.4966, 17.2957, 17.1025, 16.9231, 16.7636, 16.6228, 16.4977, 16.3861, 16.2933, 16.2298, 16.1730, 16.1295, 16.1269, 16.1917, 16.3139, 16.4577, 16.6058, 16.7753, 16.9836, 17.2415, 17.5636, 17.9139, 18.3034, 18.7255, 19.1909, 19.6810, 20.1866, 20.7079, 21.2486, 21.7977, 22.3390, 22.8328, 23.2132, 23.4540, 23.5514, 23.5467, 23.4866, 23.3880, 23.2726, 23.1335, 22.9777, 22.7784, 22.5195, 22.1552, 21.6722, 21.0633, 20.3441, 19.5608, 18.7492, 17.9133, 17.0567, 16.1752, 15.2678, 14.3705, 13.6082, 13.1044, 12.8356, 12.6922, 12.5840, 12.4857, 12.3914, 12.3106, 12.2390, 12.1808, 12.1322, 12.0907, 12.0493, 12.0124, 11.9753, 11.9477, 11.9245, 11.9151, 11.9117, 11.9118, 11.9070, 11.8881, 11.8564, 11.8160, 11.7764, 11.7366, 11.6990, 11.6573, 11.5879, 11.4487, 11.1705, 10.7323, 10.1448, 9.4434, 8.6894, 7.8991, 7.1179, 6.4289, 5.9077, 5.5848, 5.3877, 5.2791, 5.2379, 5.2413, 5.2616, 5.2781, 5.2906, 5.2967, 5.2852, 5.2451, 5.1717, 5.0988, 5.0613, 5.0780, 5.1268, 5.1773, 5.2185, 5.2552, 5.2946, 5.3588, 5.4848, 5.7116, 6.0185, 6.3704, 6.7211, 7.0697, 7.3829, 7.6856, 7.9871, 8.3246, 8.6978, 9.0749, 9.4258, 9.7597, 10.1135, 10.5135, 10.8986, 11.2318, 11.4911, 11.6903, 11.8704, 12.0587, 12.2553, 12.4201, 12.5271, 12.5917, 12.6462, 12.7210, 12.8170, 12.9395, 13.0827, 13.2560, 13.4531, 13.6581, 13.8645, 14.0880, 14.3614, 14.6864, 15.0882, 15.5313, 16.0216, 16.5381, 17.0812, 17.6448, 18.2212, 18.8006, 19.3851, 19.9442, 20.5153, 21.0734, 21.6182, 22.1358, 22.6352, 23.1351, 23.6477, 24.1709, 24.7049, 25.2182, 25.7189, 26.1961, 26.6413, 26.9970, 27.2262, 27.3446, 27.4068, 27.4516, 27.4858, 27.5170, 27.5404, 27.5549, 27.5436, 27.4967, 27.4213, 27.3330, 27.2431, 27.1170, 26.9729, 26.8422, 26.7636, 26.7016, 26.6217, 26.5152, 26.3951, 26.2790, 26.1834, 26.1249, 26.1068, 26.1419, 26.2344, 26.3704, 26.5195, 26.6611, 26.8007, 26.9347, 27.0571, 27.1628, 27.2728, 27.3986, 27.5525, 27.7124, 27.8789, 28.0231, 28.1323, 28.2144, 28.3060, 28.4250, 28.5639, 28.7132, 28.8642, 29.0047, 29.1140, 29.2042, 29.2981, 29.4090, 29.5243, 29.6405, 29.7565, 29.8931, 30.0423, 30.1941, 30.3488, 30.5275, 30.7417, 30.9676, 31.1846, 31.3798, 31.5633, 31.7649, 31.9835, 32.1967, 32.3604, 32.4713, 32.5605, 32.6436, 32.7342, 32.8089, 32.8527, 32.8735, 32.8915, 32.9287, 32.9760, 33.0135, 33.0249, 33.0159, 33.0037, 32.9958, 32.9763, 32.9417, 32.8767, 32.7946, 32.6953, 32.6005, 32.4678, 32.2997, 32.0449, 31.7266, 31.3173, 30.8168, 30.2448, 29.5996, 28.9446, 28.2461, 27.5607, 26.8033, 26.0333, 25.1687, 24.4364, 23.8103, 23.4163, 23.1494, 23.0132, 22.9176, 22.8160, 22.7057, 22.6123, 22.5246, 22.4418, 22.3519, 22.2556, 22.1634, 22.1124, 22.0887, 22.0383, 21.8640, 21.6275, 21.4296, 21.3403, 21.2957, 21.2832, 21.3039, 21.3699, 21.3765, 21.2927, 21.1694, 21.0971, 21.1274, 21.2351, 21.4083, 21.6125, 21.8311, 22.0455, 22.2626, 22.4832, 22.6913, 22.8669, 22.9684, 22.9955, 22.9657, 22.8819, 22.7596, 22.5791, 22.3764, 22.1198, 21.8324, 21.4778, 21.0585, 20.5736, 20.0647, 19.5569, 19.0502, 18.5386, 18.0270, 17.5154, 17.0039, 16.4923, 15.9807, 15.4692, 14.9576, 14.4460, 13.9345, 13.4229, 12.9113, 12.3998, 11.8882, 11.4461, 11.1063, 10.9159, 10.8211, 10.7884, 10.7637, 10.7395, 10.7221, 10.7091, 10.7026, 10.7341, 10.8053, 10.8683, 10.8859, 10.9301, 11.0382, 11.2102, 11.3823, 11.6395, 11.9951, 12.4601, 12.9179, 13.3715, 13.7844, 14.1954, 14.5808, 14.9236, 15.2267, 15.5320, 15.8963, 16.3381, 16.8548, 17.4264, 18.0741, 18.7533, 19.4582, 20.1667, 20.8759, 21.6068, 22.3438, 23.1030, 23.8518, 24.5734, 25.2053, 25.7026, 26.0062, 26.1322, 26.1393, 26.0903, 26.0369, 25.9887, 25.9286, 25.8371, 25.6887, 25.5013, 25.2590, 24.9651, 24.5943, 24.1736, 23.7092, 23.2533, 22.8269, 22.4645, 22.1663, 21.9145, 21.6769, 21.4324, 21.1743, 20.9218, 20.6685, 20.4347, 20.2163, 20.0106, 19.8162, 19.6390, 19.5054, 19.5030, 19.6521, 19.9093, 20.2133, 20.5365, 20.8841, 21.2270, 21.5819, 21.9887, 22.4282, 22.8958, 23.4118, 23.9806, 24.6020, 25.2457, 25.9389, 26.5902, 27.2546, 27.8943, 28.6393, 29.3541, 30.0988, 30.7942, 31.5044, 32.1527, 32.7421, 33.1869, 33.4775, 33.6140, 33.6722, 33.6972, 33.7091, 33.7052, 33.6793, 33.6451, 33.6054, 33.5415, 33.4429, 33.3063, 33.1490, 32.9907, 32.8460, 32.7192, 32.5822, 32.4363, 32.2781, 32.1340, 32.0026, 31.8874, 31.7638, 31.6312, 31.4926, 31.3667, 31.2521, 31.1398, 31.0193, 30.8967, 30.7746, 30.6565, 30.5426, 30.4312, 30.3116, 30.1737, 30.0265, 29.8761, 29.7281]}

    return settings