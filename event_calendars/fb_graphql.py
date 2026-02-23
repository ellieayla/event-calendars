from abc import abstractmethod
from datetime import datetime, date
from typing import Any, Callable, Iterable, Literal, NamedTuple, TypeAlias, Self

from dataclasses import dataclass, fields
from typing import TypedDict, Protocol
from operator import attrgetter


class SupportedDeserializationFromDict(Protocol):
    @classmethod
    @abstractmethod
    def from_dict(cls, d) -> Self: ...  # type: ignore[no-untyped-def]


@dataclass(init=False)
class ModuleEntry():
    name: str
    data: list[Any]

    def __init__(self, json: list[Any]) -> None:
        self.name = json[0]
        self.data = json[1:]
        return None

class internal_bbox_content_Type(TypedDict, total=False):
    require: list[Any]
    define: list[Any]
    complete: bool | None
    result: dict[str, Any] | None
    label: str | None
    path: list[str] | None
    data: dict[str, Any] | None

internal__bbox_Type: TypeAlias = dict[Literal["__bbox"], internal_bbox_content_Type | None]


@dataclass
class BBox(SupportedDeserializationFromDict):
    """A structure with one key and a list of items, like {'require': [..., ...]}"""
    require: list[ModuleEntry]# = field(default_factory=list)
    define: list[ModuleEntry]# = field(default_factory=list)
    complete: bool | None = None
    result: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, d: internal_bbox_content_Type | None) -> Self:
        if d is None:
            # an empty __bbox
            return cls(
                require=[],
                define=[],
                complete=None,
                result=None,
            )

        return cls(
            require = list([ModuleEntry(_) for _ in d.get('require', [])]),
            define = list([ModuleEntry(_) for _ in d.get('define', [])]),
            complete = d.get('complete', None),
            result = d.get('result', None),
        )



@dataclass(init=False)
class BBoxContainer():
    bbox: BBox
    def __init__(self, data: internal__bbox_Type):
        self.bbox = BBox.from_dict(data['__bbox'])


@dataclass
class RelayPrefetchedStreamCache_Result():
    label: str | None
    path: list[str] | None
    data: dict[str, Any]
    errors: list[Any] | None
    extensions: dict[str, Any]

    @classmethod
    def from_bbox(cls, bbox: BBox) -> Self:
        assert bbox.result is not None
        return cls(
            label=bbox.result.get("label"),
            path=bbox.result.get("path"),
            data=bbox.result["data"],
            errors=bbox.result.get('errors'),
            extensions=bbox.result["extensions"],
        )

@dataclass
class RelayPrefetchedStreamCache_Complete_Result():
    data: Any
    errors: list[Any]
    extensions: dict[str, Any]

    @classmethod
    def from_bbox(cls, bbox: BBox) -> Self:
        assert bbox.complete
        assert bbox.result is not None
        return cls(
            data=bbox.result['data'],
            errors=bbox.result['errors'],
            extensions=bbox.result['extensions'],
        )


@dataclass
class RelayPrefetchedStreamCache():
    preload_id: str
    bbox: BBox

    @classmethod
    def from_module_data(cls, module_data: list[Any]) -> Self:
        assert len(module_data) == 3
        assert module_data[0] == 'next'
        assert module_data[1] == []

        (preload_id, bbox_data) = module_data[2]
        return cls(preload_id=preload_id, bbox=BBoxContainer(bbox_data).bbox)

    @property
    def graph_method_name(self) -> str:
        return self.preload_id.removeprefix("adp_").partition("RelayPreloader_")[0]


class ScheduledServerJS(NamedTuple):
    command: Literal["handle"]
    unused: None
    datas: list[internal__bbox_Type]


