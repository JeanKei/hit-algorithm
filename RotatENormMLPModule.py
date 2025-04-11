import torch
from torch import nn
from pykeen.models import RotatE
from torch.nn import functional as F

class RotatENormMLP(RotatE):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Улучшения:
        self.entity_norm = nn.LayerNorm(self.embedding_dim)  # Применяем LayerNorm вместо BatchNorm
        self.relation_norm = nn.LayerNorm(self.embedding_dim)  # Применяем LayerNorm вместо BatchNorm
        
        self.entity_dropout = nn.Dropout(0.3)  # Увеличиваем Dropout для сущностей
        self.relation_dropout = nn.Dropout(0.1)  # Уменьшаем Dropout для отношений
        
        # Многослойные перцептроны для улучшения эмбеддингов
        self.entity_mlp = nn.Sequential(
            nn.Linear(self.embedding_dim, self.embedding_dim * 2),
            nn.ReLU(),
            nn.Linear(self.embedding_dim * 2, self.embedding_dim)
        )

        self.relation_mlp = nn.Sequential(
            nn.Linear(self.embedding_dim, self.embedding_dim * 2),
            nn.ReLU(),
            nn.Linear(self.embedding_dim * 2, self.embedding_dim)
        )

    def forward(self, *inputs, **kwargs):
        # Вытаскиваем эмбеддинги сущностей и отношений из базовой модели RotatE
        entity_embeddings, relation_embeddings = super().forward(*inputs, **kwargs)
        
        # Применяем нормализацию
        entity_embeddings = self.entity_norm(entity_embeddings)
        relation_embeddings = self.relation_norm(relation_embeddings)
        
        # Применяем Dropout для регуляризации
        entity_embeddings = self.entity_dropout(entity_embeddings)
        relation_embeddings = self.relation_dropout(relation_embeddings)
        
        # Применяем MLP для улучшения эмбеддингов
        entity_embeddings = self.entity_mlp(entity_embeddings)
        relation_embeddings = self.relation_mlp(relation_embeddings)
        
        return entity_embeddings, relation_embeddings
