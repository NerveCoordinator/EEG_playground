import numpy
import pickle
import random
import sys
import tempfile
import unittest

from htm.bindings.algorithms import Classifier, Predictor
from htm.bindings.sdr import SDR
from htm.algorithms import TemporalMemory as TM
from htm.algorithms import SpatialPooler as SP


def testExampleUsage():
    # Make a random SDR and associate it with a category.
    inputData  = SDR( 1000 ).randomize( 0.02 )
    categories = { 'A': 0, 'B': 1, 'C': 2, 'D': 3 }
    clsr = Classifier()
    clsr.learn( inputData, categories['B'] )
    print(numpy.argmax( clsr.infer( inputData ) ) ) #  ==  categories['B'] 
    
    # Estimate a scalar value.  The Classifier only accepts categories, so
    # put real valued inputs into bins (AKA buckets) by subtracting the
    # minimum value and dividing by a resolution.
    scalar     = 567.8
    minimum    = 500
    resolution = 10
    clsr.learn( inputData, int((scalar - minimum) / resolution) )
    print( numpy.argmax( clsr.infer( inputData ) ) * resolution + minimum) #==  560 
    
    
    # Predict 1 and 2 time steps into the future.
    
    # Make a sequence of 4 random SDRs, each SDR has 1000 bits and 2% sparsity.
    sequence = [ SDR( 1000 ).randomize( 0.02 ) for i in range(4) ]
    
    # Make category labels for the sequence.
    labels = [ 4, 5, 6, 7 ]
    
    # Make a Predictor and train it.
    pred = Predictor([ 1, 2 ])
    pred.learn( 0, sequence[0], labels[0] )
    pred.learn( 1, sequence[1], labels[1] )
    pred.learn( 2, sequence[2], labels[2] )
    pred.learn( 3, sequence[3], labels[3] )
    
    # Give the predictor partial information, and make predictions
    # about the future.
    pred.reset()
    A = pred.infer( 0, sequence[0] )
    print( numpy.argmax( A[1] ))#  ==  labels[1] )
    print( numpy.argmax( A[2] ))#  ==  labels[2] )
    
    B = pred.infer( 1, sequence[1] )
    print( numpy.argmax( B[1] ))#  ==  labels[2] )
    print( numpy.argmax( B[2] ))#  ==  labels[3] )


#testExampleUsage()



from htm.encoders.scalar_encoder import ScalarEncoder, ScalarEncoderParameters

def ScalarEncoderGenerator(mini, maxi, size, spars=-1):
  if spars == -1:
    diff = maxi-mini
    spars = 1/(diff+1)
  params            = ScalarEncoderParameters()
  params.minimum    = mini
  params.maximum    = maxi
  params.size       = size
  params.sparsity   = spars
  encoder = ScalarEncoder( params )
  return encoder




# Utility routine for printing an SDR in a particular way.
def formatBits(sdr):
  s = ''
  for c in range(sdr.size):
    if c > 0 and c % 10 == 0:
      s += ' '
    s += str(sdr.dense.flatten()[c])
  s += ' '
  return s




'''

you can easily test sparsity with only a few inputs

if sparsity is too high
    it'll predict too many numbers and be way off

if sparsity is too low
    it won't give any answer at all



if numSize is too low
    it'll give consistently wrong outputs for specific numbers
    often numbers near the start like 0 or 1
    
'''
'''
numSize = 250
numMin  = 0
numMax  = 100
numSpars = 0.02 # 5/250
tries = 10000
'''

'''
numSize = 500
numMin  = 0
numMax  = 250
numSpars = 0.008
tries = 100000
'''
'''
numSize = 2000
numMin  = 0
numMax  = 1000
numSpars = 0.002
tries = 100000
'''

# Sparsity needs to figure out how to give 4-5 values per number? 
    #so something like (1/numMax) * (numSize/numMax)?
#numEncoder = ScalarEncoderGenerator(numMin,numMax,numSize,numSpars)


import random

results = []

import math
def decToStr(num, size):
    order = int(math.log10(num))
    #print(order)
    if order > size:
        print("can't convert to str, order larger than size:", num, order, size)
        exit() 
    output = "0" * (int(size)-int(order)) + str(num)
    return output


def encodeStrDecimal(encoder, num):
    output = []
    for digit in num:
        encoding = encoder.encode(int(digit))
        output.append(encoding)
    return output

#function taken from the internet, not mine
def flatten(l, a=None):
    #check a
    if a is None:
        #initialize with empty list
        a = []

    for i in l:
        if isinstance(i, list):
            flatten(i, a)
        else:
            a.append(i)
    return a

