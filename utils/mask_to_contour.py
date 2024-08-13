"""
배경 -> 0, 영역 -> 1
1. bfs 탐색으로 가장 많은 픽셀을 가진 영역 찾기 -> list(set(좌표 집합)) -> argmax(len)
2. 1번에서 구한 영역 외에 모두 0으로 변환
3. 가장 많은 픽셀을 가진 영역의 대표 좌표를 기준 윤곽선 찾기
- 윤곽선 -> 꼭짓점 좌표(0, 0)부터 시작하여 bfs
- bfs 탐색 중 1을 만나면 좌표 저장
"""

import numpy as np
from collections import deque


def contour(masks):
    mask = masks[0]
    h, w = mask.shape
    mask = mask.astype(np.uint8)

    dy, dx = [0, 1, 0, -1], [1, 0, -1, 0]
    visited = np.zeros((h, w), dtype=bool)
    area = []  # set of area

    for i in range(h):
        for j in range(w):
            if mask[i, j] == 1 and not visited[i, j]:
                q = deque([(i, j)])
                visited[i, j] = True
                area.append(set([(i, j)]))
                while q:
                    y, x = q.popleft()
                    for k in range(4):
                        ny, nx = y + dy[k], x + dx[k]
                        if (
                            0 <= ny < h
                            and 0 <= nx < w
                            and mask[ny, nx] == 1
                            and not visited[ny, nx]
                        ):
                            q.append((ny, nx))
                            visited[ny, nx] = True
                            area[-1].add((ny, nx))

    max_area = max(area, key=len)

    for i in range(h):
        for j in range(w):
            if (i, j) not in max_area:
                mask[i, j] = 0

    start = None
    for i, j in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
        if mask[i, j] == 0:
            start = [i, j]
            break

    if start is None:
        raise ValueError("No start point")

    q = deque([start])
    visited = np.zeros((h, w), dtype=bool)
    contour = []
    while q:
        y, x = q.popleft()
        for k in range(4):
            ny, nx = y + dy[k], x + dx[k]
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                visited[ny, nx] = True
                if mask[ny, nx] == 0:
                    q.append((ny, nx))
                else:
                    contour.append([ny, nx])

    return contour
