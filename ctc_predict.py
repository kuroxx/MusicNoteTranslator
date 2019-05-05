import argparse
import tensorflow as tf
import ctc_utils
import cv2
import numpy as np

import pickle

#image_path = 'Data/Example/000051652-1_2_1.png'
model_path = 'Models/semantic_model.meta'
voc_path = 'Data/vocabulary_semantic.txt'
predicted_results = []
# predicted_results = {}
results_dic = {}

def main(image_path):
  tf.reset_default_graph()
  sess = tf.InteractiveSession()

  # Creates a dictionary to map index to words in the vocab
  dict_file = open(voc_path,'r') # open .txt file
  dict_list = dict_file.read().splitlines() # read .txt file and returns list with all the lines in string
  int2word = dict() # create dictionary 
  for word in dict_list:
      word_idx = len(int2word) # gets word index
      int2word[word_idx] = word # assigns index to word in the dictionary
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
  # print(str_predictions)
  # print(len(str_predictions[0]))

  for w in str_predictions[0]:
      predicted_results.append(int2word[w]) 

      # creates dict using key id from predictions and maps it to the word values
      results_dic = dict(zip(str_predictions[0], predicted_results))
      
      # print (int2word[w]),
      # print ('\t')

  # Saves dict in a pickle file
  pickle.dump( results_dic, open( "save.p", "wb" ) )

  # print(predicted_results)
  # print(results_dic)