def combineBits(bitList, width=None):
    bits = flatten(bitList)  
    encodingWidth = 0
    for encoding in bits:
        encodingWidth += encoding.size    
    '''
    if width:
        if width != encodingWidth:
            print("bitlist with inconsistent width! Width:", encodingWidth, 
            "chosen width:", width)#, "data:", bitList)
            exit()
    '''
    combined = SDR( encodingWidth ).concatenate(bits)
    return encodingWidth, combined
    
def decToEnc(encoder, num, size):
    numStr = decToStr(num, size)
    bitStr = encodeStrDecimal(encoder, numStr)
    width, output = combineBits(bitStr)
    return width, output

#num = 123456789

def desiredSparsity(digits, size, bits):
    return digits / (float(size) * bits)


'''

CORRECT algorithm for calculating number of unique bits per digit
decBits        = 3
decDupBits     = 2 # per side
decSize        = decBits * 10 + decDupBits
decUniqueBits  = (decSize - decDupBits * 10 )/10
print("# unique:",decUniqueBits)
decSpars       = (decBits+decDupBits) / float(decSize)

'''

'''    
def flatten(l, a):
    for i in l:
        if isinstance(i, list):
            flatten(i, a)
        else:
            a.append(i)
    return a
'''   


'''
decBits        = 3
decDupBits     = 2 # per side
decSize        = decBits * 10 + decDupBits
decUniqueBits  = (decSize - decDupBits * 10 )/10
print("# unique:",decUniqueBits)
decSpars       = (decBits+decDupBits) / float(decSize)
'''

numSize = 200
numMin  = 0
numMax  = 100

tries = 1000

decBits        = 8
decDupBits     = 2 # per side
decSize        = decBits * 10 + decDupBits
decUniqueBits  = (decSize - decDupBits * 10 )/10
print("# unique:",decUniqueBits)
decSpars       = (decBits+decDupBits) / float(decSize)
print("Spars:", decSpars)

#ecSpars = desiredSparsity(10, decSize, 1/9)
#decSize = 30
#decSpars = 0.02
decEncoder = ScalarEncoderGenerator(0,9,decSize, decSpars)#,# decSpars)

#enc = decToEnc(decEncoder,num, 10)
#for t in enc:
#    print(t)
#exit()

size = int(math.log(numMax))

emptyWidth = decSize*(size+1)
emptyBits = SDR(emptyWidth)


print("TM")
tm = TM(columnDimensions = emptyBits.dimensions,
      cellsPerColumn=1,
      initialPermanence=0.5,
      connectedPermanence=0.5,
      minThreshold=8,
      maxNewSynapseCount=20,
      permanenceIncrement=0.1,
      permanenceDecrement=0.0,
      activationThreshold=8,
      )  

print("SP")
sp = SP(emptyBits.dimensions,
      emptyBits.dimensions,
      potentialRadius = int(0.5 * emptyBits.size),
      localAreaDensity = .02,
      globalInhibition = True,
      seed = 0,
      synPermActiveInc = 0.01,
      synPermInactiveDec = 0.008)      

def promptDecPooler(sp, encoder, digit, size, train=False):
    width, inBits = decToEnc(encoder,digit, size)
    outBits = SDR(width)
    sp.compute(inBits, train, outBits)
    return outBits, inBits
    #print(x, outBits)

def promptDecTM(tm, question, answer, learn=True):  
    tm.compute(question, learn=learn)  
    tm.activateDendrites(True)
    prediction = tm.getPredictiveCells() 
    if learn: 
        tm.compute(answer,learn=learn)  
        tm.reset()
    return prediction
        

for train in [True, False]:
    for x in range(1,tries):
        outBits, inBits = promptDecPooler(sp, decEncoder, x%100+1, size, train=train)
        print(x, outBits)
        if not train:
            #exit()
            predBits = promptDecTM(tm,outBits, inBits,learn=True)
            print("true:", inBits)
            print("prediction:", predBits)
    '''
    width, inBits = decToEnc(decEncoder,x%100+1, size)
    outBits = SDR(width)
    sp.compute(inBits, True, outBits)
    print(x, outBits)
    '''

