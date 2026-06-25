import numpy as np

from lumbar_mri.training.metrics import dice_score, iou_score, mean_dice


def test_dice_score_perfect_match():
    y_true = np.array([[0, 1], [1, 2]])
    y_pred = np.array([[0, 1], [1, 2]])

    assert dice_score(y_true, y_pred, class_id=1) == 1.0


def test_iou_score_perfect_match():
    y_true = np.array([[0, 1], [1, 2]])
    y_pred = np.array([[0, 1], [1, 2]])

    assert iou_score(y_true, y_pred, class_id=2) == 1.0


def test_mean_dice_with_classes():
    y_true = np.array([[0, 1], [1, 2]])
    y_pred = np.array([[0, 1], [1, 0]])

    value = mean_dice(y_true, y_pred, class_ids=[1, 2])

    assert 0.0 <= value <= 1.0
