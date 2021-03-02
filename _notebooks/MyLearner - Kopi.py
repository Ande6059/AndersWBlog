fastai_neuralnet_from_scratch
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 761,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "#hide\n",
    "#!pip install -Uqq fastbook\n",
    "import fastbook\n",
    "fastbook.setup_book()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 762,
   "outputs": [],
   "source": [
    "#hide\n",
    "from fastai.vision.all import *\n",
    "from fastbook import *\n",
    "\n",
    "matplotlib.rc('image', cmap='Greys')\n"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 763,
   "outputs": [],
   "source": [
    "import torch\n",
    "torch.cuda.empty_cache()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 764,
   "outputs": [],
   "source": [
    "import base64\n",
    "from io import BytesIO\n",
    "from PIL import Image\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import requests\n",
    "import bs4 as bs\n",
    "\n",
    "import regex as re\n",
    "\n",
    "import seaborn as sns\n",
    "sns.set_style()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 765,
   "outputs": [],
   "source": [
    "path = untar_data(URLs.MNIST_SAMPLE)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 766,
   "outputs": [],
   "source": [
    "Path.BASE_PATH = path"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 767,
   "outputs": [
    {
     "data": {
      "text/plain": "(#3) [Path('labels.csv'),Path('train'),Path('valid')]"
     },
     "execution_count": 767,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "path.ls()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 768,
   "outputs": [],
   "source": [
    "def init_params(size, std=1.0): return (torch.randn(size)*std).requires_grad_()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 769,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11., 12., 13., 14., 15., 16., 17., 18., 19.])"
     },
     "execution_count": 769,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "time = torch.arange(0,20).float(); time"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 770,
   "outputs": [
    {
     "data": {
      "text/plain": "<Figure size 432x288 with 1 Axes>",
      "image/png": "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\n"
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "speed = torch.randn(20)*3 + 0.75*(time-9.5)**2 + 1\n",
    "plt.scatter(time,speed);"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 771,
   "outputs": [],
   "source": [
    "def f(t, params):\n",
    "    a,b,c = params\n",
    "    return a*(t**2) + (b*t) + c"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 772,
   "outputs": [],
   "source": [
    "def mse(preds, targets): return ((preds-targets)**2).mean().sqrt()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Step 1: Initialize the parameteres"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 773,
   "outputs": [],
   "source": [
    "params = torch.randn(3).requires_grad_()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 774,
   "outputs": [],
   "source": [
    "#hide\n",
    "orig_params = params.clone()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Step 2: Calculate the predictions"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 775,
   "outputs": [],
   "source": [
    "preds = f(time, params)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 776,
   "outputs": [],
   "source": [
    "def show_preds(preds, ax=None):\n",
    "    if ax is None: ax=plt.subplots()[1]\n",
    "    ax.scatter(time, speed)\n",
    "    ax.scatter(time, to_np(preds), color='red')\n",
    "    ax.set_ylim(-300,100)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 777,
   "outputs": [
    {
     "data": {
      "text/plain": "<Figure size 432x288 with 1 Axes>",
      "image/png": "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\n"
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "show_preds(preds)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Step 3: Calculate the loss"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 778,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor(178.9218, grad_fn=<SqrtBackward>)"
     },
     "execution_count": 778,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "loss = mse(preds, speed)\n",
    "loss"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Step 4: Calculate the gradients"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 779,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([166.2099,  10.6992,   0.6881])"
     },
     "execution_count": 779,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "loss.backward()\n",
    "params.grad"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 780,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([1.6621e-03, 1.0699e-04, 6.8806e-06])"
     },
     "execution_count": 780,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "params.grad * 1e-5"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 781,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([1.1480, 0.5953, 0.2770], requires_grad=True)"
     },
     "execution_count": 781,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "params"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Step 5: Step the weights\n",
    "Update the parameters:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 782,
   "outputs": [],
   "source": [
    "lr = 1e-5\n",
    "params.data -= lr * params.grad.data\n",
    "params.grad = None"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "See if it has improved:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 783,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor(178.6444, grad_fn=<SqrtBackward>)"
     },
     "execution_count": 783,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "preds = f(time,params)\n",
    "mse(preds, speed)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 784,
   "outputs": [
    {
     "data": {
      "text/plain": "<Figure size 432x288 with 1 Axes>",
      "image/png": "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\n"
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "show_preds(preds)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 785,
   "outputs": [],
   "source": [
    "def apply_step(params, prn=True):\n",
    "    preds = f(time, params)\n",
    "    loss = mse(preds, speed)\n",
    "    loss.backward()\n",
    "    params.data -= lr * params.grad.data\n",
    "    params.grad = None\n",
    "    if prn: print(loss.item())\n",
    "    return preds"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Step 6: Repeat the process"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 786,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "178.6444091796875\n",
      "178.3670196533203\n",
      "178.0896453857422\n",
      "177.81228637695312\n",
      "177.53494262695312\n",
      "177.25762939453125\n",
      "176.98031616210938\n",
      "176.7030029296875\n",
      "176.42576599121094\n",
      "176.14849853515625\n"
     ]
    }
   ],
   "source": [
    "for i in range(10): apply_step(params)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 787,
   "outputs": [],
   "source": [
    "#hide\n",
    "params = orig_params.detach().requires_grad_()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 788,
   "outputs": [
    {
     "data": {
      "text/plain": "<Figure size 864x216 with 4 Axes>",
      "image/png": "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\n"
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "_,axs = plt.subplots(1,4,figsize=(12,3))\n",
    "for ax in axs: show_preds(apply_step(params, False), ax)\n",
    "plt.tight_layout()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Step 7: Stop"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "## The MNIST Loss Function"
   ],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 789,
   "outputs": [
    {
     "data": {
      "text/plain": "(#6131) [Path('train/3/10.png'),Path('train/3/10000.png'),Path('train/3/10011.png'),Path('train/3/10031.png'),Path('train/3/10034.png'),Path('train/3/10042.png'),Path('train/3/10052.png'),Path('train/3/1007.png'),Path('train/3/10074.png'),Path('train/3/10091.png')...]"
     },
     "execution_count": 789,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "threes = (path/'train'/'3').ls().sorted()\n",
    "sevens = (path/'train'/'7').ls().sorted()\n",
    "threes"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 790,
   "outputs": [
    {
     "data": {
      "text/plain": "(6131, 6265)"
     },
     "execution_count": 790,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "seven_tensors = [tensor(Image.open(o)) for o in sevens]\n",
    "three_tensors = [tensor(Image.open(o)) for o in threes]\n",
    "len(three_tensors),len(seven_tensors)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 791,
   "outputs": [
    {
     "data": {
      "text/plain": "torch.Size([6131, 28, 28])"
     },
     "execution_count": 791,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "stacked_sevens = torch.stack(seven_tensors).float()/255\n",
    "stacked_threes = torch.stack(three_tensors).float()/255\n",
    "stacked_threes.shape"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 792,
   "outputs": [
    {
     "data": {
      "text/plain": "(torch.Size([1010, 28, 28]), torch.Size([1028, 28, 28]))"
     },
     "execution_count": 792,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "valid_3_tens = torch.stack([tensor(Image.open(o))\n",
    "                            for o in (path/'valid'/'3').ls()])\n",
    "valid_3_tens = valid_3_tens.float()/255\n",
    "valid_7_tens = torch.stack([tensor(Image.open(o))\n",
    "                            for o in (path/'valid'/'7').ls()])\n",
    "valid_7_tens = valid_7_tens.float()/255\n",
    "valid_3_tens.shape,valid_7_tens.shape"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 793,
   "outputs": [],
   "source": [
    "train_x = torch.cat([stacked_threes, stacked_sevens]).view(-1, 28*28)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 794,
   "outputs": [
    {
     "data": {
      "text/plain": "(torch.Size([12396, 784]), torch.Size([12396, 1]))"
     },
     "execution_count": 794,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "train_y = tensor([1]*len(threes) + [0]*len(sevens)).unsqueeze(1)\n",
    "train_x.shape,train_y.shape"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 795,
   "outputs": [
    {
     "data": {
      "text/plain": "(torch.Size([784]), tensor([1]))"
     },
     "execution_count": 795,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dset = list(zip(train_x,train_y))\n",
    "x,y = dset[0]\n",
    "x.shape,y"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 796,
   "outputs": [],
   "source": [
    "valid_x = torch.cat([valid_3_tens, valid_7_tens]).view(-1, 28*28)\n",
    "valid_y = tensor([1]*len(valid_3_tens) + [0]*len(valid_7_tens)).unsqueeze(1)\n",
    "valid_dset = list(zip(valid_x,valid_y))"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 797,
   "outputs": [],
   "source": [
    "weights = init_params((28*28,1))"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 798,
   "outputs": [],
   "source": [
    "bias = init_params(1)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 799,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([2.8989], grad_fn=<AddBackward0>)"
     },
     "execution_count": 799,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "(train_x[0]*weights.T).sum() + bias"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 800,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([[ 2.8989],\n        [ 4.2560],\n        [-0.2983],\n        ...,\n        [ 7.7305],\n        [13.6528],\n        [ 5.9436]], grad_fn=<AddBackward0>)"
     },
     "execution_count": 800,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def linear1(xb): return xb@weights + bias\n",
    "preds = linear1(train_x)\n",
    "preds"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 801,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([[ True],\n        [ True],\n        [False],\n        ...,\n        [False],\n        [False],\n        [False]])"
     },
     "execution_count": 801,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "corrects = (preds>0.0).float() == train_y\n",
    "corrects"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 802,
   "outputs": [
    {
     "data": {
      "text/plain": "0.4309454560279846"
     },
     "execution_count": 802,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "corrects.float().mean().item()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 803,
   "outputs": [],
   "source": [
    "weights[0] *= 1.0001"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 804,
   "outputs": [
    {
     "data": {
      "text/plain": "0.4309454560279846"
     },
     "execution_count": 804,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "preds = linear1(train_x)\n",
    "((preds>0.0).float() == train_y).float().mean().item()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 805,
   "outputs": [],
   "source": [
    "trgts  = tensor([1,0,1])\n",
    "prds   = tensor([0.9, 0.4, 0.2])"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 806,
   "outputs": [],
   "source": [
    "def mnist_loss(predictions, targets):\n",
    "    return torch.where(targets==1, 1-predictions, predictions).mean()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 807,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([0.1000, 0.4000, 0.8000])"
     },
     "execution_count": 807,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "torch.where(trgts==1, 1-prds, prds)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 808,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor(0.4333)"
     },
     "execution_count": 808,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mnist_loss(prds,trgts)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 809,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor(0.2333)"
     },
     "execution_count": 809,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mnist_loss(tensor([0.9, 0.4, 0.8]),trgts)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 810,
   "outputs": [],
   "source": [
    "def sigmoid(x): return 1/(1+torch.exp(-x))"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 811,
   "outputs": [
    {
     "data": {
      "text/plain": "<Figure size 432x288 with 1 Axes>",
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAXcAAAEMCAYAAAA/Jfb8AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjMuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8QVMy6AAAACXBIWXMAAAsTAAALEwEAmpwYAAAlXUlEQVR4nO3deXyU1dn/8c8FBBISErYQ9h1kU0AiKG51q0vr0qLVqrhhLah1a/urrY+7XbSLffSxKk9RFNz3rdpWrVbUKvsS9jVsIYFA9j3X748JPjEmMECSe2byfb9e85K558xwOcx8c3Luc59j7o6IiMSWVkEXICIijU/hLiISgxTuIiIxSOEuIhKDFO4iIjFI4S4iEoMU7hJzzOwuM1sbdB17mdlMM3t/P22uMLPK5qpJYp/CXaKKmSWY2b1mtsbMSsxsl5nNNbMbajX7A3B0UDXW40bggqCLkJalTdAFiBygR4GTCAXmYiAZGAv03dvA3QuBwkCqq4e75wVdg7Q86rlLtDkP+L27v+7uG9x9sbvPdPd79jaob1jGzG4ysy1mVmxmfzezyWbmZta75vErzKzSzE4ys6U1vxV8bGY9zewEM1toZkVm9r6Z9arz2peb2XIzK6v5O+4zsza1Hv/asIyF3Gtm2WZWaGbPA52a6P2SFkrhLtFmO3CGmXUO9wlm9n1CQzW/B0YDzwH319O0FXAncDVwLNATeAG4B5gGHAf0Bv5U67W/AzwBzAIOB34KXFfzOg25AbgF+DlwJLBgP+1FDpy766Zb1NwIhe4moApYAkwHzgWsVpu7gLW17n8KzKrzOr8DHOhdc/+KmvtjarX5ec2xcbWO3QzsrHX/E+DFOq99I1ACtK25PxN4v9bjW4Bf13nOy0Bl0O+vbrFzU89dooq7fwoMAo4HngLSgFeAN83MGnjaCOA/dY59Xt/LA0tr3c+q+e+SOse6mFnrmvsjgX/XeZ2PgfiaOr/GzJKBXsBndR6a00DtIgdF4S5Rx90r3f0zd/+ju59LqNf9XeCEfT0tjJeudvequs9x94p6XsfqOUadx+r7O/f1mEijUbhLLFhR899uDTy+HDimzrHGmiqZAZxY59gJhIZl1tdt7KGZM1sJDS/VVve+yCHRVEiJKmb2MaETovOAHGAw8BtgD/CvBp72R+AFM/sSeBeYCFxW89ih9qB/C7xlZrcCrwJjCI35/9Hdy/dRz71mtpLQcNE5wKmHWIfI16jnLtHmXeAS4G/AKuBJYA1wrLvvrO8J7v4q8P+AWwmNqV8C3F3zcOmhFOPufwOuAi4HlgEPAn+p9fr1+W/goZq2iwj9VnHPPtqLHDBz19CftDxmdgdwo7t3CboWkaagYRmJeWYWR2j++d+AIkJXuP4ceCTIukSaknruEvNqrhZ9GxgHdAA2AE8TutJVi3VJTFK4i4jEIJ1QFRGJQREx5t61a1fv379/0GWIiESV+fPn73T31Poei4hw79+/P/PmzQu6DBGRqGJmmxp6TMMyIiIxKKxwN7PrzWxezXrVM/fT9mYzyzKzPDN7wszaNUqlIiIStnB77tuA+witW90gMzud0FWApwD9gYHs+0o9ERFpAmGFu7u/6u6vA7v20/RyYIa7Z7j7buBeQiv2iYhIM2rsMfeRhPa13GsxkGZmusRbRKQZNXa4JwG1NwPe++cOdRua2TU14/jzcnJyGrkMEZGWrbHDvZDQbvR77f1zQd2G7j7d3dPdPT01td5pmiIicpAae557BqENiF+suT8a2OHu+xurFxGJae5OblE5WfmlZOeXkV1Qyo78Msb27cjxQxq/gxtWuNcsvNQGaA20NrN4Qpv51l106Wlgppk9Q2iX+v8itDmwiEhMK6+sZuueErbsLmbL7hK27i5h254Stu4pYXteKVn5pZRXVn/jedO+NSi4cCcU0nfWun8pcLeZPUFoC7MR7p7p7u+Z2QOEdsRJILRx8Z3feDURkShUUVVNZm4x63OK2LCzkA07i9m4s4jM3GK255VQXWsdxtatjO7J8fTsGM+YPh3p0TGe7smhW7fkeLp1aEdqh3bEx7Vu+C88BBGxKmR6erpr+QERiRRV1c6GnYWszCpg9Y5C1uwoYE12IZt2FVFR9X+Z2al9HP27JtKvc3v6dkmkb+f29OmUQO/O7Unr0I42rZt2EQAzm+/u6fU9FhFry4iIBKW0oopVWQUs3ZpHxrY8MrblsyqrgLKaIZRWBv26JDK4WxKnjUhjcGoSA1MTGdg1iZT2cQFX3zCFu4i0GO5OZm4x8zftZmHmHhZv2cOK7flf9cZTEuIY2TOZyUf3Y3iPZIb16MCg1KQmGzppSgp3EYlZ1dXOiqx8vlify5cbcpm3aTc7C8sASGzbmiN6d+Tq4wdyRK8URvVKoXenBMws4Kobh8JdRGLKxp1FzFm7k0/X7uSzdbvIK6kAoHenBI4f0pVx/TqR3r8TQ7p1oHWr2Ajy+ijcRSSqlVZU8fm6XXy0KpuPVuewaVcxAD1T4vn2iDSOGdSFCQO70KtjQsCVNi+Fu4hEnT3F5fxz+Q7eX7GDf6/eSUlFFfFxrZg4qCtTjhvA8UNS6d+lfcwMsRwMhbuIRIXdReW8l5HF35Zu5/N1u6isdnqkxHP+uN6cMrwbRw/sEpUnPpuKwl1EIlZJeRX/WJ7Fm4u28fHqHCqrnX5d2vOjEwZy5qjuHN4rpUX3zvdF4S4iEcXdWZC5m5fnb+HtxdspKKuke3I8Vx03gHNG92Rkz2QFehgU7iISEfKKK3hlwRae/TKTtdmFJMS15qzDezBpXC+OHtCFVjE8s6UpKNxFJFDLt+Uz87MNvLFoG2WV1Yzu05EHJh3BWUf0IKmdIupg6Z0TkWZXXe28v2IHM+Zs4IsNucTHteL7R/bm0qP7MrJnStDlxQSFu4g0m7LKKl5fuJXH/72e9TlF9OqYwK/OGsaF6X0jep2WaKRwF5EmV1pRxfNfZvLYx+vJyi9lZM9kHvrhWM4a1b3JV05sqRTuItJkSiuqeOaLTB77eB05BWWMH9CZ319wBMcN7qoZL01M4S4ija6yqpqX52/hvz9Yw/a8UiYO6sLDPxzL0QO7BF1ai6FwF5FG4+68vyKb3767gvU5RYzp05E/XjCaiYO7Bl1ai6NwF5FGsWxrHve+vZwvNuQyMDWR6ZPHcdqINA2/BEThLiKHJLeonN//fRXPz82kU/u23HvuSC4a35c4nSgNlMJdRA5KdbXz7JeZ/P7vqygsq+TKiQO46bQhJMdrSmMkULiLyAFbmZXPL19dysLMPRwzsAt3nzuSoWkdgi5LalG4i0jYSiuqeOiDNUz/93qSE+J48MLRnDeml8bVI5DCXUTCsjBzNz9/eQlrsws5f1xvbjtrOJ0S2wZdljRA4S4i+1RWWcWD/1zD9H+vIy05nqeuGs+JQ1ODLkv2Q+EuIg1avaOAG59fxIrt+VyY3ofbvjtcJ0yjhMJdRL7B3Xnqs4389t2VJLVrw18vS+fUEWlBlyUHQOEuIl+zp7icn720hPdX7OCkw1J54PzRpHZoF3RZcoAU7iLylfmbdnPDcwvJLijl9u+O4Kpj+2smTJRSuIsI7s6Tn27kN39bQY+O8bw8dSKj+3QMuiw5BAp3kRauuLySX766lDcWbePU4Wn88QejSUnQSdNop3AXacEydxVzzax5rNpRwM9PP4xpJw7SRtQxIqyVfcyss5m9ZmZFZrbJzC5uoJ2Z2X1mttXM8szsIzMb2bgli0hj+HzdLs59ZA7b80qZeeV4rjtpsII9hoS7bNsjQDmQBlwCPNpAaF8AXAUcD3QGPgdmNUKdItKInv0ik8kzvqBLUjveuO5YXZQUg/Yb7maWCEwCbnf3QnefA7wJTK6n+QBgjruvd/cqYDYwojELFpGDV1Xt3Pv2cn712lKOG9KVV6+dSP+uiUGXJU0gnJ77UKDK3VfXOrYYqK/n/jww2MyGmlkccDnw3qGXKSKHqqS8imufmc+MORu4YmJ/Zlx+lK42jWHhnFBNAvLqHMsD6lvfczvwCbAKqAI2AyfX96Jmdg1wDUDfvn3DLFdEDsauwjKmPDWPxVv2cMd3R3DVcQOCLkmaWDg990Iguc6xZKCgnrZ3AkcBfYB44G7gQzNrX7ehu09393R3T09N1XifSFPZnFvM+Y99zsqsfB67dJyCvYUIJ9xXA23MbEitY6OBjHrajgZecPct7l7p7jOBTmjcXSQQK7bnM+nRz8gtKueZqydw+sjuQZckzWS/4e7uRcCrwD1mlmhmxwLnUv8smLnABWaWZmatzGwyEAesbcyiRWT/5m7M5QePf04rM16aegzj+nUOuiRpRuFexHQt8ASQDewCprl7hpn1BZYDI9w9E7gf6AYsAhIJhfokd9/TyHWLyD58siaHHz09j54pCTw9ZTy9O31jZFRiXFjh7u65wHn1HM8kdMJ17/1S4Lqam4gE4B8ZWVz/7EIGpiYya8oErejYQmn5AZEY8tbibdz0wiJG9UrhqSuPomN7bYPXUincRWLEG4u2cvMLi0jv15kZV6TTQXPYWzSFu0gMeH3hVm55cRFH9e/ME1ccRWI7fbVbOn0CRKLc3mAfPyAU7O3b6mstCneRqPbOku3c8uIiJgzowhNXHEVC29ZBlyQRItxVIUUkwvwjI4sbn1/IkX07MeOKdAW7fI3CXSQKfbw6h+ufXcjIXik8eaWGYuSbFO4iUWbexlx+PGseg7ol8fSV4zUrRuqlcBeJIsu35XPlzLn0TElg1pTxpLRXsEv9FO4iUWLDziIue+JLktq1YdbVE+iapCtPpWEKd5EokJ1fyuQZX1DtzqwpE+jVMSHokiTCKdxFIlx+aQWXPzmX3KJyZl55FIO7Je3/SdLiKdxFIlhZZRVTZ81nzY4CHrt0HEf07hh0SRIlNH9KJEJVVzs/e2kJn63bxYMXjuaEodqxTMKnnrtIhLr/7yt5a/E2bj1zGN8b2zvociTKKNxFItDs/2zi8Y/Xc+nRffnxCQODLkeikMJdJMJ8uHIHd7yxjJOHdeOus0diZkGXJFFI4S4SQZZvy+f6ZxcyomcyD/9wLG1a6ysqB0efHJEIkZ1fytVPzSUlIY4Zl2tNdjk0+vSIRICS8ip+9PQ89pRU8NLUY0hLjg+6JIlyCneRgIWmPC5mydY8Hr90HCN7pgRdksQADcuIBOyhD9fwztLt3HrGML49snvQ5UiMULiLBOjdpdv58/trmHRkb67RlEdpRAp3kYBkbMvjlhcXM7ZvR379vVGa8iiNSuEuEoCdhWVc8/R8OraP4/HJ44iP0xZ50rh0QlWkmVVUVXPdMwvYWVjGy1Mn0q2DZsZI41O4izSzX7+zgi825PLghaM5vLdmxkjT0LCMSDN6ad5mZn62kSnHDdBiYNKkFO4izWTJlj3c9voyJg7qwi/PHBZ0ORLjFO4izWBXYRlTZ80nNakd/3PxkVozRpqcxtxFmlhlVTU3PL+QnUXlvDJ1Ip0T2wZdkrQAYXUfzKyzmb1mZkVmtsnMLt5H24Fm9raZFZjZTjN7oPHKFYk+f/jHaj5du4v7zhulE6jSbML93fARoBxIAy4BHjWzkXUbmVlb4J/Ah0B3oDcwu3FKFYk+7y3L4rGP13HxhL78IL1P0OVIC7LfcDezRGAScLu7F7r7HOBNYHI9za8Atrn7n9y9yN1L3X1Jo1YsEiXW5xTys5cWM7pPR+48e0TQ5UgLE07PfShQ5e6rax1bDHyj5w4cDWw0s3drhmQ+MrPDG6NQkWhSXF7JtNkLiGtt/OWSI2nXRlegSvMKJ9yTgLw6x/KADvW07Q1cBDwE9ATeAd6oGa75GjO7xszmmdm8nJycA6taJIK5O7e9tozV2QX8+aKx9OqYEHRJ0gKFE+6FQHKdY8lAQT1tS4A57v6uu5cDfwC6AMPrNnT36e6e7u7pqampB1i2SOR65otMXlu4lZtOGcqJQ/XZlmCEE+6rgTZmNqTWsdFARj1tlwDeGIWJRKOlW/K4563lnDA0lZ+cPDjocqQF22+4u3sR8Cpwj5klmtmxwLnArHqazwaONrNTzaw1cBOwE1jReCWLRKa84gqufXY+XZLa8ucLx9CqlZbwleCEOxXyWiAByAaeA6a5e4aZ9TWzQjPrC+Duq4BLgceA3YR+CJxTM0QjErPcnZ+9vJjte0r5n4uP1IVKEriwrlB191zgvHqOZxI64Vr72KuEevoiLcZfP9nAP5fv4PbvjmBcv05BlyOitWVEDtX8Tbu5/72VnDGyO1cd2z/ockQAhbvIIdldVM5Pnl1Aj47x3H/+EdoqTyKGFg4TOUjV1c5PX1rMzsJyXpk2kZSEuKBLEvmKeu4iB+l/P1nPhyuzue07w7UgmEQchbvIQZi/KZcH/r6Ksw7vzmXH9Au6HJFvULiLHKDQOPtCenVM4HeTNM4ukUlj7iIHwN35Wa1x9uR4jbNLZFLPXeQA/PWTDXywMptfnTVM4+wS0RTuImFamBmaz376yDQun9g/6HJE9knhLhKGvOIKrn92Id1T4nng/NEaZ5eIpzF3kf1wd37xyhJ25Jfy0tRjNJ9dooJ67iL78fTnm3gvI4tfnDGMsX21boxEB4W7yD4s25rHr99ZwcnDunH18QOCLkckbAp3kQYUlFZw/bML6JLUlj9eoHF2iS4acxeph7vzq9eWsXl3Cc9fczSdtD67RBn13EXq8cLczby1eBu3nDaUo/p3DrockQOmcBepY1VWAXe+mcFxg7sy7cRBQZcjclAU7iK1FJdXct2zC+gQH8eD2gdVopjG3EVqueONDNblFDJ7ygRSO7QLuhyRg6aeu0iNV+Zv4eX5W/jJyUM4dnDXoMsROSQKdxFgbXYB//X6MsYP6MyNpwwJuhyRQ6ZwlxavpLyK655ZSELb1jx00Vhaa5xdYoDG3KXFu+vNDFbtKOCpq8bTPSU+6HJEGoV67tKivb5wKy/M28y13xrEiUNTgy5HpNEo3KXFWptdyK9eW8pR/Ttxy2lDgy5HpFEp3KVFCo2zLyA+rjUP/XAsbVrrqyCxRWPu0iLtHWefeeVR9EhJCLockUan7oq0OK8u2MIL8zZz3UmD+NZh3YIuR6RJKNylRVmzo4DbXgvNZ7/5VI2zS+xSuEuLUVRWybRnFpDYrjX/o3F2iXEac5cWwd257bWlrK9ZN6ZbsuazS2wLq+tiZp3N7DUzKzKzTWZ2cRjP+dDM3Mz0A0QC9+yXmby+aBs3nzqUiVo3RlqAcIP3EaAcSAPGAO+Y2WJ3z6ivsZldcgCvLdKklmzZw91vLufEoalcd9LgoMsRaRb77bmbWSIwCbjd3QvdfQ7wJjC5gfYpwJ3A/2vMQkUOxp7icqbNXkBqh3Zan11alHCGZYYCVe6+utaxxcDIBtr/BngUyDrE2kQOSXW1c9MLi8gpKOMvlxxJZ+2DKi1IOOGeBOTVOZYHdKjb0MzSgWOBh/f3omZ2jZnNM7N5OTk54dQqckAe/nAtH63K4Y6zRzC6T8egyxFpVuGEeyGQXOdYMlBQ+4CZtQL+Atzo7pX7e1F3n+7u6e6enpqqBZukcX20Kps/f7Ca743txSUT+gZdjkizCyfcVwNtzKz2DgajgbonU5OBdOAFM8sC5tYc32Jmxx9ypSJhytxVzI3PL+KwtA785nuHY6Zxdml59jujxd2LzOxV4B4zu5rQbJlzgYl1muYBPWvd7wN8CYwDNO4izaKkvIqps+fj7jw+eRwJbVsHXZJIIMK9RO9aIAHIBp4Dprl7hpn1NbNCM+vrIVl7b/xfoO9w9/ImqF3ka9yd215fyoqsfP77orH065IYdEkigQlrLrq75wLn1XM8k9AJ1/qesxHQ78PSbJ7+fBOvLtjKTacO4aRhWhBMWjYtriEx4fN1u7jn7eWcOjyNG07WBtciCneJelv3lHDdswvo36U9D144WhcqiaBwlyhXWlHFj2fNo6KymumXpdMhPi7okkQigtZ/kajl7vz85SVkbMvnr5elMyi13tM/Ii2Seu4Stf7y0TreWryNn59+GKcMTwu6HJGIonCXqPSPjCx+//dVnDumJ9NOHBR0OSIRR+EuUWdlVj43v7CI0b1TuH/SEboCVaQeCneJKjkFZUyZOY+k+DY8Pjmd+DhdgSpSH51QlahRWlHFNbPmkVtUzktTj6F7irbKE2mIwl2iwt6ZMQsz9/DYpeMY1Ssl6JJEIpqGZSQqPPjP1by1eBu/OGMYZ4zqHnQ5IhFP4S4R78W5m3now7VcmN6HqScODLockaigcJeI9smaHH712lJOGJrKfd8bpZkxImFSuEvEWrE9n2mzFzC4WxKPXDyWuNb6uIqES98WiUhbdhdzxZNfktSuDU9eeZTWjBE5QAp3iTi7i8q57IkvKSmv4ukp4+mRkhB0SSJRR1MhJaKUlFdx1VNz2bK7hNlTJjA0rUPQJYlEJfXcJWKUV1Zz7TPzWbx5Dw9dNJbxAzoHXZJI1FLPXSJCVbXz05cW869VOfz2+4drLrvIIVLPXQLn7tzxxjLeWryNW88cxg/H9w26JJGop3CXQLk7D/x9Fc98kcnUEwcxVcv3ijQKhbsE6qEP1vLoR+u4eEJffnHGYUGXIxIzFO4SmMc/XseD76/m/HG9ue9cXX0q0pgU7hKIJz/dwG/fXcnZo3ty/6QjaNVKwS7SmDRbRprdE3M2cM/byzljZHf+9IPRtFawizQ6hbs0q79+sp773lnBGSO787DWixFpMvpmSbPZG+xnjlKwizQ19dylybk7D3+4lj/9czXfObwHf75ojIJdpIkp3KVJuTu/e28lj3+8nklH9ub+SYfTRsEu0uQU7tJkqqqdO99cxuz/ZDL56H7cfc5IzYoRaSYKd2kSZZVV3PLCYt5Zup0fnziQW88YpnnsIs0orN+Pzayzmb1mZkVmtsnMLm6g3eVmNt/M8s1si5k9YGb6AdLCFJZVctXMubyzdDu3nTWcX545XMEu0szCHfx8BCgH0oBLgEfNbGQ97doDNwFdgQnAKcDPDr1MiRbZ+aVcNP1z/rM+lz9eMJofnaANrUWCsN9etZklApOAUe5eCMwxszeBycCttdu6+6O17m41s2eAkxqxXolgq3cUcOWTc9ldXM5fL0vnpGHdgi5JpMUKZ8hkKFDl7qtrHVsMnBjGc08AMg6mMIkun67dydRZ84lv25oXf3wMo3qlBF2SSIsWTrgnAXl1juUB+9z/zMyuBNKBqxt4/BrgGoC+fbV+dzR75otN3PlGBgNTE3nyyvH06qg9T0WCFk64FwLJdY4lAwUNPcHMzgN+B5zq7jvra+Pu04HpAOnp6R5OsRJZKququfft5Tz1+SZOHJrKwxePJTk+LuiyRITwwn010MbMhrj7mppjo2lguMXMzgD+F/iOuy9tnDIl0uQWlXPDcwuZs3YnPzp+ALeeOVwLgIlEkP2Gu7sXmdmrwD1mdjUwBjgXmFi3rZmdDDwDfM/dv2zkWiVCLN2Sx9TZ88kpLOOB84/gB+l9gi5JROoIdyrktUACkA08B0xz9wwz62tmhWa2d9D8diAF+FvN8UIze7fxy5agvDhvM5Me+wyAl6ceo2AXiVBhXWDk7rnAefUczyR0wnXvfU17jFHF5ZXc8UYGL8/fwnGDu/LQD8fSObFt0GWJSAN09ajs16qsAq57dgHrcgq54ZQh3HjKEI2vi0Q4hbs0yN2Z/UUmv35nOUnt4pg9ZQLHDu4adFkiEgaFu9Qrp6CMX7yyhA9XZnPC0FT+cMERdOsQH3RZIhImhbt8w3vLsrjttaUUlFVy19kjuOyY/lqqVyTKKNzlK7lF5dz5ZgZvLd7GyJ7JPHfhGIam7fNCZBGJUAp3wd15Z+l27nozg7ySCm45bSjTvjVIW+GJRDGFewu3ObeYO95Yxr9W5XB4rxRmTZnA8B51V5sQkWijcG+hyiqrmDFnAw9/sBYzuP27I7j8mH7a31QkRijcW6CPVmVz91vL2bCziNNGpHHXOSO1kqNIjFG4tyBrdhTw23dX8uHKbAZ2TeSpq8Zz4tDUoMsSkSagcG8BcgrK+PP7q3l+7mbat23NL88cxpXHDqBtGw3BiMQqhXsMyyuuYPon63hizkYqqqqZfHQ/bjhliNaEEWkBFO4xKL+0gqc+3cj/frKe/NJKzhndk5tPG8qArolBlyYizUThHkP2FJfz5KcbeeLTDRSUVnLq8G7cctphjOipqY0iLY3CPQZs3VPCjE828PzcTIrLqzh9ZBo/OXmINqkWacEU7lFs0eY9PPnpBt5esh0Dzh7dk2tOGKiLkERE4R5tSiuqeG9ZFjM/28iizXtIateGy4/pz5TjB2iuuoh8ReEeJdbnFPLcl5m8PH8Lu4srGNA1kbvOHsH56X1Iaqd/RhH5OqVCBMsvreCdJdt5ef4W5m/aTZtWxmkj0rhkQj8mDuqiZXhFpEEK9whTWlHFR6tyeHPxVj5YkU1ZZTWDuyVx65nD+P7YXnRL1oYZIrJ/CvcIUFpRxb9X5/DusizeX7GDgtJKuia15aKj+nDe2F6M6dMRM/XSRSR8CveA5BaV86+V2by/Ygf/Xp1DUXkVKQlxnD6yO+eM7snEQV20QqOIHDSFezOpqnaWbc3jo1U5fLw6m0Wb91DtkJbcjnPG9OLMUd05ZlAXbZAhIo1C4d5E3J11OUX8Z/0uPl27k8/W7SKvpAIzOKJXCtefPIRTh3djVM8UnRgVkUancG8kFVXVrNiez7yNu5m3KZcvN+Sys7AcgJ4p8Xx7RBrHDenKcYO70iWpXcDVikisU7gfBHdny+4Slm7NY9HmPSzavIelW/IoqagCQmF+/JBUJgzozISBXejfpb1OiIpIs1K470d5ZTXrcgpZmZXPiu0FLN+Wz7JteewprgCgbetWjOiZzIVH9SG9fyeO7NuJnrpSVEQCpnCvUVpRxYadRazLKWRtdiFrsgtZnVXAhp1FVFY7AG3btGJoWhJnjurOqF4pjOqZwvAeydr0QkQiTosK97ySCrbsLmZzbjGbdhWTmVvMxl1FbNxZzLa8EjyU4ZhBn07tGZqWxKkj0hjWvQPDeyQzsGuipieKSFSImXAvKqsku6CM7Xkl7MgvJSuvjG17StieV8LWPaVs2V1MQWnl157TsX0c/bskMn5AZ/p3SWRgaiKDuyUxoGsi8XGtA/o/ERE5dFEd7v9amc09by8nO7+UovKqbzyekhBHz44J9EyJZ3z/TvTu1J5enRLo27k9fTq3JyUhLoCqRUSaXljhbmadgRnAt4GdwC/d/dkG2t4M/AJIAF4Bprl7WeOU+3Ud28cxokcy3zoslW4d4unWoR09UuLpXnNr3zaqf3aJiBy0cNPvEaAcSAPGAO+Y2WJ3z6jdyMxOB24FTga2Aa8Bd9cca3Rj+3bikUs6NcVLi4hEtf2eHTSzRGAScLu7F7r7HOBNYHI9zS8HZrh7hrvvBu4FrmjEekVEJAzhTP0YClS5++paxxYDI+tpO7Lmsdrt0sysy8GXKCIiByqccE8C8uocywM6hNF275+/0dbMrjGzeWY2LycnJ5xaRUQkTOGEeyFQd8flZKAgjLZ7//yNtu4+3d3T3T09NTU1nFpFRCRM4YT7aqCNmQ2pdWw0kFFP24yax2q32+Huuw6+RBEROVD7DXd3LwJeBe4xs0QzOxY4F5hVT/OngSlmNsLMOgH/BcxsxHpFRCQM4V5Lfy2heevZwHOE5q5nmFlfMys0s74A7v4e8ADwL2BTze3Oxi9bRET2Jax57u6eC5xXz/FMQidRax/7E/CnxihOREQOjvne1bKCLMIsh1Av/2B0JXTVbKSJ1LogcmtTXQdGdR2YWKyrn7vXOyMlIsL9UJjZPHdPD7qOuiK1Lojc2lTXgVFdB6al1aX1a0VEYpDCXUQkBsVCuE8PuoAGRGpdELm1qa4Do7oOTIuqK+rH3EVE5JtioecuIiJ1KNxFRGKQwl1EJAbFXLib2RAzKzWz2UHXAmBms81su5nlm9lqM7s6AmpqZ2YzzGyTmRWY2UIzOzPougDM7PqapaDLzGxmwLV0NrPXzKyo5r26OMh6amqKmPentgj/TEXcd7C2psqsWNxk9BFgbtBF1PJbYIq7l5nZMOAjM1vo7vMDrKkNsBk4EcgEzgJeNLPD3X1jgHVBaHvG+4DTCa1nFKSwtpdsZpH0/tQWyZ+pSPwO1tYkmRVTPXczuwjYA3wQcClfqdlycO8G4V5zGxRgSbh7kbvf5e4b3b3a3d8GNgDjgqyrprZX3f11INBlog9we8lmEynvT10R/pmKuO/gXk2ZWTET7maWDNwD/DToWuoys7+YWTGwEtgO/C3gkr7GzNIIbacYZI800hzI9pJSR6R9piLxO9jUmRUz4U5oM+4Z7r456ELqcvdrCW01eDyhtfHL9v2M5mNmccAzwFPuvjLoeiLIgWwvKbVE4mcqQr+DTZpZURHuZvaRmXkDtzlmNgY4FXgwkuqq3dbdq2p+te8NTIuEusysFaFNV8qB65uypgOpK0IcyPaSUqO5P1MHojm/g/vTHJkVFSdU3f1b+3rczG4C+gOZZgahXldrMxvh7kcGVVcD2tDE433h1GWhN2oGoZOFZ7l7RVPWFG5dEeSr7SXdfU3NsYa2lxSC+UwdpCb/DobhWzRxZkVFzz0M0wn9Y42puT0GvENoRkFgzKybmV1kZklm1trMTgd+CHwYZF01HgWGA2e7e0nQxexlZm3MLB5oTejDHm9mzd4JOcDtJZtNpLw/DYi4z1QEfwebPrPcPeZuwF3A7AioIxX4mNDZ8HxgKfCjCKirH6EZA6WEhh/23i6JgNru4v9mNOy93RVQLZ2B14EiQtP7Ltb7E12fqUj9Djbw79qomaWFw0REYlCsDMuIiEgtCncRkRikcBcRiUEKdxGRGKRwFxGJQQp3EZEYpHAXEYlBCncRkRj0/wEgFjgxXr3rVQAAAABJRU5ErkJggg==\n"
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plot_function(torch.sigmoid, title='Sigmoid', min=-4, max=4)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 812,
   "outputs": [],
   "source": [
    "def mnist_loss(predictions, targets):\n",
    "    predictions = predictions.sigmoid()\n",
    "    return torch.where(targets==1, 1-predictions, predictions).mean()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 813,
   "outputs": [
    {
     "data": {
      "text/plain": "[tensor([ 7, 14,  3,  0,  6]),\n tensor([ 1, 12, 10,  5,  8]),\n tensor([13,  9,  4,  2, 11])]"
     },
     "execution_count": 813,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "coll = range(15)\n",
    "dl = DataLoader(coll, batch_size=5, shuffle=True)\n",
    "list(dl)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 814,
   "outputs": [
    {
     "data": {
      "text/plain": "(#26) [(0, 'a'),(1, 'b'),(2, 'c'),(3, 'd'),(4, 'e'),(5, 'f'),(6, 'g'),(7, 'h'),(8, 'i'),(9, 'j')...]"
     },
     "execution_count": 814,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ds = L(enumerate(string.ascii_lowercase))\n",
    "ds"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 815,
   "outputs": [
    {
     "data": {
      "text/plain": "[(tensor([ 1, 10,  7,  9, 24, 17]), ('b', 'k', 'h', 'j', 'y', 'r')),\n (tensor([ 6, 12, 16, 15, 19,  2]), ('g', 'm', 'q', 'p', 't', 'c')),\n (tensor([ 0, 20,  5, 23,  3, 25]), ('a', 'u', 'f', 'x', 'd', 'z')),\n (tensor([ 4,  8, 21, 11, 13, 14]), ('e', 'i', 'v', 'l', 'n', 'o')),\n (tensor([18, 22]), ('s', 'w'))]"
     },
     "execution_count": 815,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dl = DataLoader(ds, batch_size=6, shuffle=True)\n",
    "list(dl)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Putting It All Together"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Re-initialize parameters:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 816,
   "outputs": [],
   "source": [
    "weights = init_params((28*28,1))\n",
    "bias = init_params(1)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "`DataLoader` created from a `Dataset`:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 817,
   "outputs": [
    {
     "data": {
      "text/plain": "(torch.Size([256, 784]), torch.Size([256, 1]))"
     },
     "execution_count": 817,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dl = DataLoader(dset, batch_size=256)\n",
    "xb,yb = first(dl)\n",
    "xb.shape,yb.shape"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Same for the validation set:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 818,
   "outputs": [],
   "source": [
    "valid_dl = DataLoader(valid_dset, batch_size=256)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Mini-batch of size 4 for testing:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 819,
   "outputs": [
    {
     "data": {
      "text/plain": "torch.Size([4, 784])"
     },
     "execution_count": 819,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "batch = train_x[:4]\n",
    "batch.shape"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 820,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([[8.0212],\n        [9.3134],\n        [2.0936],\n        [7.6557]], grad_fn=<AddBackward0>)"
     },
     "execution_count": 820,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "preds = linear1(batch)\n",
    "preds"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 821,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor(0.0277, grad_fn=<MeanBackward0>)"
     },
     "execution_count": 821,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "loss = mnist_loss(preds, train_y[:4])\n",
    "loss"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Calculate the gradients:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 822,
   "outputs": [
    {
     "data": {
      "text/plain": "(torch.Size([784, 1]), tensor(-0.0035), tensor([-0.0246]))"
     },
     "execution_count": 822,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "loss.backward()\n",
    "weights.grad.shape,weights.grad.mean(),bias.grad\n"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Everything in a function:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 823,
   "outputs": [],
   "source": [
    "def calc_grad(xb, yb, model):\n",
    "    preds = model(xb)\n",
    "    loss = mnist_loss(preds, yb)\n",
    "    loss.backward()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Test the function:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 824,
   "outputs": [
    {
     "data": {
      "text/plain": "(tensor(-0.0071), tensor([-0.0493]))"
     },
     "execution_count": 824,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "calc_grad(batch, train_y[:4], linear1)\n",
    "weights.grad.mean(),bias.grad"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "If we call it twice the gradients change:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 825,
   "outputs": [
    {
     "data": {
      "text/plain": "(tensor(-0.0106), tensor([-0.0739]))"
     },
     "execution_count": 825,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "calc_grad(batch, train_y[:4], linear1)\n",
    "weights.grad.mean(),bias.grad"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Reason being that the `loss.backward` *adds* the gradients of `loss` to any currently stored gradients.\n",
    "So we need to set the current gradients to 0 first:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 826,
   "outputs": [],
   "source": [
    "weights.grad.zero_()\n",
    "bias.grad.zero_();"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "> note: Inplace Operations: Methods in PyTorch whose names end in an underscore modify their objects _in place_. For instance, `bias.zero_()` sets all elements of the tensor `bias` to 0."
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 827,
   "outputs": [],
   "source": [
    "def train_epoch(model, lr, params):\n",
    "    for xb,yb in dl:\n",
    "        calc_grad(xb, yb, model)\n",
    "        for p in params:\n",
    "            p.data -= p.grad*lr\n",
    "            p.grad.zero_()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 828,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor([[True],\n        [True],\n        [True],\n        [True]])"
     },
     "execution_count": 828,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "(preds>0.0).float() == train_y[:4]"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Function to calculate validation accuracy:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 829,
   "outputs": [],
   "source": [
    "def batch_accuracy(xb, yb):\n",
    "    preds = xb.sigmoid()\n",
    "    correct = (preds>0.5) == yb\n",
    "    return correct.float().mean()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Check it works:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 830,
   "outputs": [
    {
     "data": {
      "text/plain": "tensor(1.)"
     },
     "execution_count": 830,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "batch_accuracy(linear1(batch), train_y[:4])"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Put the batches together:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 831,
   "outputs": [],
   "source": [
    "def validate_epoch(model):\n",
    "    accs = [batch_accuracy(model(xb), yb) for xb,yb in valid_dl]\n",
    "    return round(torch.stack(accs).mean().item(), 4)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 832,
   "outputs": [
    {
     "data": {
      "text/plain": "0.3944"
     },
     "execution_count": 832,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "validate_epoch(linear1)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "##### Starting point done.\n",
    "Train for one epoch to see if accuray improves:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 833,
   "outputs": [
    {
     "data": {
      "text/plain": "0.4917"
     },
     "execution_count": 833,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lr = 1.\n",
    "params = weights,bias\n",
    "train_epoch(linear1, lr, params)\n",
    "validate_epoch(linear1)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "Then a few more:"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 834,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0.4942 0.4986 0.7137 0.7324 0.8769 0.9233 0.9433 0.9511 0.9536 0.9594 0.9628 0.9623 0.9662 0.9682 0.9687 0.9697 0.9711 0.9726 0.9726 0.9731 "
     ]
    }
   ],
   "source": [
    "for i in range(20):\n",
    "    train_epoch(linear1, lr, params)\n",
    "    print(validate_epoch(linear1), end=' ')"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 852,
   "outputs": [],
   "source": [
    "class MyLearner():\n",
    "\n",
    "    def __init__(self, dls : DataLoaders, model, loss_func, opt_func, metrics, lr=1e-3):\n",
    "        self.dls = dls\n",
    "        self.model = model\n",
    "        self.loss_func = loss_func\n",
    "        self.opt_func = opt_func\n",
    "        self.metrics = metrics\n",
    "        self.lr = lr\n",
    "        self.opt = self.opt_func([p for p in self.model.parameters() if p.requires_grad], lr=self.lr)\n",
    "\n",
    "    def fit(self, n_epoch):\n",
    "        for i in range(n_epoch):\n",
    "            self.train_epoch()\n",
    "            print(f\"t_loss: {round(float(self.loss), 4)} acc: {self.validate_epoch()}\", end='\\n')\n",
    "\n",
    "    def train_epoch(self):\n",
    "        for xb,yb in self.dls.train:\n",
    "            self.calc_grad(xb, yb)\n",
    "            self.opt.step()\n",
    "            self.opt.zero_grad()\n",
    "\n",
    "    def calc_grad(self, xb, yb):\n",
    "        self.preds = self.model(xb)\n",
    "        self.loss_grad = self.loss_func(self.preds, yb)\n",
    "        self.loss = self.loss_grad.clone()\n",
    "        self.loss_grad.backward()\n",
    "\n",
    "\n",
    "    def validate_epoch(self):\n",
    "        accs = [self.metrics(self.model(xb), yb) for xb,yb in self.dls.valid]\n",
    "        return round(torch.stack(accs).mean().item(), 4)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 860,
   "outputs": [],
   "source": [
    "my_net = nn.Sequential(\n",
    "    nn.Linear(28*28,128),\n",
    "    nn.ReLU(),\n",
    "    nn.Linear(128,64),\n",
    "    nn.ReLU(),\n",
    "    nn.Linear(64,1),\n",
    ")"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 856,
   "outputs": [],
   "source": [
    "dls = DataLoaders(dl, valid_dl)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 861,
   "outputs": [],
   "source": [
    "my_learner = MyLearner(dls, my_net, loss_func=mnist_loss, opt_func=SGD, metrics=batch_accuracy)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 862,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "t_loss: 0.4746 acc: 0.5068\n",
      "t_loss: 0.474 acc: 0.5068\n",
      "t_loss: 0.4733 acc: 0.5068\n",
      "t_loss: 0.4726 acc: 0.5073\n",
      "t_loss: 0.4719 acc: 0.5078\n",
      "t_loss: 0.4711 acc: 0.5093\n",
      "t_loss: 0.4704 acc: 0.5151\n",
      "t_loss: 0.4696 acc: 0.5186\n",
      "t_loss: 0.4689 acc: 0.5249\n",
      "t_loss: 0.4681 acc: 0.5361\n",
      "t_loss: 0.4673 acc: 0.5542\n",
      "t_loss: 0.4664 acc: 0.5737\n",
      "t_loss: 0.4656 acc: 0.5923\n",
      "t_loss: 0.4647 acc: 0.6133\n",
      "t_loss: 0.4638 acc: 0.6353\n",
      "t_loss: 0.4629 acc: 0.6567\n",
      "t_loss: 0.462 acc: 0.6816\n",
      "t_loss: 0.461 acc: 0.7119\n",
      "t_loss: 0.4601 acc: 0.7373\n",
      "t_loss: 0.4591 acc: 0.7588\n",
      "t_loss: 0.4581 acc: 0.7725\n",
      "t_loss: 0.457 acc: 0.7964\n",
      "t_loss: 0.456 acc: 0.811\n",
      "t_loss: 0.4549 acc: 0.8281\n",
      "t_loss: 0.4538 acc: 0.8413\n",
      "t_loss: 0.4526 acc: 0.8564\n",
      "t_loss: 0.4515 acc: 0.8691\n",
      "t_loss: 0.4503 acc: 0.875\n",
      "t_loss: 0.449 acc: 0.8813\n",
      "t_loss: 0.4477 acc: 0.8867\n",
      "t_loss: 0.4464 acc: 0.8984\n",
      "t_loss: 0.445 acc: 0.9082\n",
      "t_loss: 0.4436 acc: 0.9155\n",
      "t_loss: 0.4421 acc: 0.9223\n",
      "t_loss: 0.4406 acc: 0.9267\n",
      "t_loss: 0.439 acc: 0.9287\n",
      "t_loss: 0.4374 acc: 0.9316\n",
      "t_loss: 0.4357 acc: 0.937\n",
      "t_loss: 0.4339 acc: 0.9424\n",
      "t_loss: 0.4321 acc: 0.9468\n"
     ]
    }
   ],
   "source": [
    "my_learner.fit(40)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "outputs": [],
   "source": [
    "plt.plot(L(my_learner.recorder.values).itemgot(2));"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Creating an Optimizer"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%% md\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "outputs": [],
   "source": [
    "linear_model = nn.Linear(28*28,1)"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "outputs": [],
   "source": [
    "w,b = linear_model.parameters()\n",
    "w.shape,b.shape\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  }
 ],
 "metadata": {
  "kernelspec": {
   "name": "python3",
   "language": "python",
   "display_name": "Python 3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}