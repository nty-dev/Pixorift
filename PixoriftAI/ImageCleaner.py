import os
from PIL import Image
import tensorflow as tf
import base64

o = os.walk('./ImageDB')
p = []
for x in o:
    p.extend(x[1])
for i in p:
    dit = './ImageDB/' + i
    prob = './ImageProblem/' + i
    a = 1
    for fn in os.listdir(dit):
        try:
            with open(dit + '/' + fn, 'rb') as l:
                r = str(base64.b64encode(l.read()).decode()[:4])
            if r not in ['/9j/', 'iVBO', 'R0lG']:
                print(fn + ' rejected.')
                if not os.path.isdir(prob):
                    os.mkdir(prob)
                os.rename(dit + '/' + fn, prob + '/' + fn)
                #tf.image.decode_image(l.read())
            elif fn[-4:].lower() not in ['.jpg', '.png', '.gif', 'jpeg']:
                print(fn + ' rejected.')
                if not os.path.isdir(prob + '/' + fn):
                    os.mkdir(prob + '/' + fn)
                os.rename(dit + '/' + fn, prob + '/' + fn)
            else:
                if fn[-4:].lower() in ['.jpg', '.png', '.gif']:
                    os.rename(dit + '/' + fn, dit + '/' + str(a) + fn[-4:])
                else:
                    os.rename(dit + '/' + fn, dit + '/' + str(a) + fn[-5:])
                a = a + 1
        except ValueError:
            print(fn + ' rejected.')
            if not os.path.isdir(prob + '/' + fn):
                os.mkdir(prob + '/' + fn)
            os.rename(dit + '/' + fn, prob + '/' + fn)

        
