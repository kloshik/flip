#!/bin/env python3
#
# Requirements:
# numpy
# scikit-image
# scipy

import sys

import numpy
import skimage
from scipy.signal import savgol_filter, find_peaks

def flip_channel(channel):
    print(channel.shape)

    channel_hist, channel_bins = numpy.histogram(channel, bins=256)

    peaks, _ = find_peaks(channel_hist)

    channel_hist = savgol_filter(channel_hist, 96, 3)
    
    peaks, _ = find_peaks(channel_hist)
    pits, _ = find_peaks(-channel_hist)

    keypoints_pos = list()
    keypoints_val = list()


    keypoints_pos.append(0)
    keypoints_val.append(255.0)
    if peaks[0] < pits[0]:
        for peak, pit in zip(peaks, pits):
            keypoints_pos.append(peak)
            keypoints_val.append(0.0)

            keypoints_pos.append(pit)
            keypoints_val.append(255.0)
    else:
        for peak, pit in zip(peaks, pits):
            keypoints_pos.append(pit)
            keypoints_val.append(255.0)

            keypoints_pos.append(peak)
            keypoints_val.append(0.0)


    keypoints_pos.append(255)
    keypoints_val.append(255.0)

    val_map = list()

    for val in range(256):

        begin_pos = None
        begin_val = None

        end_pos = None
        end_val = None

        for map_pos, map_val in zip(keypoints_pos, keypoints_val):
            if map_pos >= val:
                end_pos = map_pos
                end_val = map_val
                break

            begin_pos = map_pos
            begin_val = map_val

        if begin_pos is None:
            begin_pos = 0

            if keypoints_val[0] > 255 / 2:
                begin_val = 0   
            else:
                begin_val = 255 

        if end_pos is None:
            end_pos = 255

            if keypoints_val[-1] > 255 / 2:
                end_val = 0
            else:
                end_val = 255

        if end_pos - begin_pos != 0:
            x_rel = (val - begin_pos) / (end_pos - begin_pos)
        else:
            x_rel = 1.0
        val_map.append(begin_val * (1.0 - x_rel) + end_val * x_rel)


    for idx, val in enumerate(channel.flatten()):
        x = idx % channel.shape[1]
        y = idx // channel.shape[1]


        channel[y, x] = val_map[val]

    return channel

    


def flip(img):
    img[:,:,0] = flip_channel(img[:,:,0])
    img[:,:,1] = flip_channel(img[:,:,1])
    img[:,:,2] = flip_channel(img[:,:,2])
    
    return img

def usage():
    print('Usage:\n\t{:} "input_image_path" "output_image_path"'.format(sys.argv[0]))

def main():
    if len(sys.argv) != 3:
        print('E: Wrong argument count.')
        usage()
        exit()
    
    input_img = skimage.io.imread(sys.argv[1])

    output_img = flip(input_img)

    skimage.io.imsave(sys.argv[2], output_img)


if __name__ == '__main__':
    main()
