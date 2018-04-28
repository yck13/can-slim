from modules.core.util.collections.list_util import set_difference

def test_set_difference():
    left = [1,2,3]
    right = [1,2]
    assert [3] == set_difference(left, right)
    assert [] == set_difference(right, left)
