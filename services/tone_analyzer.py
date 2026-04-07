import cv2
import numpy as np
from sklearn.cluster import KMeans
from rembg import remove

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_dominant_colors(image_bytes: bytes, k: int = 3):
    """
    KMeans 클러스터링을 사용하여 주요 색상을 추출하고, 톤과 팔레트를 추천합니다.
    rembg를 이용해 배경을 제거한 후 전경(주로 옷/사람)의 색상만 분석합니다.
    """
    # 1. 배경 제거 (rembg 적용: 머리카락 배경 등 날리고 옷, 피부 등 주요 객체만 분리)
    # 첫 실행 시 u2net.onnx 모델 가중치를 다운로드 받습니다.
    subject_bytes = remove(image_bytes)
    
    # 2. 이미지 디코딩 (알파 채널 포함)
    nparr = np.frombuffer(subject_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    
    if img is None:
        raise ValueError("이미지를 디코딩할 수 없습니다.")
        
    # 3. 투명 배경 제외 (Alpha > 0인 픽셀만 추출)
    if img.shape[2] == 4:
        alpha_mask = img[:, :, 3] > 0
        pixels = img[alpha_mask]
        pixels = pixels[:, :3] # BGR만 추출
    else:
        pixels = img.reshape((-1, 3))
    
    # BGR -> RGB 변환
    pixels = cv2.cvtColor(np.uint8([pixels]), cv2.COLOR_BGR2RGB)[0]
    
    # 분석 속도를 위해 픽셀 랜덤 샘플링 (10,000개)
    if len(pixels) > 10000:
        indices = np.random.choice(len(pixels), 10000, replace=False)
        sampled_pixels = pixels[indices]
    else:
        sampled_pixels = pixels
    
    # 4. KMeans 클러스터링
    clf = KMeans(n_clusters=k, n_init=10, random_state=42)
    clf.fit(sampled_pixels)
    
    colors = clf.cluster_centers_
    labels = clf.labels_
    
    # 비율순 정렬
    counts = np.bincount(labels)
    sorted_idx = np.argsort(counts)[::-1]
    
    dominant_colors = colors[sorted_idx]
    hex_colors = [rgb_to_hex(c) for c in dominant_colors]
    
    # 5. 퍼스널 컬러 톤 분석 및 추천 색조합 생성 (간이 휴리스틱)
    avg_color = np.average(dominant_colors, axis=0, weights=counts[sorted_idx])
    hsv_avg = cv2.cvtColor(np.uint8([[avg_color]]), cv2.COLOR_RGB2HSV)[0][0]
    
    h, s, v = hsv_avg
    
    palette = []
    if s > 128:
        if (h < 30) or (h > 150):
            tone = "봄 웜톤 (Spring Warm)"
            palette = ["#FFD1DC", "#FFB347", "#B2EBF2", "#FDFD96"] 
        else:
            tone = "겨울 쿨톤 (Winter Cool)"
            palette = ["#000080", "#800080", "#FF00FF", "#FFFFFF"]
    else:
        if v > 150:
            if (h < 40) or (h > 140):
                tone = "봄 웜톤 소프트 (Spring Warm Soft)"
                palette = ["#F5DEB3", "#FFDAB9", "#E6E6FA", "#FFF0F5"]
            else:
                tone = "여름 쿨톤 (Summer Cool)"
                palette = ["#E6E6FA", "#ADD8E6", "#FFB6C1", "#E0FFFF"]
        else:
            if (h < 40) or (h > 140):
                tone = "가을 웜톤 (Autumn Warm)"
                palette = ["#8B4513", "#D2691E", "#CD853F", "#556B2F"]
            else:
                tone = "여름 쿨톤 뮤트 (Summer Cool Mute)"
                palette = ["#778899", "#B0C4DE", "#D8BFD8", "#C0C0C0"]
            
    return {
        "colors": hex_colors,
        "tone": tone,
        "palette": palette
    }
