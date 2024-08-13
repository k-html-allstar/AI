import numpy as np


def normalize_coordinates(coords):
    """좌표 정규화"""
    if not isinstance(coords, np.ndarray):
        coords = np.array(coords)

    # 인덱스 0값에 대해 내림차순으로 정렬하고, 인덱스 1값에 대해 오름차순으로 정렬
    sorted_arr = coords[np.lexsort((coords[:, 1], -coords[:, 0]))]

    base_coord = sorted_arr[0]
    normalized_coords = sorted_arr - base_coord
    # 인덱스 0값 전체 반전
    normalized_coords[:, 0] = -normalized_coords[:, 0]

    return normalized_coords


def change_to_map_scale(coords):
    """좌표를 지도 스케일로 변환"""
    if not isinstance(coords, np.ndarray):
        coords = np.array(coords)

    extra_normalization = 0.002
    max_val = np.max(np.abs(coords))
    coords = coords / max_val * extra_normalization

    return coords


def sorted_by_contour(coords):
    """좌표를 윤곽선을 따라 정렬"""
    if not isinstance(coords, np.ndarray):
        coords = np.array(coords)

    # 중심점 계산
    center = np.mean(coords, axis=0)

    # 각도를 기준으로 좌표 정렬
    angles = np.arctan2(coords[:, 1] - center[1], coords[:, 0] - center[0])
    sorted_indices = np.argsort(angles)
    sorted_coords = coords[sorted_indices]

    return sorted_coords
