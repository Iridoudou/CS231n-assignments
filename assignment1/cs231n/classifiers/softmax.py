from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    num_classes = W.shape[1]
    num_train = X.shape[0]

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    for i in range(num_train):
        scores = np.dot(X[i], W)
        scores -= np.max(scores)
        correct_class_score = scores[y[i]]
        tmp_sum = np.sum(np.exp(scores))
        loss += -correct_class_score + np.log(tmp_sum)
        for j in range(num_classes):
            if j == y[i]:
                dW[:, j] += X[i]*(-1+(np.exp(scores[j]) / tmp_sum))
            else:
                dW[:, j] += X[i]*(np.exp(scores[j]) / tmp_sum)

    loss /= num_train
    loss += 0.5 * reg * np.sum(W * W)

    dW /= num_train
    dW += reg*W
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    num_classes = W.shape[1]
    num_train = X.shape[0]

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    # print(X.shape)
    # print(W.shape)

    scores = np.dot(X, W)
    # print(scores.shape)
    scores -= np.max(scores, axis=1, keepdims=True)
    # print(scores.shape)

    correct_class_scores = np.sum(scores[range(num_train), y])

    scores = np.exp(scores)
    tmp_sum = np.sum(scores, axis=1, keepdims=True)
    loss = -correct_class_scores+np.sum(np.log(tmp_sum))
    loss /= num_train
    loss += 0.5*reg*np.sum(W*W)

    prob = scores/tmp_sum
    prob[range(num_train), y] -= 1

    dW = np.dot(X.T, prob)
    dW /= num_train
    dW += reg*W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
