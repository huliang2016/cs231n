import numpy as np


def softmax_loss_naive(W, X, y, reg):
    """Softmax loss function, naive implementation (with loops)

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

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_classes = W.shape[1]
    num_train = X.shape[0]

    for i in range(num_train):

        # loss
        scores = X[i].dot(W)
        # shift values for 'scores' for numeric reasons (over-flow cautious)
        scores -= scores.max()
        scores_expsum = np.sum(np.exp(scores))
        cor_ex = np.exp(scores[y[i]])
        loss += - np.log( cor_ex / scores_expsum)

        # grad
        # for correct class
        dW[:, y[i]] += (-1) * (scores_expsum - cor_ex) / scores_expsum * X[i]
        for j in range(num_classes):
            # pass correct class gradient
            if j == y[i]:
                continue
            # for incorrect classes
            dW[:, j] += np.exp(scores[j]) / scores_expsum * X[i]

    loss /= num_train
    loss += reg * np.sum(W * W)
    dW /= num_train
    dW += 2 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """Softmax loss function, vectorized version.

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
    scores = X.dot(W)
    # shift values for 'scores' for numeric reasons (over-flow cautious)
    scores -= scores.max()
    scores = np.exp(scores)
    scores_sum = np.sum(scores, axis=1)
    correct = scores[range(num_train), y]

    loss = correct / scores_sum
    loss = -np.sum(np.log(loss)) / num_train + reg * np.sum(W * W)

    # grad
    s = np.divide(scores, scores_sum.reshape(num_train, 1))
    s[range(num_train), y] = - (scores_sum - correct) / scores_sum
    dW = X.T.dot(s)
    dW /= num_train
    dW += 2 * reg * W
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    return loss, dW
