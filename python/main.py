# -*- coding: utf-8 -*-

import numpy as np
import copy
import random
import math

class SumilatedAnneling():
  def __init__(self, width, anslen, answer_matrix, base_point, num_branch, threshold, basediff, max_time):
      self.width = width
      self.anslen = anslen
      self.answer_matrix = answer_matrix
      self.base_point = base_point
      self.num_branch = num_branch
      self.threshold = threshold
      self.basediff = basediff
      self.max_time = max_time

  def calcoutput(self,answer_order):
    output = np.zeros((self.width,self.width))
    for n in range(len(answer_order)):
      x = answer_order[n][0][0]
      y = answer_order[n][0][1]
      h = answer_order[n][1]
      for j in range(int(max(0,y-h)),int(min(self.width, y+h))):
        for k in range(int(max(0, x-h)), int(min(self.width, x+h))):
          output[j][k] = output[j][k] + max(0, h-abs(j-y) - abs(k-x))

    return output

  def calcdiff(self,matrix1,matrix2):
    diff = 0

    for i in range(len(matrix1)):
      for j in range(len(matrix1)):
        diff= diff + abs(matrix1[i][j]-matrix2[i][j])
    return diff

  def calcscore(self,answer_order):
    output_matrix = self.calcoutput(answer_order)
    diff = self.calcdiff(output_matrix,self.answer_matrix)
    score = self.base_point - diff
    return score

  def createbranch(self, answer_order, trynum):
    branch = []
    for i in range(self.num_branch):
      chg = copy.deepcopy(answer_order)

      for k in range(int(trynum)):
        kth_index = random.randint(0, len(answer_order)-1)
        x = math.floor(random.random() * self.width)
        y = math.floor(random.random() * self.width)
        h = math.floor(random.random() * self.width + 1)
        chg[kth_index] = [[x,y],h]

      branch.append(chg)
    return branch

  def selectbranch(self,branch,nowanswer,nowscore):
    maxans = nowanswer
    maxscore = math.floor(nowscore)
    for i in range(self.num_branch):
      score = math.floor(self.calcscore(branch[i]))
      if score > maxscore:
        maxscore = score
        maxans = branch[i]
    if not maxscore == nowscore:

      if random.random() < self.threshold:

        answer_order = maxans
        answer_score = maxscore

        return answer_order, answer_score
      else:
        return nowanswer, nowscore
    else:
      return nowanswer, nowscore

  def updatetrynum(self,nowscore):

    trynum = (self.base_point -nowscore)/self.basediff * self.anslen

    return trynum

  def slove(self, initial_order, initial_score, initial_trynum):
    anneling_time = 0
    noworder = initial_order
    nowscore = initial_score
    trynum = initial_trynum

    while anneling_time < self.max_time and nowscore < self.base_point:
      branch = self.createbranch(noworder, trynum)
      noworder, nowscore = self.selectbranch(branch, noworder, nowscore)
      trynum = self.updatetrynum(nowscore)
      anneling_time = anneling_time + 1

    return noworder, nowscore

  def output_answer(self, initial_order, initial_score, initial_trynum):
    answer_order, answer_score = self.slove(initial_order, initial_score, initial_trynum)
    print(answer_score)
    for n in range(len(answer_order)):
      print(answer_order[n][0][0], answer_order[n][0][1],answer_order[n][1])

    return None

#?????????????????????
N_MAX = 105 # ??????????????????????????????(??????????????????)
BASE_POINT_MAX = 2e8
N = 10  # ????????????(=??????)
Q = 30  # ????????????????????????
NUM_BRANCH = 4 # ???????????????
MAX_TIME = 30 # ?????????????????????
BASE_DIFF = 10 * 10 * 30 * 10
trynum = Q  # Number of Modifications(1???????????????????????????????????????????????????????????????)
threshold = 0.8 # ??????????????????????????????????????????????????????????????????????????????????????????????????????

#??????????????????
mountain = []
for n in range(N):
  i = math.floor(random.random() * N)
  j = math.floor(random.random() * N)
  h = math.floor(random.random() *N + 1)
  mountain.append([[i,j],h])

#???????????????
#????????????
input_matrix = np.array([[20, 20, 18, 17, 17, 15, 14, 11, 8, 6],
                         [20, 20, 18, 17, 17, 16, 13, 10, 8, 6],
                         [18, 18, 17, 16, 16, 15, 12, 9, 6, 5],
                         [16, 17, 16, 16, 16, 14, 13, 10, 6, 4],
                         [14, 14, 14, 14, 14, 13, 12, 11, 7, 4],
                         [11, 10, 10, 10, 11, 10, 11, 12, 7, 4],
                         [9, 7, 6, 7, 8, 9, 12, 13, 9, 5],
                         [7, 5, 4, 4, 7, 9, 11, 13, 9, 6],
                         [5, 5, 3, 4, 7, 9, 12, 13, 10, 8],
                         [4, 3, 3, 4, 6, 8, 11, 12, 10, 8]])




sa = SumilatedAnneling(N, Q, input_matrix, BASE_POINT_MAX,NUM_BRANCH,threshold, BASE_DIFF, MAX_TIME)

initial_score = sa.calcscore(mountain)

sa.output_answer(mountain, initial_score, trynum)
