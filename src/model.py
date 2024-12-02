import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def get_similar_clusters(model, similarity_threshold, items_to_cluster):
    embeddings = model.encode(items_to_cluster)
    similarity_matrix = cosine_similarity(embeddings)
    n = similarity_matrix.shape[0]
    indices_clusters = []
    
    for i in range(n):
        max_similarity = 0
        best_cluster = None
        
        for indices_cluster in indices_clusters:
            indices_cluster_list = list(indices_cluster)
            min_similarity = similarity_matrix[i, indices_cluster_list].min()
            avg_similarity = similarity_matrix[i, indices_cluster_list].mean()
            
            if min_similarity >= similarity_threshold and avg_similarity > max_similarity:
                max_similarity = avg_similarity
                best_cluster = indices_cluster
        
        if best_cluster is not None:
            best_cluster.add(i)
        else:
            indices_clusters.append(set([i]))
    
    return [[items_to_cluster[i] for i in indices_cluster] for indices_cluster in indices_clusters]
    
def get_rare_to_frequent(clusters, frequencies):
    rare_to_frequent = {}
    
    for cluster in clusters:
        most_frequent_cluster_item = max(cluster, key=lambda cluster_item: frequencies.get(cluster_item, 0))
        
        for cluster_item in cluster:
            rare_to_frequent[cluster_item] = most_frequent_cluster_item
            
    return rare_to_frequent

def replace_rare_with_frequent(df, column, rare_to_frequent):
    df[column] = df[column].apply(lambda x: rare_to_frequent.get(x, x))
    return df

def get_features_coefs_by_class(model, features_names, top_n=10):
    coefs = pd.DataFrame(model.coef_, columns=features_names, index=model.classes_)
    features_coefs_by_class = {}
    
    for class_name in coefs.index:
        class_features_coefs = coefs.loc[class_name].sort_values(ascending=False).head(top_n)
        class_features_coefs_list = [(feature, coef) for feature, coef in class_features_coefs.items()]
        features_coefs_by_class[class_name] = class_features_coefs_list
    
    return features_coefs_by_class