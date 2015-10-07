from constance import config

from ralph import monkeys

__version__ = '3.0.0'

monkeys.patch_constance_fields()


__all__ = ['config']
