import sys
import timeit
from datetime import datetime
from enum import Enum
from typing import NamedTuple


class Direction(Enum):
    In = "In"


# 定义测试数据
dt = datetime.now()
raw_bytes = b"A1 B2 C3"
direction = Direction.In

# 1. 普通 tuple
TupleData = tuple[datetime, bytes, Direction]
tuple_obj = (dt, raw_bytes, direction)


# 2. NamedTuple
class NamedTupleData(NamedTuple):
    timestamp: datetime
    data: bytes
    direction: Direction


named_tuple_obj = NamedTupleData(dt, raw_bytes, direction)


# ==========================================
# 测试 1: 内存占用对比
# ==========================================
def test_memory():
    print("=== 1. 内存占用对比 ===")
    size_tuple = sys.getsizeof(tuple_obj)
    size_namedtuple = sys.getsizeof(named_tuple_obj)

    print(f"tuple 内存占用      : {size_tuple} bytes")
    print(f"NamedTuple 内存占用 : {size_namedtuple} bytes")
    print(f"内存结果判断       : {'完全一致' if size_tuple == size_namedtuple else '不同'}\n")


# ==========================================
# 测试 2: 创建速度对比 (实例化 1,000,000 次)
# ==========================================
def test_creation_speed():
    print("=== 2. 创建速度对比 (1,000,000 次) ===")

    tuple_time = timeit.timeit(
        stmt="(dt, raw_bytes, direction)",
        globals=globals(),
        number=1_000_000
    )

    named_tuple_time = timeit.timeit(
        stmt="NamedTupleData(dt, raw_bytes, direction)",
        globals=globals(),
        number=1_000_000
    )

    print(f"tuple 创建耗时      : {tuple_time:.4f} 秒")
    print(f"NamedTuple 创建耗时 : {named_tuple_time:.4f} 秒")
    print(f"创建耗时比 (NT / T) : {named_tuple_time / tuple_time:.2f} 倍\n")


# ==========================================
# 测试 3: 元素访问速度对比 (读取 10,000,000 次)
# ==========================================
def test_access_speed():
    print("=== 3. 访问速度对比 (10,000,000 次) ===")

    # tuple 按索引访问
    t_idx_time = timeit.timeit(
        stmt="x = tuple_obj[1]",
        globals=globals(),
        number=10_000_000
    )

    # NamedTuple 按索引访问
    nt_idx_time = timeit.timeit(
        stmt="x = named_tuple_obj[1]",
        globals=globals(),
        number=10_000_000
    )

    # NamedTuple 按属性名访问
    nt_attr_time = timeit.timeit(
        stmt="x = named_tuple_obj.data",
        globals=globals(),
        number=10_000_000
    )

    print(f"tuple [索引] 访问耗时          : {t_idx_time:.4f} 秒")
    print(f"NamedTuple [索引] 访问耗时     : {nt_idx_time:.4f} 秒")
    print(f"NamedTuple [.属性名] 访问耗时   : {nt_attr_time:.4f} 秒")
    print(f"属性名访问 vs 索引访问开销差距 : {nt_attr_time - nt_idx_time:.4f} 秒\n")


if __name__ == "__main__":
    test_memory()
    test_creation_speed()
    test_access_speed()