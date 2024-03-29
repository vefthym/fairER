
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')

import os
import random
import keras
from tqdm import *
import numpy as np
from utils import *
from CSLS import *
import tensorflow as tf
import keras.backend as K
from keras.layers import *
from layer import NR_GraphAttention
import time
from datetime import datetime
import sys
import os 

os.environ["KMP_WARNINGS"] = "FALSE"

total_time = time.time()

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"]="2"
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

config = tf.ConfigProto()
config.gpu_options.allow_growth=True  
sess = tf.Session(config=config)  


# In[2]:

args = sys.argv[1:]

export_results = True
mycsls = -1
dataset_path = args[0]
dest_path = args[1]
file_name = args[2]

if mycsls == -1:
    csls_mode = "NO_CSLS"
elif mycsls > 0:
    csls_mode = "WITH_CSLS"

print(csls_mode)
print(dataset_path)
print(dest_path)

if export_results == True:
    isExist = os.path.exists(dest_path)
    if not isExist:
        os.makedirs(dest_path)
    sys.stdout=open(dest_path + "log_" + str(datetime.now()),"w")

# Specify dataset, training ratio and fold
entity1, entity2, train_pair,dev_pair,valid_pair,adj_matrix,r_index,r_val,adj_features,rel_features = load_data(dataset_path,0.20,2)
print(len(entity1))
adj_matrix = np.stack(adj_matrix.nonzero(),axis = 1)
rel_matrix,rel_val = np.stack(rel_features.nonzero(),axis = 1),rel_features.data
ent_matrix,ent_val = np.stack(adj_features.nonzero(),axis = 1),adj_features.data

# In[3]:


node_size = adj_features.shape[0]
rel_size = rel_features.shape[1]
triple_size = len(adj_matrix)
batch_size = node_size
class TokenEmbedding(keras.layers.Embedding):
    """Embedding layer with weights returned."""

    def compute_output_shape(self, input_shape):
        return self.input_dim, self.output_dim

    def compute_mask(self, inputs, mask=None):
        return None

    def call(self, inputs):
        return self.embeddings
    
def get_embedding():
    inputs = [adj_matrix,r_index,r_val,rel_matrix,ent_matrix]
    inputs = [np.expand_dims(item,axis=0) for item in inputs]
    return get_emb.predict_on_batch(inputs)

def test(wrank = None):
    vec = get_embedding()
    return  get_hits(vec,dev_pair,wrank=wrank)

def check_early_stop(thread_number = 16, csls=10,accurate = True, iteration = 0):
    vec = get_embedding()
    Lvec = np.array([vec[e1] for e1, e2 in valid_pair])
    Rvec = np.array([vec[e2] for e1, e2 in valid_pair])
    Lvec = Lvec / np.linalg.norm(Lvec,axis=-1,keepdims=True)
    Rvec = Rvec / np.linalg.norm(Rvec,axis=-1,keepdims=True)
    _, hits1, _, _ = eval_alignment_by_sim_mat(Lvec, Rvec, [1, 5, 10], thread_number, "", entity1, entity2, csls=csls, accurate=accurate, output=False, testing=False, iteration = iteration)
    return hits1

def testing(thread_number = 16, csls=10,accurate = True, iteration = 0):
    vec = get_embedding()
    Lvec = np.array([vec[e1] for e1, e2 in dev_pair])
    Rvec = np.array([vec[e2] for e1, e2 in dev_pair])
    Lvec = Lvec / np.linalg.norm(Lvec,axis=-1,keepdims=True)
    Rvec = Rvec / np.linalg.norm(Rvec,axis=-1,keepdims=True)
    test_ent_list = [ent[0] for ent in dev_pair]
    _, hits1, performance, neighbors_sim_dict = eval_alignment_by_sim_mat(Lvec, Rvec, [1, 5, 10], thread_number, "", entity1, entity2, csls=csls, accurate=accurate, testing=True, iteration = iteration, test_ent_list=test_ent_list)
    return performance, neighbors_sim_dict


