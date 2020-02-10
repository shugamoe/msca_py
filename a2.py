# Julian McClellan
# Advanced Python for Streaming Analytics (Fall 2017)
# Assignment II 

import pdb
import math
from PIL import Image, ImageDraw
import numpy as np
import cv2

i = Image.open("images/mario.png")
iar = np.asarray(i)

# Lets you write iar
iar.flags.writeable = True

class Tree:
    GREEN_BLOCK = [77, 158, 58, 255]
    WHITE_BLOCK = [255, 255, 255, 0]
    BROWN_BLOCK = [102, 51, 0, 255]
    TRUNK_FRAC = (.3, .3)

    def __init__(self):
        """
        """
        pass


    @staticmethod
    def draw(cols, block):
        rv = []
        for i in range(cols):
            rv.append(block)
        return rv

    def add_root(self, leaves_array):
        where_green = np.where(np.all(leaves_array == self.GREEN_BLOCK, axis=2))
        s_green, e_green = np.min(where_green[1]), np.max(where_green[1])

        root_size = math.floor((e_green - s_green) * self.TRUNK_FRAC[1])
        remainder = (math.floor((leaves_array.shape[1] - root_size) / 2), 
                math.ceil((leaves_array.shape[1] - root_size) / 2))

        for r in range(math.ceil(leaves_array.shape[1] * self.TRUNK_FRAC[0])):
            row = []
            row += self.draw(remainder[0], self.WHITE_BLOCK)
            row += self.draw(root_size, self.BROWN_BLOCK)
            row += self.draw(remainder[1], self.WHITE_BLOCK)
            row = np.array(row, dtype=np.uint8, ndmin=3)
            leaves_array = np.vstack([leaves_array, row])

        return(leaves_array)

    def add_trunk(self, landr_array):
        """
        Takes a numpy array with the leaves and root added and
        adds the trunk (an upward extension of the root with reduced opacity).
        """
        where_leaves = np.where(np.all(landr_array == self.GREEN_BLOCK, axis=2))
        where_root = np.where(np.all(landr_array == self.BROWN_BLOCK, axis=2))

        root_top_left = (np.min(where_root[0]), np.min(where_root[1]))
        root_top_right = (np.min(where_root[0]), np.max(where_root[1]))

        trunk_top_left = (np.min(np.where(np.all(
            landr_array[:, root_top_left[1],:] == self.GREEN_BLOCK, axis=1))) + 1,
            root_top_left[1])
        trunk_top_right = (np.min(np.where(np.all(
            landr_array[:, root_top_right[1],:] == self.GREEN_BLOCK, axis=1))) + 1,
            root_top_right[1])

        r_grad = list(np.linspace(77, 102, root_top_left[0] - trunk_top_left[0], dtype=np.uint8))
        g_grad = list(np.linspace(158, 51, root_top_left[0] - trunk_top_left[0], dtype=np.uint8))
        b_grad = list(np.linspace(58, 0, root_top_left[0] - trunk_top_left[0], dtype=np.uint8))
        trunk_array = np.array([[[r, g, b, 255] for col in range(trunk_top_right[1] - trunk_top_left[1])] for r, g, b in zip(r_grad,
            g_grad, b_grad)])

        # Insert Trunk array
        landr_array[trunk_top_left[0]:root_top_left[0], trunk_top_left[1]:trunk_top_right[1],:] = trunk_array

        return landr_array