def handle_module(module: ModuleEntry) -> Iterable[BBox]:
    match module.name:
        case "ScheduledServerJS":
            if len(module.data) != 3:
                raise ValueError(f"Unexpected length of ScheduledServerJS (SSJS) arguments, expected 3, got {len(module.data)}")
            ssjs = ScheduledServerJS(command=module.data[0], unused=module.data[1], datas=module.data[2])

            if ssjs.command != 'handle':
                raise ValueError(f"Unexpected ScheduledServerJS (SSJS) command {ssjs.command}")
            if ssjs.unused is not None:
                raise Warning(f"Unexpected ScheduledServerJS module.data[1] value, expected None, got {ssjs.unused}")
            assert isinstance(ssjs.datas, list)

            for inner_data in ssjs.datas:
                if inner_data['__bbox'] is None:
                    continue
                yield BBoxContainer(inner_data).bbox

        case _:
            ...
            #warnings.warn(f"Unsupported module type {module.name=}")

@dataclass(repr=False)
class PageInfo():
    """Concrete type PageInfo from fb_graphql_types.json"""
    has_previous_page: bool = False
    has_next_page: bool = False

    end_cursor: str | None = None
    start_cursor: str | None = None
    delta_cursor: str | None = None

    is_defer_fulfilled: bool | None = None

    def __repr__(self) -> str:
        nodef_f_vals = (
            (f.name, attrgetter(f.name)(self))
            for f in fields(self)
            if attrgetter(f.name)(self) != f.default
        )

        nodef_f_repr = ", ".join(f"{name}={value}" for name, value in nodef_f_vals)
        return f"{self.__class__.__name__}({nodef_f_repr})"

class _WireEventActor(TypedDict):
    __typename: str
    id: str
    name: str


@dataclass()
class Actor(SupportedDeserializationFromDict):
    """Concrete type Actor from fb_graphql_types.json"""
    _typename: str
    id: str
    name: str

    @classmethod
    def from_dict(cls, d: _WireEventActor) -> Self:
        assert d["__typename"] == "User"
        return cls(
            _typename=d["__typename"],
            id=d["id"],
            name=d["name"],
        )


def parse_day_time_sentence(s: str) -> date:
    """Parsed a string like 'Sat, Nov 1, 2025' into a datetime.date"""
    return datetime.strptime(s, "%a, %b %d, %Y")

class _WireEventDict(TypedDict):
    """Concrete type Event from fb_graphql_types.json"""
    __typename: Literal["Event"]
    id: str
    name: str
    is_canceled: bool
    is_past: bool
    shared_in_group_by: _WireEventActor
    event_creator: _WireEventActor
    day_time_sentence: str
    url: str
    one_line_address: str
    event_description: dict[str, str]


@dataclass
class Event:
    """Concrete type Event from fb_graphql_types.json"""
    id: str
    name: str
    is_canceled: bool
    is_past: bool
    #shared_in_group_by: Actor | None
    event_creator: Actor | None
    start_date: date | None
    url: str

    one_line_address: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, d: _WireEventDict) -> Self:
        assert d.get('__typename', 'Event') == 'Event'  # default if reading typeless data

        try:
            description = d['event_description']['text']
        except KeyError:
            description = None

        return cls(
            id=str(d["id"]),
            name=d.get("name"),
            is_canceled=d.get("is_canceled"),
            is_past=d.get("is_past"),
            #shared_in_group_by=Actor.from_dict(d.get("shared_in_group_by")),
            event_creator=Actor.from_dict(d.get("event_creator")),
            start_date=parse_day_time_sentence(d.get("day_time_sentence")) if "day_time_sentence" in d else None,
            url=d.get("url"),
            one_line_address=d.get("one_line_address"),
            description=description,
        )


class EdgeCursor[T](TypedDict):
    cursor: str
    node: T


@dataclass(init=False)
class PagedEdges[T]():
    edges: list[T]
    page_info: PageInfo

    def __init__(self, edges: list[EdgeCursor[T]], page_info: dict[str, Any], deserialize_with: Callable[[Any], T]):
        self.page_info = PageInfo(**page_info)

        # Note: The parameterization of this type is incorrect.
        # mypy error: "type[T]" has no attribute "from_dict"  [attr-defined]
        #assert issubclass(deserialize_with_cls, SupportedDeserializationFromDict)
        self.edges = list([
            deserialize_with(edge_cursor['node'])
            for edge_cursor in edges
        ])


