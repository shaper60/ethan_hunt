# coding: utf-8

def pkgen(length=16):
  """
  ランダムな文字数列を作成する
  ObjectIDの生成とかに使う
  @params length: 文字数列の長さ
  @type length: int
  @return pk: 文字数列
  @rtype pk: str
  """
  from base64 import b32encode
  from hashlib import sha1
  from random import random
  rude = ('lol',)
  bad_pk = True
  while bad_pk:
    pk = b32encode(sha1(str(random())).digest()).lower()[:length]
    bad_pk = False
    for rw in rude:
      if pk.find(rw) >= 0: bad_pk = True
  return pk

# def weakpkgen(length=8):
#   """
#   ランダムな整数を作成する
#   @params length: 整数の桁数
#   @type length: int
#   @return pk: 整数
#   @rtype pk: int
#   """
#   from random import randint
#   maxint = reduce(lambda x,y: x+y, [9*10**n for n in range(length)])
#   pk = randint(0, maxint)
#   return pk
