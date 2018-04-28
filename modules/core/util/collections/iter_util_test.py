from modules.core.util.collections.iter_util import chunks


def test_chunks():
    iterable = (i for i in [2, 0, '', 3, 5])
    chunk_size = 2
    assert list(chunks(iterable, chunk_size)) == [(2, 0), ('', 3), (5, )]
