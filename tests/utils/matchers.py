
from aiohttp import FormData


class AssertableFormData(FormData):

  def __eq__(self, __o: object) -> bool:
    target_fields = [(t[0]['name'], t[2]) for t in __o._fields]
    target_fields = dict(target_fields)
    for field in self._fields:
      key = field[0]['name']
      if key in target_fields:
        if field[2] == target_fields[key]:
          continue
      return False
    return True

