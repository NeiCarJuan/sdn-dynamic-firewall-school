def extract_features(event_counter):
    """
    Giả lập trích xuất hành vi mạng
    """
    features = {
        "ping_rate": event_counter,
        "burstiness": event_counter / 2,
        "dst_variance": 1
    }
    return features

