'''
This code was originally developed by Jorge Calvo Zaragoza:
https://github.com/calvozaragoza/tf-deep-omr
It was used for experiments detailed in this paper: 
https://www.mdpi.com/2076-3417/8/4/606

Modifications to the code have been applied to be used for the project: MusicNoteTranslator
'''

import argparse
import tensorflow as tf
import ctc_utils
import cv2
import numpy as np
import pickle

model_path = 'Models/semantic_model.meta'
voc_path = 'Data/vocabulary_semantic.txt'
predicted_results = []
results_dic = {}

def main(image_path):
  """
  Runs TF model to get predictions and saves it to a dictionary.

  :param str image_path: The path to the image
  """

  tf.reset_default_graph()
  sess = tf.InteractiveSession()

  # Map index to words in the vocab
  dict_file = open(voc_path,'r') 
  dict_list = dict_file.read().splitlines() 
  int2word = dict() 
  for word in dict_list:
      word_idx = len(int2word) 
      int2word[word_idx] = word 
  dict_file.close()

  # Restore weights
  saver = tf.train.import_meta_graph(model_path)
  saver.restore(sess,model_path[:-5])

  graph = tf.get_default_graph()

  input = graph.get_tensor_by_name("model_input:0")
  seq_len = graph.get_tensor_by_name("seq_lengths:0")
  rnn_keep_prob = graph.get_tensor_by_name("keep_prob:0")
  height_tensor = graph.get_tensor_by_name("input_height:0")
  width_reduction_tensor = graph.get_tensor_by_name("width_reduction:0")
  logits = tf.get_collection("logits")[0]

  # Constants that are saved inside the model itself
  WIDTH_REDUCTION, HEIGHT = sess.run([width_reduction_tensor, height_tensor])

  decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_len)

  image = cv2.imread(image_path,False)
  image = ctc_utils.resize(image, HEIGHT)
  image = ctc_utils.normalize(image)
  image = np.asarray(image).reshape(1,image.shape[0],image.shape[1],1)

  seq_lengths = [ image.shape[2] / WIDTH_REDUCTION ]

  prediction = sess.run(decoded,
                        feed_dict={
                            input: image,
                            seq_len: seq_lengths,
                            rnn_keep_prob: 1.0,
                        })

  str_predictions = ctc_utils.sparse_tensor_to_strs(prediction)

  for w in str_predictions[0]:
      predicted_results.append(int2word[w]) 

      # Map prediction key ids to words
      results_dic = dict(zip(str_predictions[0], predicted_results))
      
  pickle.dump( results_dic, open( "save.p", "wb" ) )
  print(results_dic)