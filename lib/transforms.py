import torch


def batch_mm(matrix, matrix_batch):
    """
    https://github.com/pytorch/pytorch/issues/14489#issuecomment-607730242
    :param matrix: Sparse or dense matrix, size (m, n).
    :param matrix_batch: Batched dense matrices, size (b, n, k).
    :return: The batched matrix-matrix product, size (m, n) x (b, n, k) = (b, m, k).
    """
    batch_size = matrix_batch.shape[0]
    # Stack the vector batch into columns. (b, n, k) -> (n, b, k) -> (n, b*k)
    vectors = matrix_batch.transpose(0, 1).reshape(matrix.shape[1], -1)

    # A matrix-matrix product is a batched matrix-vector product of the columns.
    # And then reverse the reshaping. (m, n) x (n, b*k) = (m, b*k) -> (m, b, k) -> (b, m, k)
    return matrix.mm(vectors).reshape(matrix.shape[0], batch_size, -1).transpose(1, 0)


def aa2quat(rots, form='wxyz', unified_orient=True):
    """
    Convert angle-axis representation to wxyz quaternion and to the half plan (w >= 0)
    @param rots: angle-axis rotations, (*, 3)
    @param form: quaternion format, either 'wxyz' or 'xyzw'
    @param unified_orient: Use unified orientation for quaternion (quaternion is dual cover of SO3)
    :return:
    """
    angles = rots.norm(dim=-1, keepdim=True)
    norm = angles.clone()
    norm[norm < 1e-8] = 1
    axis = rots / norm
    quats = torch.empty(rots.shape[:-1] + (4,), device=rots.device, dtype=rots.dtype)
    angles = angles * 0.5
    if form == 'wxyz':
        quats[..., 0] = torch.cos(angles.squeeze(-1))
        quats[..., 1:] = torch.sin(angles) * axis
    elif form == 'xyzw':
        quats[..., :3] = torch.sin(angles) * axis
        quats[..., 3] = torch.cos(angles.squeeze(-1))

    if unified_orient:
        idx = quats[..., 0] < 0
        quats[idx, :] *= -1

    return quats


def quat2aa(quats):
    """
    Convert wxyz quaternions to angle-axis representation
    :param quats:
    :return:
    """
    # wxyz
    _cos = quats[..., 0]
    xyz = quats[..., 1:]
    _sin = xyz.norm(dim=-1)
    norm = _sin.clone()
    norm[norm < 1e-7] = 1
    axis = xyz / norm.unsqueeze(-1)
    angle = torch.atan2(_sin, _cos) * 2
    return axis * angle.unsqueeze(-1)


def quat2mat(quats: torch.Tensor):
    """
    Convert (w, x, y, z) quaternions to 3x3 rotation matrix
    :param quats: quaternions of shape (..., 4)
    :return:  rotation matrices of shape (..., 3, 3)
    """
    qw = quats[..., 0]
    qx = quats[..., 1]
    qy = quats[..., 2]
    qz = quats[..., 3]

    x2 = qx + qx
    y2 = qy + qy
    z2 = qz + qz
    xx = qx * x2
    yy = qy * y2
    wx = qw * x2
    xy = qx * y2
    yz = qy * z2
    wy = qw * y2
    xz = qx * z2
    zz = qz * z2
    wz = qw * z2

    m = torch.empty(quats.shape[:-1] + (3, 3), device=quats.device, dtype=quats.dtype)
    m[..., 0, 0] = 1.0 - (yy + zz)
    m[..., 0, 1] = xy - wz
    m[..., 0, 2] = xz + wy
    m[..., 1, 0] = xy + wz
    m[..., 1, 1] = 1.0 - (xx + zz)
    m[..., 1, 2] = yz - wx
    m[..., 2, 0] = xz - wy
    m[..., 2, 1] = yz + wx
    m[..., 2, 2] = 1.0 - (xx + yy)

    return m


def aa2mat(rots):
    """
    Convert angle-axis representation to rotation matrix
    :param rots: angle-axis representation
    :return:
    """
    quat = aa2quat(rots)
    mat = quat2mat(quat)
    return mat


def inv_affine(mat):
    """
    Calculate the inverse of any affine transformation
    """
    affine = torch.zeros((mat.shape[:2] + (1, 4)))
    affine[..., 3] = 1
    vert_mat = torch.cat((mat, affine), dim=2)
    vert_mat_inv = torch.inverse(vert_mat)
    return vert_mat_inv[..., :3, :]


def inv_rigid_affine(mat):
    """
    Calculate the inverse of a rigid affine transformation
    """
    res = mat.clone()
    res[..., :3] = mat[..., :3].transpose(-2, -1)
    res[..., 3] = -torch.matmul(res[..., :3], mat[..., 3].unsqueeze(-1)).squeeze(-1)
    return res