@dataclass
class GroupEventsGraphQLQueryResult():
    id: str
    past_events: PagedEdges[Event]
    upcoming_events: PagedEdges[Event]

    @classmethod
    def from_prefetch(cls, group_data: dict[str, Any]) -> Self:
        # there's a maximum of 3 prefetched events
        return cls(
            id=group_data['id'],
            past_events=PagedEdges(edges=group_data['past_events']['edges'], page_info=group_data['past_events']['page_info'], deserialize_with=Event.from_dict),
            upcoming_events=PagedEdges(edges=group_data['upcoming_events']['edges'], page_info=group_data['upcoming_events']['page_info'], deserialize_with=Event.from_dict),
        )


def extract_prefetched_events_from_inline_json(parsed_json: internal_bbox_content_Type) -> Iterable[Event]:
    # https://github.com/firsttris/plugin.video.sendtokodi/blob/891fa15b264f25d1f24f59d161ca1aa057ec69c9/lib/yt_dlp/extractor/facebook.py#L581
    # https://github.com/SSujitX/facebook-pages-scraper/blob/4c0a68893399a98275c3ada5b8af42de06a9c654/facebook_page_scraper/page_post_info.py#L62
    # https://github.com/c4ffe14e/phice/blob/c2cda1cf98b281871f269f74630b4bf60939c373/src/lib/api.py#L147
    # https://github.com/mautrix/meta/blob/3e8aa342fa0b9dc568825104dbeaa0df182331b3/pkg/messagix/js_module_parser.go#L289

    root = BBox.from_dict(parsed_json)
    for module in root.require:

        ssjs_module_boxes = handle_module(module)
        for ssjs_module_box in ssjs_module_boxes:

            for module in ssjs_module_box.require:
                if module.name == 'RelayPrefetchedStreamCache':
                    # only supported module right now
                    rpsc = RelayPrefetchedStreamCache.from_module_data(module.data)

                    # only known graph_method_name
                    if rpsc.graph_method_name == "CometGroupEventsRootQuery":
                        result = RelayPrefetchedStreamCache_Complete_Result.from_bbox(rpsc.bbox)

                        # there's a maximum of 3 prefetched events
                        group_result = GroupEventsGraphQLQueryResult.from_prefetch(result.data['group'])
                        # pprint(group_result, width=200)

                        for e in group_result.past_events.edges + group_result.upcoming_events.edges:
                            yield e

def extract_prefetched_objects_from_inline_json(parsed_json: internal_bbox_content_Type) -> Iterable[RelayPrefetchedStreamCache]:
    # https://github.com/firsttris/plugin.video.sendtokodi/blob/891fa15b264f25d1f24f59d161ca1aa057ec69c9/lib/yt_dlp/extractor/facebook.py#L581
    # https://github.com/SSujitX/facebook-pages-scraper/blob/4c0a68893399a98275c3ada5b8af42de06a9c654/facebook_page_scraper/page_post_info.py#L62
    # https://github.com/c4ffe14e/phice/blob/c2cda1cf98b281871f269f74630b4bf60939c373/src/lib/api.py#L147
    # https://github.com/mautrix/meta/blob/3e8aa342fa0b9dc568825104dbeaa0df182331b3/pkg/messagix/js_module_parser.go#L289

    root = BBox.from_dict(parsed_json)
    for module in root.require:

        ssjs_module_boxes = handle_module(module)
        for ssjs_module_box in ssjs_module_boxes:

            for module in ssjs_module_box.require:
                if module.name == 'RelayPrefetchedStreamCache':
                    # only supported module right now
                    rpsc = RelayPrefetchedStreamCache.from_module_data(module.data)

                    yield rpsc