class ChristmasTree(Tree):
    def __init__(self, rows, cols):
        """
        """
        self.leaves = (rows, cols)
        self.root = (math.floor(.1 * rows), math.floor(.3 * cols))

    def DisplayTree(self):
        """
        Displays a christmas tree on the screen
        """
        rows, cols = self.leaves

        def draw_leaves():
            init = False
            for r in range(rows):
                row = []
                div_num = math.floor(((((cols - 1) * (r - 1) / (rows - 1) + 1) / 2) * 2 + 1))
                row += self.draw((cols - div_num) // 2, self.WHITE_BLOCK)
                row += self.draw((div_num), self.GREEN_BLOCK)
                row += self.draw((cols - div_num) // 2, self.WHITE_BLOCK)
                
                # Balance col numbers
                col_dif = len(row) - cols
                if cols != len(row):
                    row += [row[-1]] * abs(col_dif)
                row = np.array(row, dtype=np.uint8, ndmin=3)
                if not init:
                    final_array = row
                    init = True
                else:
                    final_array = np.vstack([final_array, row])
            return(np.array(final_array))

        return self.add_trunk(self.add_root(draw_leaves()))

class SquareTree(Tree):
    def __init__(self, length):
        """
        """
        self.leaves = length, length

    def DisplayTree(self):
        """
        Displays a christmas tree on the screen
        """
        rows = self.leaves[0]
        def draw_leaves():
            init = False
            for r in range(rows):
                row = []
                row += self.draw(rows, self.GREEN_BLOCK)
                row = np.array(row, dtype=np.uint8, ndmin=3)

                if not init:
                    final_array = row
                    init = True
                else:
                    final_array = np.vstack([final_array, row])
            return(np.array(final_array))
        return self.add_trunk(self.add_root(draw_leaves()))

class OvalTree(Tree):
    TRUNK_FRAC = (.09, .5) 

    def __init__(self, rows, cols):
        self.leaves = rows, cols

    def DisplayTree(self):
        def draw_leaves():
            init = False
            rows, cols = self.leaves
            for r in range(rows):
                row = []
                row += self.draw(cols, self.WHITE_BLOCK)
                row = np.array(row, dtype=np.uint8, ndmin=3)

                if not init:
                    leaves_array = row
                    init = True
                else:
                    leaves_array = np.vstack([leaves_array, row])

            # Modify blank image with drawing of green ellipse
            # From https://stackoverflow.com/questions/4789894/python-pil-how-to-draw-an-ellipse-in-the-middle-of-an-image
            leaves_image = Image.fromarray(leaves_array, mode='RGBA')
            x, y =  leaves_image.size
            eX, eY = x / 3.5, y  #Size of Bounding Box for ellipse

            bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
            draw = ImageDraw.Draw(leaves_image)
            draw.ellipse(bbox,
                    fill=tuple(self.GREEN_BLOCK[:-1]))

            leaves_array = np.asarray(leaves_image)
            return(leaves_array)

        return self.add_trunk(self.add_root(draw_leaves()))

def mar_look_at_trees(image, start_point = (183, 1023), tree_size = 100):
    """
    Makes the mario image look at the three different trees
    """
    tree_arrays = [ChristmasTree(tree_size, tree_size).DisplayTree(),
            OvalTree(tree_size, tree_size).DisplayTree(), 
            SquareTree(tree_size).DisplayTree()]
    sx, sy = start_point

    for tree in tree_arrays:
        image[sx:sx + tree.shape[0], sy:sy + tree.shape[1], :] = tree
        sy += tree.shape[1]

    Image.fromarray(image, mode='RGBA').show()
    return

def threshold(image):
    """
    """
    import re
    image_array = np.asarray(image)
    image_array.flags.writeable = True

    full_mean = np.mean(image_array, axis=(0, 1, 2))

    image_array[np.mean(image_array, axis=2) >= full_mean] = np.array([255, 255, 255, 255], 
            dtype=np.uint8)
    image_array[np.mean(image_array, axis=2) <= full_mean] = np.array([0, 0, 0, 0], 
            dtype=np.uint8)

    new_image = Image.fromarray(image_array, mode='RGBA')
    new_name = re.sub(r'\.png', "_thresh.png", image.filename)
    new_image.save(new_name)
    return





if __name__ == "__main__":
    # c_array = ChristmasTree(1400, 1500).DisplayTree()
    # s_array = SquareTree(1500).DisplayTree()
    # o_array = OvalTree(1400, 1500).DisplayTree()

    # cimage = Image.fromarray(c_array, mode='RGBA').save('ctest.png')
    # simage = Image.fromarray(s_array, mode='RGBA').save('stest.png')
    # oimage = Image.fromarray(o_array, mode='RGBA').save('otest.png')

    tar = np.array([[[1,2,3,4],[1,2,3,4]], [[1,2,3,4], [1,2,3,4]], [[1,2,3,4], [1,2,3,4]]])

    mar_look_at_trees(iar.copy())
    threshold(i)

