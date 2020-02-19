from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import os
import tempfile
# 需要解压缩文件
# 需要一些系统文件
# 需要一些模板文件

import numpy
from six.moves import urllib
from six.moves import xrange
import tensorflow as tf
from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets


