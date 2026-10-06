# perm

一个只依赖 Python 标准库的排列组合枚举内核：字典序下一排列与上一排列、去重全排列、
去重组合、多重集的排列条数、字典序编号与反编号、按编号裁切，以及候选多重集校验。
元素只参与比较与相等判断，内核不读时钟、不起线程，也不做任何 I/O。

## 目录

- perm/core.py：内核实现（枚举、编号、反编号、裁切与校验）
- tests/test_core.py：内核的行为测试

## 怎么跑测试

在项目根目录执行：

    python3 -m unittest discover -s tests -v

Windows 上把 python3 换成你的解释器路径，例如：

    C:/Users/<你>/AppData/Local/Programs/Python/Python313/python.exe -m unittest discover -s tests -v
