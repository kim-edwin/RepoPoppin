import keras
from keras import layers
from keras import ops
import tensorflow as tf
import pymysql
import numpy as np
import pandas as pd
import sys

# 사용자 정의 클래스 정의
class RecommenderNet(keras.Model):
    def __init__(self, num_users, num_news, embedding_size, **kwargs):
        super().__init__(**kwargs)
        self.num_users = num_users
        self.num_news = num_news
        self.embedding_size = embedding_size
        self.user_embedding = layers.Embedding(
            num_users,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.user_bias = layers.Embedding(num_users, 1)
        self.news_embedding = layers.Embedding(
            num_news,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.news_bias = layers.Embedding(num_news, 1)

    def call(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        user_bias = self.user_bias(inputs[:, 0])
        news_vector = self.news_embedding(inputs[:, 1])
        news_bias = self.news_bias(inputs[:, 1])
        dot_user_news = ops.tensordot(user_vector, news_vector, 2)
        # Add all the components (including bias)
        x = dot_user_news + user_bias + news_bias
        # The sigmoid activation forces the rating to between 0 and 1
        return ops.nn.sigmoid(x)

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "num_users": self.num_users,
                "num_news": self.num_news,
                "embedding_size": self.embedding_size,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)
