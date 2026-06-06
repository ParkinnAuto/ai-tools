## Summary

Cross-modal image-text retrieval (ITR) involves retrieving relevant samples from one modality based on queries expressed in another modality. The approaches can be divided into three main categories: feature extraction, feature alignment, and system efficiency.

### Feature Extraction
- **Visual Semantic Embedding (VSE)**: Learning features independently.
  - Data-centric: Features are learned for all data pairs without distinction.
  - Weighted informative pairs to enhance discrimination; attention mechanisms to handle mismatched noise correspondences.
- **Cross-Attention (CA)**: Interactive feature learning through the transformer architecture.
  - Feeds image and text together into the transformer network, extracting cross-modal contextual features.
- **Self-adaptive (SA)**: Adaptive feature extraction based on self-modality interactions.

### Feature Alignment
The integration module is crucial for aligning images and texts. There are two main approaches:
1. **Global alignment-driven**: Aligns global features across modalities.
2. **Local alignment-involved**: Attempts explicit local alignment at a fine-grained level, known as local alignment-based methods.

### System Efficiency
Efficiency plays a critical role in ITR systems:
- Hash encoding to reduce computational cost by binarizing features.
- Model compression for lightweight running speed.
- Fast then slow approach: retrieves initially with coarse performance and then refines with high accuracy.

## Pre-training Paradigm

To advance research, insights into cross-modal pre-trained approaches are gained. This area has attracted significant attention recently due to the rich knowledge encoded by large-scale cross-modal models. Compared to conventional ITR, pre-trained ITR benefits from this implicit knowledge, leading to encouraging performance even without sophisticated retrieval engineering.

### Pre-training Paradigm Classification

1. **Model Architecture**: Different architectures used for feature extraction.
2. **Pre-training Task**: The type of tasks the model was trained on (e.g., image classification).
3. **Pre-training Data**: The data sets and sources from which the pre-trained models were trained.

In conclusion, this paper provides a comprehensive survey of ITR approaches, focusing on the cross-modal pre-training paradigm as well. It includes common benchmark datasets, evaluation metrics, accuracy comparisons among representative methods, and an overview of taxonomy construction based on feature extraction, alignment, and system efficiency perspectives. Additionally, some critical issues that were less studied are discussed at the end of the paper.

### Key Points
- **Feature Extraction**: Independent embedding, data-centric, weighted informative pairs.
- **Feature Alignment**: Global cross-modal alignment, local fine-grained alignment.
- **System Efficiency**: Hash encoding, model compression, fast then slow approach.
- **Pre-training Paradigm Classification**: Various architectures, tasks, and datasets.

### Important Terms
- ITR: Cross-modal image-text retrieval.
- VSE (Visual Semantic Embedding): Learning independent features for images and texts.
- CA (Cross-Attention): Interactive feature learning through transformer architecture.
- SA (Self-adaptive): Adaptive feature extraction based on self-modality interactions.
- Pre-training: Large-scale models trained first, then fine-tuned.

### Final Takeaway
This comprehensive survey covers the latest research trends in ITR from multiple perspectives. It includes detailed discussions of features, alignment methods, system efficiency, and an overview of pre-trained approaches for future advancements.