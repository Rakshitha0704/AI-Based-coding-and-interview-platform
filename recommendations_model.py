# recommendation_model.py
import numpy as np
from sklearn.neighbors import NearestNeighbors

# ---------------------------------------
# 1. Dummy topic vectors (you can expand)
# ---------------------------------------
topics = [
    "AI Basics",
    "Machine Learning",
    "Supervised Learning",
    "Unsupervised Learning",
    "Neural Networks",
    "Deep Learning",
    "Reinforcement Learning"
]

# Convert topics to simple numeric vectors (for demo)
# In real systems, use TF-IDF or embeddings.
vectors = np.array([
    [0, 0, 1],   # AI Basics
    [1, 0, 1],   # Machine Learning
    [1, 1, 0],   # Supervised
    [0, 1, 1],   # Unsupervised
    [2, 1, 0],   # Neural Networks
    [2, 2, 0],   # Deep Learning
    [0, 2, 1]    # Reinforcement Learning
], dtype=float)

# ---------------------------------------
# 2. Build KNN model
# ---------------------------------------
model = NearestNeighbors(n_neighbors=3, metric='euclidean')
model.fit(vectors)


# ---------------------------------------
# 3. Recommendation function
# ---------------------------------------
def recommend(topic_name):
    if topic_name not in topics:
        return ["Topic not found"]

    index = topics.index(topic_name)
    topic_vector = vectors[index].reshape(1, -1)

    distances, indices = model.kneighbors(topic_vector)

    recommended = []
    for idx in indices[0]:
        if topics[idx] != topic_name:
            recommended.append(topics[idx])

    return recommended
