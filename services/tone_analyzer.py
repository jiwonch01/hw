import cv2
import numpy as np
from sklearn.cluster import KMeans

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_dominant_colors(image_bytes: bytes, k: int = 3):
    """
    주어진 이미지 바이트 데이터에서 KMeans 클러스터링을 사용하여
    가장 주요한(Dominant) 색상 k개를 추출하고, 간단한 톤을 추정합니다.
    """
    # 1. 이미지 디코딩
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("이미지를 디코딩할 수 없습니다.")
        
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 2. 처리 속도 향상을 위해 이미지 리사이즈
    img = cv2.resize(img, (150, 150), interpolation=cv2.INTER_AREA)
    pixels = img.reshape((-1, 3))
    
    # 3. KMeans 클러스터링
    clf = KMeans(n_clusters=k, n_init=10, random_state=42)
    clf.fit(pixels)
    
    colors = clf.cluster_centers_
    labels = clf.labels_
    
    # 4. 색상별 비율 기반으로 정렬
    counts = np.bincount(labels)
    sorted_idx = np.argsort(counts)[::-1]
    
    dominant_colors = colors[sorted_idx]
    hex_colors = [rgb_to_hex(c) for c in dominant_colors]
    
    # 5. 퍼스널 컬러 톤 분석 (단순화된 휴리스틱 알고리즘)
    # 실제로는 얼굴 피부톤과 색채학 데이터베이스가 필요하지만,
    # 여기서는 옷의 전반적인 색감 톤을 모의(Mock)로 분석합니다.
    avg_color = np.average(dominant_colors, axis=0, weights=counts[sorted_idx])
    hsv_avg = cv2.cvtColor(np.uint8([[avg_color]]), cv2.COLOR_RGB2HSV)[0][0]
    
    h, s, v = hsv_avg
    # OpenCV HSV 범위: H (0 ~ 179), S (0 ~ 255), V (0 ~ 255)
    # 단순화 로직: 명도(V)와 채도(S) 및 색상(H)를 기반으로 웜/쿨 분류
    if s > 128:  # 채도가 높을 때
        if (h < 30) or (h > 150):
            tone = "봄 웜톤 (Spring Warm)"
        else:
            tone = "겨울 쿨톤 (Winter Cool)"
    else:        # 채도가 낮거나 명도가 중요할 때
        if v > 150:
            if (h < 40) or (h > 140):
                tone = "봄 웜톤 소프트 (Spring Warm Soft)"
            else:
                tone = "여름 쿨톤 (Summer Cool)"
        else:
            if (h < 40) or (h > 140):
                tone = "가을 웜톤 (Autumn Warm)"
            else:
                tone = "여름 쿨톤 뮤트 (Summer Cool Mute)"
            
    return {
        "colors": hex_colors,
        "tone": tone
    }
