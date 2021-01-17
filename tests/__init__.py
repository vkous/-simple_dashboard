#import parrent_dir
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
sys.path.append(parent_dir)