def get_train_set(batch_size = batch_size):
    negative_ratio =  batch_size // len(train_pair) + 1
    train_set = np.reshape(np.repeat(np.expand_dims(train_pair,axis=0),axis=0,repeats=negative_ratio),newshape=(-1,2))
    np.random.shuffle(train_set); train_set = train_set[:batch_size]
    train_set = np.concatenate([train_set,np.random.randint(0,node_size,train_set.shape)],axis = -1)
    return train_set

def get_trgat(node_size,rel_size,node_hidden,rel_hidden,triple_size,n_attn_heads = 2,dropout_rate = 0,gamma = 3,lr = 0.005,depth = 2):
    adj_input = Input(shape=(None,2))
    index_input = Input(shape=(None,2),dtype='int64')
    val_input = Input(shape = (None,))
    rel_adj = Input(shape=(None,2))
    ent_adj = Input(shape=(None,2))
    
    ent_emb = TokenEmbedding(node_size,node_hidden,trainable = True)(val_input) 
    rel_emb = TokenEmbedding(rel_size,node_hidden,trainable = True)(val_input)
    
    def avg(tensor,size):
        adj = K.cast(K.squeeze(tensor[0],axis = 0),dtype = "int64")   
        adj = tf.SparseTensor(indices=adj, values=tf.ones_like(adj[:,0],dtype = 'float32'), dense_shape=(node_size,size)) 
        adj = tf.sparse_softmax(adj) 
        return tf.sparse_tensor_dense_matmul(adj,tensor[1])
    
    opt = [rel_emb,adj_input,index_input,val_input]
    ent_feature = Lambda(avg,arguments={'size':node_size})([ent_adj,ent_emb])
    rel_feature = Lambda(avg,arguments={'size':rel_size})([rel_adj,rel_emb])
    
    encoder = NR_GraphAttention(node_size,activation="relu",
                                       rel_size = rel_size,
                                       depth = depth,
                                       attn_heads=n_attn_heads,
                                       triple_size = triple_size,
                                       attn_heads_reduction='average',   
                                       dropout_rate=dropout_rate)
    
    out_feature = Concatenate(-1)([encoder([ent_feature]+opt),encoder([rel_feature]+opt)])
    out_feature = Dropout(dropout_rate)(out_feature)
    
    alignment_input = Input(shape=(None,4))
    find = Lambda(lambda x:K.gather(reference=x[0],indices=K.cast(K.squeeze(x[1],axis=0), 'int32')))([out_feature,alignment_input])
    
    def align_loss(tensor):
        def _cosine(x):
            dot1 = K.batch_dot(x[0], x[1], axes=1)
            dot2 = K.batch_dot(x[0], x[0], axes=1)
            dot3 = K.batch_dot(x[1], x[1], axes=1)
            max_ = K.maximum(K.sqrt(dot2 * dot3), K.epsilon())
            return dot1 / max_
        
        def l1(ll,rr):
            return K.sum(K.abs(ll-rr),axis=-1,keepdims=True)
        
        def l2(ll,rr):
            return K.sum(K.square(ll-rr),axis=-1,keepdims=True)
        
        l,r,fl,fr = [tensor[:,0,:],tensor[:,1,:],tensor[:,2 ,:],tensor[:,3,:]]
        loss = K.relu(gamma + l1(l,r) - l1(l,fr)) + K.relu(gamma + l1(l,r) - l1(fl,r))
        return tf.reduce_sum(loss,keep_dims=True) / (batch_size)
    
    loss = Lambda(align_loss)(find)
    
    inputs = [adj_input,index_input,val_input,rel_adj,ent_adj]
    train_model = keras.Model(inputs = inputs + [alignment_input],outputs = loss)
    train_model.compile(loss=lambda y_true,y_pred: y_pred,optimizer=keras.optimizers.rmsprop(lr))
    
    feature_model = keras.Model(inputs = inputs,outputs = out_feature)
    return train_model,feature_model

