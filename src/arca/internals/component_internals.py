import importlib
import inspect
import logging
import pkgutil
import re
import weakref
from collections import namedtuple
from functools import lru_cache, wraps
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Sequence, \
    Union

from arca import component

log = logging.getLogger(__name__)


class ComponentOutput(NamedTuple):
    name: str
    type_hint: Any
    description: str = ""


class ComponentInput(NamedTuple):
    name: str
    var_name: str
    type_hint: Any
    description: str = ""


class ComponentMetadata:
    def __init__(
            self,
            *,
            name: str,
            param_names: Optional[Dict]=None,
            output_name: Union[None, List[str], str]=None,
            unpack_output: Optional[Sequence]=None,
    ):
        self._name = name
        self._param_names = param_names if param_names else {}
        self._output_name = [output_name] if isinstance(output_name, str) else output_name
        self._obj_call = None
        self._unpack_output = unpack_output

    @property
    def name(self) -> str:
        return self._name

    @property
    def func_name(self) -> str:
        if not self._obj_call:
            return ""
        return self._obj_call.__name__

    @property
    def input_list(self) -> Optional[List[ComponentInput]]:
        if not self._obj_call:
            return None

        re_param = re.compile(
            "^\s*:param\s+(?P<type>\w+\s+)?(?P<param>\w+)\s*:\s*(?P<doc>.*)\s*$",
            re.IGNORECASE | re.MULTILINE
        )
        all_doc = inspect.getdoc(self._obj_call)
        if all_doc:
            docs = re_param.findall(inspect.getdoc(self._obj_call))
        else:
            docs = []
        param_doc = {name_param: doc_param for _, name_param, doc_param in docs}

        all_input = []
        for var_name, param in inspect.signature(self._obj_call).parameters.items():
            name = self._param_names.get(var_name, var_name)
            all_input.append(
                ComponentInput(
                    name=name,
                    var_name=var_name,
                    type_hint=param.annotation,
                    description=param_doc.get(var_name, ""),
                )
            )
        return all_input

    @property
    def output(self) -> Union[None, ComponentOutput, List[ComponentOutput]]:
        if not self._obj_call:
            return None

        re_return = re.compile(
            "^\s*:return(?P<type>\s+\w+)?\s*:\s*(?P<doc>.*)\s*$",
            re.IGNORECASE | re.MULTILINE
        )
        all_doc = inspect.getdoc(self._obj_call)
        if all_doc:
            docs = re_return.search(all_doc)
            docs = docs.groups()[1] if docs else ""
        else:
            docs = ""

        params = inspect.signature(self._obj_call)
        out_type = params.return_annotation
        if not self._unpack_output:
            return ComponentOutput(name="output", type_hint=out_type)

        result_output = []
        for cmp_name in self._unpack_output:
            cmp_type = Any
            if isinstance(cmp_name, (list, tuple)):
                cmp_name, cmp_type = cmp_name
            result_output.append(
                ComponentOutput(name=cmp_name, type_hint=cmp_type, description=docs)
            )
        return result_output

    @property
    def description(self) -> str:
        if not self._obj_call:
            return ""
        return inspect.getdoc(self._obj_call)

    def setup(self, obj_call: Callable):
        pass

    def teardown(self, obj_call: Callable):
        pass

    def __repr__(self) -> str:
        func_name = None
        if self._obj_call:
            func_name = self._obj_call.__name__
        return (
            f"(Name: {self._name},"
            f" Parameters name: {self._param_names}," 
            f" Output name: {self._output_name}," 
            f" Wrapped Function: {func_name})"
        )

    def __call__(self, obj_call: Optional[Callable] = None) -> Callable:
        if obj_call:
            self._obj_call = obj_call
        else:
            obj_call = self._obj_call
        @wraps(obj_call)
        def wrapped_function(*args, **kwargs):
            self.setup(obj_call)
            return_value = obj_call(*args, **kwargs)
            self.teardown(obj_call)
            return return_value
        wrapped_function.__arca_mark__ = weakref.ref(self)
        return wrapped_function


def is_component(obj_call: Callable) -> bool:
    return get_component(obj_call) is not None


def get_component(obj_call: Callable) -> Optional[ComponentMetadata]:
    weak_mark = getattr(obj_call, "__arca_mark__", None)
    if weak_mark is None:
        return None
    return weak_mark()


@lru_cache(maxsize=1)
def get_all_components() -> Dict:
    all_func = {}
    CmpInfo = namedtuple("CmpInfo", ("metadata", "function"))
    for module_info in pkgutil.iter_modules(component.__path__):
        module_import = importlib.import_module(
            f"{component.__package__}.{module_info.name}"
        )
        for name, ref in inspect.getmembers(module_import, is_component):
            all_func[name] = CmpInfo(metadata=ref.__arca_mark__(), function=ref)
    log.debug(f"All components loaded: {all_func.keys()}")
    return all_func