'''      
for x in range (0,tries):
  a = random.randint(1,numMax/2)
  b = random.randint(1,numMax/2)
  c = a + b 
  
  
  aBits = decToEnc(decEncoder,a, size)
  bBits = decToEnc(decEncoder,b, size)
  cBits = decToEnc(decEncoder,c, size)
  print(a,b,c)
  #print(len(aBits),len(bBits),len(cBits))
  
  print(aBits, "\n", bBits,"\n", cBits,"\n",emptyBits)
  print(size)
  
  print(decSize)
  print(emptyWidth)
  
  print(aBits)
  
  questionBits = flatten([aBits, bBits, emptyBits])  
  answerBits = flatten([emptyBits, emptyBits, cBits])  
    
  encodingWidth = 0
  for arr in questionBits: 
    encodingWidth += arr.size    
  print(encodingWidth)
  
  question = SDR( encodingWidth ).concatenate(questionBits)#aBits + bBits +[SDR(decSize)])
  answer   = SDR( encodingWidth ).concatenate(answerBits)#aBits + bBits +[SDR(decSize)])

  activeColumns = question
  #print(activeColumns)
  tm.compute(activeColumns, learn = True)  
  tm.activateDendrites(True)
  prediction = tm.getPredictiveCells()  
  print("prediction:", tm.getPredictiveCells())
  print("true:", answer )
  #printStateTM(tm)

  #print(encoding.coordinates)  
  #print(encoding.coordinates[0])  
  activeColumns = answer
  tm.compute(activeColumns, learn = True)  
  
  #print(tm.getPredictiveCells().sparse)

  #printStateTM(tm)
  if x > tries/2:
      results.append((c, prediction))
  tm.reset()  
'''
def ScalarEncoderGenerator(mini, maxi, size, spars=-1):
  if spars == -1:
    diff = maxi-mini
    spars = 1/(diff+1)
  params            = ScalarEncoderParameters()
  params.minimum    = mini
  params.maximum    = maxi
  params.size       = size
  params.sparsity   = spars
  encoder = ScalarEncoder( params )
  return encoder

from htm.bindings.algorithms import Classifier, Predictor

def decode(decoder, encoded):
    return numpy.argmax(decoder.infer( encoded ) )

# from sp_tutorial
def corruptSDR(sdr, noiseLevel):
      """
      Corrupts a binary vector by inverting noiseLevel percent of its bits.
    
      Argument vector     (array) binary vector to be corrupted
      Argument noiseLevel (float) amount of noise to be applied on the vector.
      """
      vector = sdr.flatten().dense
      for i in range(sdr.size):
        rnd = random.random()
        if rnd < noiseLevel:
          if vector[i] == 1:
            vector[i] = 0
          else:
            vector[i] = 1
      sdr.dense = vector

def trainDecTMDecoder(sp, tm, encoder, size, noise):
    clsr = Classifier()
    errors = 0
    for train in [True, False]:
        for x in range(1,100000):
            num = x%100+1
            outBits, inBits = promptDecPooler(sp, encoder, num, size, train=False)
            predBits = promptDecTM(tm,outBits, inBits,learn=False)
            if train:
                clsr.learn(predBits, num)
            else:
                out = decode(clsr,predBits)
                if out != num:
                    print("error in decode training:", num, "->", out)
                    errors += 1
                    if errors > 10:
                        print("too many errors")
                        exit()
    return clsr    
        
        
        
def trainNumDecoder(encoder, mini, maxi, noise):
    clsr = Classifier()
    for y in range(0,10):
        for x in range(mini,maxi):
            encoded = encoder.encode(x)
            #corruptSDR(encoded, noise)
            clsr.learn(encoded, x)
    
    for x in range(mini,maxi):
        encoded = numEncoder.encode(x)
        out = decode(clsr,encoded)
        if out != x:
            print("error in decode training:", out, "->", x)
    return clsr
        
'''
numSize = 200
numMin  = 0
numMax  = 100
numSpars = 0.02
numEncoder = ScalarEncoderGenerator(numMin,numMax,numSize,numSpars)
'''
print("got here")
decDecoder = trainDecTMDecoder(sp, tm, decEncoder, size, 0)#01)

testNum = 77

outBits, inBits = promptDecPooler(sp, decEncoder, testNum, size, train=False)
predBits = promptDecTM(tm,outBits, inBits,learn=False)

result = decode(decDecoder,predBits)

print(testNum,result)

exit()
test = numEncoder.encode(7)
result = decode(numDecoder,test)
exit()
#numDecoder = trainNumDecoder(numEncoder, numMin, numMax, 0.45)#01)
#exit()
test = numEncoder.encode(7)
result = decode(numDecoder,test)
print("----")
print(7,result)


for result in results:
    val = result[0]
    prediction = None
    raw_prediction = result[1].coordinates[0]
    #print(raw_prediction)#[400:]
    if len(raw_prediction) > 0:
        prediction = SDR(numSize)
        for value in raw_prediction:
            prediction.dense[value-numSize*2] = 1
        prediction.dense = prediction.dense #updates values
        print(prediction)
        #print(prediction)
        prediction = decode(numDecoder,prediction)
    
    print(val, prediction)
    #print(prediction)
    #print(numEncoder.encode(val))

