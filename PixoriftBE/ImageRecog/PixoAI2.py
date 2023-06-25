import os
import tensorflow as tf
import numpy as np
import cv2

AIgraph = os.getcwd() + '/ImageRecog/TrainedAI/graph.pb'
imgvar = os.getcwd() + '/ImageRecog/TrainedAI/var.txt'

class PixoAI():
    def __init__(self):
        pass

    def __repr__(self):
        return repr(self.lastreturn)

    def process(self, img, AI=AIgraph, imgvar=imgvar):
        print('Initializing PixoAI...')
        self.AI = AI
        self.imgvar = imgvar
        if not self.checksum(self.AI, self.imgvar):
            return
        print('Validated existence of required files.')
        imgclass = []
        for x in tf.gfile.GFile(self.imgvar):
            j = x.rstrip()
            imgclass.append(j)
        self.imgclass = imgclass
        print('Image Class loaded.')
        with tf.gfile.GFile(self.AI, 'rb') as p:
            graphDef = tf.GraphDef()
            graphDef.ParseFromString(p.read())
            _ = tf.import_graph_def(graphDef, name='')
        print('Core AI Mainframe loaded.')
        self.lastreturn = []
        print('PixoAI initiated.')
        with tf.Session() as s:
            finalTensor = s.graph.get_tensor_by_name('final_result:0')
            openCVImage = cv2.imread(img)
            if openCVImage is None:
                print('PixoAI Error: A fatal error has occured. Image file cannot be opened.')
                return
            finalTensor = s.graph.get_tensor_by_name('final_result:0')
            tfImage = np.array(openCVImage)[:, :, 0:3]
            predictions = s.run(finalTensor, {'DecodeJpeg:0': tfImage})
            sortedPredictions = predictions[0].argsort()[-len(predictions[0]):][::-1]
            onMostLikelyPrediction = True
            for prediction in sortedPredictions:
                strClassification = self.imgclass[prediction]
                if strClassification.endswith("s"):
                    strClassification = strClassification[:-1]
                confidence = predictions[0][prediction]
                if onMostLikelyPrediction:
                    AIprocessed = [strClassification, confidence * 100]
                    onMostLikelyPrediction = False
        self.lastreturn = AIprocessed
        return AIprocessed

    def checksum(self, a, b):
        if not os.path.exists(a):
            print('PixoAI Error: A fatal error has occured. Machine Learning data does not exist.')
            return False
        if not os.path.exists(b):
            print('PixoAI Error: AI variable file does not exist.')
            return False
        return True

if __name__ == '__main__':
    PixoAI = PixoAI()
    PixoAI.process('./ImageTest/67.china.jpg')
    print(PixoAI)
