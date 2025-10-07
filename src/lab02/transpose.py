def transpose(mat: list[list[float | int]]) -> list[list]:
    if not mat:
        return []
    
    rows = len(mat)
    cols = len(mat[0])
    
    for row in mat:
        if len(row) != cols:
            raise ValueError
    
    result = []
    
    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(mat[i][j])
        result.append(new_row)
    
    return result

print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
print(transpose([[1, 2], [3]]))