import numpy as np
import copy as c




# <--- Transzformációs mátrixok --->

# Forgatás
rot = np.zeros((9,9), dtype='int32')
rot[0][6] = 1
rot[1][3] = 1
rot[2][0] = 1
rot[3][7] = 1
rot[4][4] = 1
rot[5][1] = 1
rot[6][8] = 1
rot[7][5] = 1
rot[8][2] = 1

# Tükrözés
refl = np.zeros((9, 9), dtype='int32')
refl[0][2] = 1
refl[1][1] = 1
refl[2][0] = 1
refl[3][5] = 1
refl[4][4] = 1
refl[5][3] = 1
refl[6][8] = 1
refl[7][7] = 1
refl[8][6] = 1


# Teljes transzformációs mátrix (8 x 9 x 9)
transformations = np.zeros((8, 9, 9), dtype='int32')

### Identitás
transformations[0][0][0] = 1
transformations[0][1][1] = 1
transformations[0][2][2] = 1
transformations[0][3][3] = 1
transformations[0][4][4] = 1
transformations[0][5][5] = 1
transformations[0][6][6] = 1
transformations[0][7][7] = 1
transformations[0][8][8] = 1

### Forgatások
transformations[1] = np.dot(rot, transformations[0])
transformations[2] = np.dot(rot, transformations[1])
transformations[3] = np.dot(rot, transformations[2])

### Tükrözés -> Forgatások
transformations[4] = np.dot(refl, transformations[0])
transformations[5] = np.dot(rot, transformations[4])
transformations[6] = np.dot(rot, transformations[5])
transformations[7] = np.dot(rot, transformations[6])