# In[4]:


model,get_emb = get_trgat(dropout_rate=0.30,node_size=node_size,rel_size=rel_size,n_attn_heads = 1,depth=2,gamma =3,node_hidden=100,rel_hidden = 100,triple_size = triple_size)
model.summary(); initial_weights = model.get_weights()


# In[ ]:

# propose new pairs on test and validation sets
un_aligned = np.concatenate([dev_pair,valid_pair],axis = 0)
rest_set_1 = [e1 for e1, e2 in un_aligned]
rest_set_2 = [e2 for e1, e2 in un_aligned]
# propose new pairs on test set
# rest_set_1 = [e1 for e1, e2 in dev_pair]
# rest_set_2 = [e2 for e1, e2 in dev_pair]
np.random.shuffle(rest_set_1)
np.random.shuffle(rest_set_2)

# test set for bias@k
test_set_1 = [e1 for e1, e2 in dev_pair]
test_set_2 = [e2 for e1, e2 in dev_pair]

np.random.shuffle(test_set_1)
np.random.shuffle(test_set_2)

epoch = 1200
# epoch = 40

# replace 5 with 1 for RREA(basic)
for turn in range(5):
    iter_time = time.time()
    print("iteration %d start."%turn)
    hits1_temp = []
    for i in trange(epoch):
        epoch_time = time.time()
        train_set = get_train_set()
        inputs = [adj_matrix,r_index,r_val,rel_matrix,ent_matrix,train_set]
        inputs = [np.expand_dims(item,axis=0) for item in inputs]
        model.train_on_batch(inputs,np.zeros((1,1)))

        if i >= 30 and i%30==0:
        # if i%10==0:
            hits1_temp.append(check_early_stop(csls=mycsls))
            if len(hits1_temp) >= 2:
                if hits1_temp[-1] < hits1_temp[-2]:
                    print("Should early stop !!!")
                    break
    print("[N]. Iteration " + str(turn) + " training time = {:.3f} s.".format(time.time() - iter_time))
    print("epoch = " + str(i))
    test_time = time.time()
    performance, neighbors_sim_dict = testing(iteration = turn, csls=mycsls)
    print("[N]. Iteration " + str(turn) + " testing time = {:.3f} s.".format(time.time() - test_time))
    new_pair = []
    new_right_ent = []
    vec = get_embedding()
    
    if turn == 4:
        if export_results == True:
            file_to_write = open(dest_path + file_name, "wb")
            pickle.dump(neighbors_sim_dict, file_to_write)
    
    Lvec = np.array([vec[e] for e in rest_set_1])
    Rvec = np.array([vec[e] for e in rest_set_2])
    Lvec = Lvec / np.linalg.norm(Lvec,axis=-1,keepdims=True)
    Rvec = Rvec / np.linalg.norm(Rvec,axis=-1,keepdims=True)
    A,_,_,_ = eval_alignment_by_sim_mat(Lvec, Rvec, [1, 5, 10], 16, "", entity1, entity2, mycsls,True,False)
    B,_,_,_ = eval_alignment_by_sim_mat(Rvec, Lvec,[1, 5, 10], 16, "", entity1, entity2, mycsls,True,False)
    A = sorted(list(A)); B = sorted(list(B))
    for a,b in A:
        if  B[b][1] == a:
            new_pair.append([rest_set_1[a],rest_set_2[b]])
            new_right_ent.append(rest_set_2[b])
    print("generate new semi-pairs: %d." % len(new_pair))
    
    train_pair = np.concatenate([train_pair,np.array(new_pair)],axis = 0)
    for e1,e2 in new_pair:
        if e1 in rest_set_1:
            rest_set_1.remove(e1) 
        
    for e1,e2 in new_pair:
        if e2 in rest_set_2:
            rest_set_2.remove(e2)
    
print("[N]. Total time = {:.3f} s.".format(time.time() - total_time))