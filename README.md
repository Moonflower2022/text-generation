# text-generation

A collection of text generation algorithms trained on different text sources like movie scripts, plays, etc.

## text sources (in /texts)

* `peter_pan.txt`: <https://www.gutenberg.org/files/16/16-h/16-h.htm#chap17>
* `shakespeare.txt`: <https://www.gutenberg.org/ebooks/100>
* `bee_movie.txt`: <https://courses.cs.washington.edu/courses/cse163/20wi/files/lectures/L04/bee-movie.txt>

## generation algorithms

* [LSTM (Long Short-term Memory)](https://en.wikipedia.org/wiki/Long_short-term_memory) and [GRU (Gated Recurrent Unit)](https://en.wikipedia.org/wiki/Gated_recurrent_unit): `train_rnn.ipynb`
* : `train_lstm_or_gru.ipynb`
* [Markov Chain](https://en.wikipedia.org/wiki/Markov_chain): `markov_chain.py`
