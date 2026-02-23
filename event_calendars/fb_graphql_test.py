import pytest

from event_calendars.fb_graphql import parse_day_time_sentence
from datetime import datetime


from pprint import pprint

from event_calendars.spiders.respect_cyclists import convert_facebook_event_to_spider_event
from event_calendars.fb_graphql import extract_prefetched_events_from_inline_json, Event, internal_bbox_content_Type


schedule_server_js_example: internal_bbox_content_Type = {
    "require": [
        [
            "ScheduledServerJS",
            "handle",
            None,
            [
                {
                    "__bbox": {
                        "define": [
                            ["cr:14085", ["FDSShareExternalFilled16PNGIcon.react"], {"__rc": ["FDSShareExternalFilled16PNGIcon.react", None]}, -1],
                            ["cr:13865", ["FDSCheckmarkCircleFilled16PNGIcon.react"], {"__rc": ["FDSCheckmarkCircleFilled16PNGIcon.react", None]}, -1],
                            ["cr:13974", ["FDSCheckmarkFilled16PNGIcon.react"], {"__rc": ["FDSCheckmarkFilled16PNGIcon.react", None]}, -1],
                            ["cr:14249", ["FDSStarOutline16PNGIcon.react"], {"__rc": ["FDSStarOutline16PNGIcon.react", None]}, -1],
                            ["cr:14694", ["FDSChevronDownFilled12PNGIcon.react"], {"__rc": ["FDSChevronDownFilled12PNGIcon.react", None]}, -1],
                            ["cr:15697", ["FDSStarFilled16PNGIcon.react"], {"__rc": ["FDSStarFilled16PNGIcon.react", None]}, -1],
                            ["cr:13971", ["FDSCheckmarkCircleOutline16PNGIcon.react"], {"__rc": ["FDSCheckmarkCircleOutline16PNGIcon.react", None]}, -1],
                        ],
                        "require": [
                            ["EventCometGoToHorizonEventButton_renderer$normalization.graphql"],
                            ["EventCometGoToHorizonEventButton.react"],
                            ["PublicEventCometRSVPButtonRenderer_rsvpStyleRenderer$normalization.graphql"],
                            ["PublicEventCometRSVPButtonRenderer.react"],
                            ["PublicEventCometRSVPButtonGroupRenderer_rsvpStyleRenderer$normalization.graphql"],
                            ["PublicEventCometRSVPButtonGroupRenderer.react"],
                            [
                                "emptyFunction",
                                "thatReturns",
                                ["RequireDeferredReference"],
                                [
                                    [
                                        {"__dr": "EventCometGoToHorizonEventButton_renderer$normalization.graphql"},
                                        {"__dr": "EventCometGoToHorizonEventButton.react"},
                                        {"__dr": "PublicEventCometRSVPButtonRenderer_rsvpStyleRenderer$normalization.graphql"},
                                        {"__dr": "PublicEventCometRSVPButtonRenderer.react"},
                                        {"__dr": "PublicEventCometRSVPButtonGroupRenderer_rsvpStyleRenderer$normalization.graphql"},
                                        {"__dr": "PublicEventCometRSVPButtonGroupRenderer.react"},
                                    ]
                                ],
                            ],
                            [
                                "RelayPrefetchedStreamCache",
                                "next",
                                [],
                                [
                                    "adp_CometGroupEventsRootQueryRelayPreloader_6998b335d225d6617895497",
                                    {
                                        "__bbox": {
                                            "complete": True,
                                            "result": {
                                                "data": {
                                                    "group": {
                                                        "if_viewer_can_create_event": None,
                                                        "if_viewer_can_post": None,
                                                        "id": "562446623836569",
                                                        "cover_photo": {
                                                            "photo": {
                                                                "focus": {"x": 0.5, "y": 0.33},
                                                                "small_image": {
                                                                    "width": 431,
                                                                    "height": 296,
                                                                    "uri": "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-6/447836681_10163590193479046_4282936966233871889_n.jpg?stp=dst-jpg_s526x296_tt6&amp;_nc_cat=108&amp;ccb=1-7&amp;_nc_sid=25d718&amp;_nc_ohc=0u6dmoZGZ8oQ7kNvwEeOXbj&amp;_nc_oc=AdnADQrF7nLQqcYQtOlUb6JltFfG0T60nQN_CpQ9C0RdbBQvw16aFsoKZk1owmXbPAo&amp;_nc_zt=23&amp;_nc_ht=scontent-yyz1-1.xx&amp;_nc_gid=23wW1S8DFUcQ5qwtC6lV_g&amp;oh=00_AfsH2BJ_bGr-3j8hsUSNMGW6KgOdjByLT4nb1nIk3t2t1g&amp;oe=699E7BA9",
                                                                },
                                                                "id": "10163590193484046",
                                                            }
                                                        },
                                                        "upcoming_events": {"edges": [], "page_info": {"end_cursor": None, "has_next_page": False}},
                                                        "past_events": {
                                                            "edges": [
                                                                {
                                                                    "node": {
                                                                        "id": "789092220770764",
                                                                        "rsvp_button_renderer": {
                                                                            "__typename": "PublicRsvpStyleRenderer",
                                                                            "event": {
                                                                                "id": "789092220770764",
                                                                                "connection_style": "INTERESTED",
                                                                                "can_viewer_join": False,
                                                                                "can_viewer_watch": False,
                                                                                "can_viewer_unwatch": False,
                                                                                "viewer_watch_status": "UNWATCHED",
                                                                                "if_viewer_can_see_going_button": None,
                                                                                "event_connection_data_privacy_scope": None,
                                                                                "privacy_scope_for_toast": None,
                                                                                "can_join_group_chat": False,
                                                                                "created_for_group": {"id": "562446623836569"},
                                                                                "chat": None,
                                                                            },
                                                                            "__module_operation_EventCometUniversalRSVPButton_event": {
                                                                                "__dr": "PublicEventCometRSVPButtonRenderer_rsvpStyleRenderer$normalization.graphql"
                                                                            },
                                                                            "__module_component_EventCometUniversalRSVPButton_event": {"__dr": "PublicEventCometRSVPButtonRenderer.react"},
                                                                        },
                                                                        "rsvp_button_group_renderer": {
                                                                            "__typename": "PublicRsvpStyleRenderer",
                                                                            "event": {
                                                                                "should_show_recurring_event_rsvp_button": False,
                                                                                "id": "789092220770764",
                                                                                "can_join_group_chat": False,
                                                                                "can_viewer_watch": False,
                                                                                "chat": None,
                                                                                "connection_style": "INTERESTED",
                                                                                "created_for_group": {"id": "562446623836569"},
                                                                                "if_viewer_can_see_going_button": None,
                                                                                "is_past": True,
                                                                                "viewer_watch_status": "UNWATCHED",
                                                                                "can_viewer_unwatch": False,
                                                                                "viewer_watch_all_status_for_recurring_events": None,
                                                                                "event_connection_data_privacy_scope": None,
                                                                            },
                                                                            "__module_operation_EventCometUniversalRSVPButtonGroup_event": {
                                                                                "__dr": "PublicEventCometRSVPButtonGroupRenderer_rsvpStyleRenderer$normalization.graphql"
                                                                            },
                                                                            "__module_component_EventCometUniversalRSVPButtonGroup_event": {"__dr": "PublicEventCometRSVPButtonGroupRenderer.react"},
                                                                        },
                                                                        "privacy_scope_for_toast": None,
                                                                        "rsvp_style": "PUBLIC_RSVP_STYLE",
                                                                        "should_show_recurring_event_rsvp_button": False,
                                                                        "viewer_guest_status": "UNKNOWN",
                                                                        "viewer_watch_status": "UNWATCHED",
                                                                        "should_show_horizon_rsvp_warning": False,
                                                                        "event_kind": "PUBLIC_TYPE",
                                                                        "can_viewer_invite": False,
                                                                        "can_page_viewer_invite_as_user": False,
                                                                        "can_profile_plus_viewer_invite_as_user": False,
                                                                        "can_profile_plus_viewer_invite_followers": False,
                                                                        "acting_account_name": None,
                                                                        "acting_account_id": "0",
                                                                        "if_workplace_event": None,
                                                                        "eventUrl": "https://www.facebook.com/events/789092220770764/",
                                                                        "can_boost_event_renderer": None,
                                                                        "can_viewer_see_rsvp_button": False,
                                                                        "can_viewer_share": True,
                                                                        "has_header_action_menu_items": False,
                                                                        "is_event_draft": False,
                                                                        "profile_plus_admin_id_if_self": None,
                                                                        "profile_plus_admin_name_if_self": None,
                                                                        "if_viewer_can_publish_draft_event": None,
                                                                        "parent_if_exists_or_self": {"id": "789092220770764"},
                                                                        "event_for_edit_flow": {"if_viewer_can_edit": None, "id": "789092220770764"},
                                                                        "is_eligible_for_poe_view_as_visitor_button": False,
                                                                        "is_past": True,
                                                                        "chat": None,
                                                                        "go_to_horizon_event_button_renderer": {
                                                                            "event": None,
                                                                            "__module_operation_useEventCometGetPermalinkActionButtons_event_go_to_horizon_event_button_renderer": {
                                                                                "__dr": "EventCometGoToHorizonEventButton_renderer$normalization.graphql"
                                                                            },
                                                                            "__module_component_useEventCometGetPermalinkActionButtons_event_go_to_horizon_event_button_renderer": {
                                                                                "__dr": "EventCometGoToHorizonEventButton.react"
                                                                            },
                                                                        },
                                                                        "name": "Ghost Bike Ride For Jean Louis",
                                                                        "is_canceled": False,
                                                                        "day_time_sentence": "Sat, Nov 1, 2025",
                                                                        "event_creator": {
                                                                            "__typename": "User",
                                                                            "__isEntity": "User",
                                                                            "url": None,
                                                                            "profile_picture": {
                                                                                "uri": "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-1/622434588_10166750358904046_3204157736143041933_n.jpg?stp=c350.0.900.900a_cp0_dst-jpg_s48x48_tt6&amp;_nc_cat=106&amp;ccb=1-7&amp;_nc_sid=1d2534&amp;_nc_ohc=RaJBjkE3sUEQ7kNvwGIAaXS&amp;_nc_oc=Admmosc2BxO2SwfKcifPgJsVaafU5A5a2uN8OM4tW0absSvuOhNmzbkWw09hwyDZtIc&amp;_nc_zt=24&amp;_nc_ht=scontent-yyz1-1.xx&amp;_nc_gid=23wW1S8DFUcQ5qwtC6lV_g&amp;oh=00_AftRLgo3iDp71kaby3cH3ylhl3dIDgbPwdok2tQGMhBBIg&amp;oe=699E7747"
                                                                            },
                                                                            "name": "Joey Schwartz",
                                                                            "id": "634499045",
                                                                        },
                                                                        "shared_in_group_by": {
                                                                            "__typename": "User",
                                                                            "__isEntity": "User",
                                                                            "url": None,
                                                                            "profile_picture": {
                                                                                "uri": "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-1/628021068_10162157697430766_6643701476472674239_n.jpg?stp=cp0_dst-jpg_s48x48_tt6&amp;_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=1d2534&amp;_nc_ohc=6ov1n3QsncAQ7kNvwEXvMU6&amp;_nc_oc=Adkp41itfow1h0fb0Dvi7E7uibQLQ8wZJyGOxuBBufmB2J7y2FlzuSHJN65zE3A6G6s&amp;_nc_zt=24&amp;_nc_ht=scontent-yyz1-1.xx&amp;_nc_gid=23wW1S8DFUcQ5qwtC6lV_g&amp;oh=00_AftacvVpKrH-It9Q6hVjC7Pu-arfr5oCNKp5F2mZl2K-aQ&amp;oe=699E8DBA"
                                                                            },
                                                                            "name": "Geoffrey Bercarich",
                                                                            "id": "503020765",
                                                                        },
                                                                        "cover_photo": {
                                                                            "photo": {
                                                                                "focus": {"x": 0.5, "y": 0.33},
                                                                                "small_image": {
                                                                                    "width": 296,
                                                                                    "height": 296,
                                                                                    "uri": "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-6/571255611_10166243255269046_4325153680977749030_n.jpg?stp=dst-jpg_s526x296_tt6&amp;_nc_cat=111&amp;ccb=1-7&amp;_nc_sid=7e0d18&amp;_nc_ohc=7pzTyafhuREQ7kNvwEgJ5rC&amp;_nc_oc=AdmaSttgOuwZQYze1goUw2U9BfuFsyr6Z3HCKCY-49toQ7m4g7i4DhnkPLxFPBmjdws&amp;_nc_zt=23&amp;_nc_ht=scontent-yyz1-1.xx&amp;_nc_gid=23wW1S8DFUcQ5qwtC6lV_g&amp;oh=00_AftCvQGv6bETMAcywG-jvohdmyRDz3G3jzCKK40nLNrQqQ&amp;oe=699EA04B",
                                                                                },
                                                                                "id": "10166243255259046",
                                                                            }
                                                                        },
                                                                        "url": "https://www.facebook.com/events/789092220770764/",
                                                                        "__typename": "Event",
                                                                    },
                                                                    "cursor": "AQHSGM6CK9fAE0_uMkuNoTn7pwh7AmETb8pP60shDRUeY83LYS00IXQpEjfGVg7-rkt1S_vDCq8UhRbwp9X41Psifg",
                                                                },
                                                                {
                                                                    "node": {
                                                                        "id": "2533827373664092",
                                                                        "rsvp_button_renderer": {
                                                                            "__typename": "PublicRsvpStyleRenderer",
                                                                            "event": {
                                                                                "id": "2533827373664092",
                                                                                "connection_style": "INTERESTED",
                                                                                "can_viewer_join": False,
                                                                                "can_viewer_watch": False,
                                                                                "can_viewer_unwatch": False,
                                                                                "viewer_watch_status": "UNWATCHED",
                                                                                "if_viewer_can_see_going_button": None,
                                                                                "event_connection_data_privacy_scope": None,
                                                                                "privacy_scope_for_toast": None,
                                                                                "can_join_group_chat": False,
                                                                                "created_for_group": {"id": "2246288900"},
                                                                                "chat": None,
                                                                            },
                                                                            "__module_operation_EventCometUniversalRSVPButton_event": {
                                                                                "__dr": "PublicEventCometRSVPButtonRenderer_rsvpStyleRenderer$normalization.graphql"
                                                                            },
                                                                            "__module_component_EventCometUniversalRSVPButton_event": {"__dr": "PublicEventCometRSVPButtonRenderer.react"},
                                                                        },
                                                                        "rsvp_button_group_renderer": {
                                                                            "__typename": "PublicRsvpStyleRenderer",
                                                                            "event": {
                                                                                "should_show_recurring_event_rsvp_button": False,
                                                                                "id": "2533827373664092",
                                                                                "can_join_group_chat": False,
                                                                                "can_viewer_watch": False,
                                                                                "chat": None,
                                                                                "connection_style": "INTERESTED",
                                                                                "created_for_group": {"id": "2246288900"},
                                                                                "if_viewer_can_see_going_button": None,
                                                                                "is_past": True,
                                                                                "viewer_watch_status": "UNWATCHED",
                                                                                "can_viewer_unwatch": False,
                                                                                "viewer_watch_all_status_for_recurring_events": None,
                                                                                "event_connection_data_privacy_scope": None,
                                                                            },
                                                                            "__module_operation_EventCometUniversalRSVPButtonGroup_event": {
                                                                                "__dr": "PublicEventCometRSVPButtonGroupRenderer_rsvpStyleRenderer$normalization.graphql"
                                                                            },
                                                                            "__module_component_EventCometUniversalRSVPButtonGroup_event": {"__dr": "PublicEventCometRSVPButtonGroupRenderer.react"},
                                                                        },
                                                                        "privacy_scope_for_toast": None,
                                                                        "rsvp_style": "PUBLIC_RSVP_STYLE",
                                                                        "should_show_recurring_event_rsvp_button": False,
                                                                        "viewer_guest_status": "UNKNOWN",
                                                                        "viewer_watch_status": "UNWATCHED",
                                                                        "should_show_horizon_rsvp_warning": False,
                                                                        "event_kind": "PUBLIC_TYPE",
                                                                        "can_viewer_invite": False,
                                                                        "can_page_viewer_invite_as_user": False,
                                                                        "can_profile_plus_viewer_invite_as_user": False,
                                                                        "can_profile_plus_viewer_invite_followers": False,
                                                                        "acting_account_name": None,
                                                                        "acting_account_id": "0",
                                                                        "if_workplace_event": None,
                                                                        "eventUrl": "https://www.facebook.com/events/2533827373664092/",
                                                                        "can_boost_event_renderer": None,
                                                                        "can_viewer_see_rsvp_button": False,
                                                                        "can_viewer_share": True,
                                                                        "has_header_action_menu_items": False,
                                                                        "is_event_draft": False,
                                                                        "profile_plus_admin_id_if_self": None,
                                                                        "profile_plus_admin_name_if_self": None,
                                                                        "if_viewer_can_publish_draft_event": None,
                                                                        "parent_if_exists_or_self": {"id": "2533827373664092"},
                                                                        "event_for_edit_flow": {"if_viewer_can_edit": None, "id": "2533827373664092"},
                                                                        "is_eligible_for_poe_view_as_visitor_button": False,
                                                                        "is_past": True,
                                                                        "chat": None,
                                                                        "go_to_horizon_event_button_renderer": {
                                                                            "event": None,
                                                                            "__module_operation_useEventCometGetPermalinkActionButtons_event_go_to_horizon_event_button_renderer": {
                                                                                "__dr": "EventCometGoToHorizonEventButton_renderer$normalization.graphql"
                                                                            },
                                                                            "__module_component_useEventCometGetPermalinkActionButtons_event_go_to_horizon_event_button_renderer": {
                                                                                "__dr": "EventCometGoToHorizonEventButton.react"
                                                                            },
                                                                        },
                                                                        "name": "Critical Mask Halloween Bike Ride ",
                                                                        "is_canceled": False,
                                                                        "day_time_sentence": "Fri, Oct 31, 2025",
                                                                        "event_creator": {
                                                                            "__typename": "User",
                                                                            "__isEntity": "User",
                                                                            "url": None,
                                                                            "profile_picture": {
                                                                                "uri": "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-1/628021068_10162157697430766_6643701476472674239_n.jpg?stp=cp0_dst-jpg_s48x48_tt6&amp;_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=1d2534&amp;_nc_ohc=6ov1n3QsncAQ7kNvwEXvMU6&amp;_nc_oc=Adkp41itfow1h0fb0Dvi7E7uibQLQ8wZJyGOxuBBufmB2J7y2FlzuSHJN65zE3A6G6s&amp;_nc_zt=24&amp;_nc_ht=scontent-yyz1-1.xx&amp;_nc_gid=23wW1S8DFUcQ5qwtC6lV_g&amp;oh=00_AftacvVpKrH-It9Q6hVjC7Pu-arfr5oCNKp5F2mZl2K-aQ&amp;oe=699E8DBA"
                                                                            },
                                                                            "name": "Geoffrey Bercarich",
                                                                            "id": "503020765",
                                                                        },
                                                                        "shared_in_group_by": {
                                                                            "__typename": "User",
                                                                            "__isEntity": "User",
                                                                            "url": None,
                                                                            "profile_picture": {
                                                                                "uri": "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-1/628021068_10162157697430766_6643701476472674239_n.jpg?stp=cp0_dst-jpg_s48x48_tt6&amp;_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=1d2534&amp;_nc_ohc=6ov1n3QsncAQ7kNvwEXvMU6&amp;_nc_oc=Adkp41itfow1h0fb0Dvi7E7uibQLQ8wZJyGOxuBBufmB2J7y2FlzuSHJN65zE3A6G6s&amp;_nc_zt=24&amp;_nc_ht=scontent-yyz1-1.xx&amp;_nc_gid=23wW1S8DFUcQ5qwtC6lV_g&amp;oh=00_AftacvVpKrH-It9Q6hVjC7Pu-arfr5oCNKp5F2mZl2K-aQ&amp;oe=699E8DBA"
                                                                            },
                                                                            "name": "Geoffrey Bercarich",
                                                                            "id": "503020765",
                                                                        },
                                                                        "cover_photo": None,
                                                                        "url": "https://www.facebook.com/events/2533827373664092/",
                                                                        "__typename": "Event",
                                                                    },
                                                                    "cursor": "AQHSau_TzadY5AdfHJFgWjq23XbIXeIyBpOTXGW5h0kNzBDuG1pdEUzOssIyZt_XLEax2tqBvC6Zq_GS7Tv5-9mYiQ",
                                                                },
                                                                {
                                                                    "node": {
                                                                        "id": "783985534010634",
                                                                        "rsvp_button_renderer": {
                                                                            "__typename": "PublicRsvpStyleRenderer",
                                                                            "event": {
                                                                                "id": "783985534010634",
                                                                                "connection_style": "INTERESTED",
                                                                                "can_viewer_join": False,
                                                                                "can_viewer_watch": False,
                                                                                "can_viewer_unwatch": False,
                                                                                "viewer_watch_status": "UNWATCHED",
                                                                                "if_viewer_can_see_going_button": None,
                                                                                "event_connection_data_privacy_scope": None,
                                                                                "privacy_scope_for_toast": None,
                                                                                "can_join_group_chat": False,
                                                                                "created_for_group": {"id": "562446623836569"},
                                                                                "chat": None,
                                                                            },
                                                                            "__module_operation_EventCometUniversalRSVPButton_event": {
                                                                                "__dr": "PublicEventCometRSVPButtonRenderer_rsvpStyleRenderer$normalization.graphql"
                                                                            },
                                                                            "__module_component_EventCometUniversalRSVPButton_event": {"__dr": "PublicEventCometRSVPButtonRenderer.react"},
                                                                        },
                                                                        "rsvp_button_group_renderer": {
                                                                            "__typename": "PublicRsvpStyleRenderer",
                                                                            "event": {
                                                                                "should_show_recurring_event_rsvp_button": False,
                                                                                "id": "783985534010634",
                                                                                "can_join_group_chat": False,
                                                                                "can_viewer_watch": False,
                                                                                "chat": None,
                                                                                "connection_style": "INTERESTED",
                                                                                "created_for_group": {"id": "562446623836569"},
                                                                                "if_viewer_can_see_going_button": None,
                                                                                "is_past": True,
                                                                                "viewer_watch_status": "UNWATCHED",
                                                                                "can_viewer_unwatch": False,
                                                                                "viewer_watch_all_status_for_recurring_events": None,
                                                                                "event_connection_data_privacy_scope": None,
                                                                            },
                                                                            "__module_operation_EventCometUniversalRSVPButtonGroup_event": {
                                                                                "__dr": "PublicEventCometRSVPButtonGroupRenderer_rsvpStyleRenderer$normalization.graphql"
                                                                            },
                                                                            "__module_component_EventCometUniversalRSVPButtonGroup_event": {"__dr": "PublicEventCometRSVPButtonGroupRenderer.react"},
                                                                        },
                                                                        "privacy_scope_for_toast": None,
                                                                        "rsvp_style": "PUBLIC_RSVP_STYLE",
                                                                        "should_show_recurring_event_rsvp_button": False,
                                                                        "viewer_guest_status": "UNKNOWN",
                                                                        "viewer_watch_status": "UNWATCHED",
                                                                        "should_show_horizon_rsvp_warning": False,
                                                                        "event_kind": "PUBLIC_TYPE",
                                                                        "can_viewer_invite": False,
                                                                        "can_page_viewer_invite_as_user": False,
                                                                        "can_profile_plus_viewer_invite_as_user": False,
                                                                        "can_profile_plus_viewer_invite_followers": False,
                                                                        "acting_account_name": None,
                                                                        "acting_account_id": "0",
                                                                        "if_workplace_event": None,
                                                                        "eventUrl": "https://www.facebook.com/events/783985534010634/",
                                                                        "can_boost_event_renderer": None,
                                                                        "can_viewer_see_rsvp_button": False,
                                                                        "can_viewer_share": True,
                                                                        "has_header_action_menu_items": False,
                                                                        "is_event_draft": False,
                                                                        "profile_plus_admin_id_if_self": None,
                                                                        "profile_plus_admin_name_if_self": None,
                                                                        "if_viewer_can_publish_draft_event": None,
                                                                        "parent_if_exists_or_self": {"id": "783985534010634"},
                                                                        "event_for_edit_flow": {"if_viewer_can_edit": None, "id": "783985534010634"},
                                                                        "is_eligible_for_poe_view_as_visitor_button": False,
                                                                        "is_past": True,
                                                                        "chat": None,
                                                                        "go_to_horizon_event_button_renderer": {
                                                                            "event": None,
                                                                            "__module_operation_useEventCometGetPermalinkActionButtons_event_go_to_horizon_event_button_renderer": {
                                                                                "__dr": "EventCometGoToHorizonEventButton_renderer$normalization.graphql"
                                                                            },
                                                                            "__module_component_useEventCometGetPermalinkActionButtons_event_go_to_horizon_event_button_renderer": {
                                                                                "__dr": "EventCometGoToHorizonEventButton.react"
                                                                            },
                                                                        },
                                                                        "name": "Ghost Bike Ride For Dave: Oakville",
                                                                        "is_canceled": False,
                                                                        "day_time_sentence": "Sat, Oct 25, 2025",
                                                                        "event_creator": {
                                                                            "__typename": "User",
                                                                            "__isEntity": "User",
                                                                            "url": None,
                                                                            "profile_picture": {
                                                                                "uri": "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-1/622434588_10166750358904046_3204157736143041933_n.jpg?stp=c350.0.900.900a_cp0_dst-jpg_s48x48_tt6&amp;_nc_cat=106&amp;ccb=1-7&amp;_nc_sid=1d2534&amp;_nc_ohc=RaJBjkE3sUEQ7kNvwGIAaXS&amp;_nc_oc=Admmosc2BxO2SwfKcifPgJsVaafU5A5a2uN8OM4tW0absSvuOhNmzbkWw09hwyDZtIc&amp;_nc_zt=24&amp;_nc_ht=scontent-yyz1-1.xx&amp;_nc_gid=23wW1S8DFUcQ5qwtC6lV_g&amp;oh=00_AftRLgo3iDp71kaby3cH3ylhl3dIDgbPwdok2tQGMhBBIg&amp;oe=699E7747"
                                                                            },
                                                                            "name": "Joey Schwartz",
                                                                            "id": "634499045",
                                                                        },
                                                                        "shared_in_group_by": {
                                                                            "__typename": "User",
                                                                            "__isEntity": "User",
                                                                            "url": None,
                                                                            "profile_picture": {
                                                                                "uri": "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-1/628021068_10162157697430766_6643701476472674239_n.jpg?stp=cp0_dst-jpg_s48x48_tt6&amp;_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=1d2534&amp;_nc_ohc=6ov1n3QsncAQ7kNvwEXvMU6&amp;_nc_oc=Adkp41itfow1h0fb0Dvi7E7uibQLQ8wZJyGOxuBBufmB2J7y2FlzuSHJN65zE3A6G6s&amp;_nc_zt=24&amp;_nc_ht=scontent-yyz1-1.xx&amp;_nc_gid=23wW1S8DFUcQ5qwtC6lV_g&amp;oh=00_AftacvVpKrH-It9Q6hVjC7Pu-arfr5oCNKp5F2mZl2K-aQ&amp;oe=699E8DBA"
                                                                            },
                                                                            "name": "Geoffrey Bercarich",
                                                                            "id": "503020765",
                                                                        },
                                                                        "cover_photo": {
                                                                            "photo": {
                                                                                "focus": {"x": 0.5, "y": 0.33},
                                                                                "small_image": {
                                                                                    "width": 296,
                                                                                    "height": 296,
                                                                                    "uri": "https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-6/539269226_10165880514014046_7234917147762152664_n.jpg?stp=dst-jpg_s526x296_tt6&amp;_nc_cat=105&amp;ccb=1-7&amp;_nc_sid=7e0d18&amp;_nc_ohc=LX8v95QnJ1EQ7kNvwHP7rFh&amp;_nc_oc=Adlkvi_-LSq-iM4JwRSMLwyhXGu8v0F-Mb1l9-SN1jH6GUB1BaVWBFM97RxmWONIJAs&amp;_nc_zt=23&amp;_nc_ht=scontent-yyz1-1.xx&amp;_nc_gid=23wW1S8DFUcQ5qwtC6lV_g&amp;oh=00_AftbyE7bzXCiQpzdIXH82o6qzmMcsyT1YaqJOYl_J3eV7g&amp;oe=699E7BDB",
                                                                                },
                                                                                "id": "10165880514004046",
                                                                            }
                                                                        },
                                                                        "url": "https://www.facebook.com/events/783985534010634/",
                                                                        "__typename": "Event",
                                                                    },
                                                                    "cursor": "AQHSbubz0cezfWeq_4gaTDHmy_TJx9-IdYI_1nSJZOHU2JVUX3_TqFlFmX4dBGFsi-LWoaGFXBPDiUvdEoOSN-vwiA",
                                                                },
                                                            ],
                                                            "page_info": {
                                                                "end_cursor": "AQHSddO0N4ymZqhQf8mADDKSbJJp1A2CVGQxg-7NHTYKgMZjCnDrM2ifYDJJuMLs3V2-C3Psgi7iDwascgq2h6YHJA",
                                                                "has_next_page": True,
                                                            },
                                                        },
                                                        "all_past_events": {"nodes": [{"id": "789092220770764"}]},
                                                    }
                                                },
                                                "errors": [
                                                    {
                                                        "message": "A server error field_exception occured. Check server logs for details.",
                                                        "severity": "ERROR",
                                                        "mids": ["26e780294c3a4e19019e49c16108db7c"],
                                                        "debug_link": "https://www.meta.com/debug/?mid=26e780294c3a4e19019e49c16108db7c",
                                                        "path": ["group", "past_events", "edges", 0, "node", "acting_account_name"],
                                                    },
                                                    {
                                                        "message": "A server error field_exception occured. Check server logs for details.",
                                                        "severity": "ERROR",
                                                        "mids": ["26e780294c3a4e19019e49c16108db7c"],
                                                        "debug_link": "https://www.meta.com/debug/?mid=26e780294c3a4e19019e49c16108db7c",
                                                        "path": ["group", "past_events", "edges", 1, "node", "acting_account_name"],
                                                    },
                                                    {
                                                        "message": "A server error field_exception occured. Check server logs for details.",
                                                        "severity": "ERROR",
                                                        "mids": ["26e780294c3a4e19019e49c16108db7c"],
                                                        "debug_link": "https://www.meta.com/debug/?mid=26e780294c3a4e19019e49c16108db7c",
                                                        "path": ["group", "past_events", "edges", 2, "node", "acting_account_name"],
                                                    },
                                                ],
                                                "extensions": {"is_final": True},
                                            },
                                            "sequence_number": 0,
                                        }
                                    },
                                ],
                            ],
                            ["Bootloader", "markComponentsAsImmediate", [], [["CometPrivacySelectorDialog.react", "CometPrivacySelectorPickerContainer.react"]]],
                            [
                                "RequireDeferredReference",
                                "unblock",
                                [],
                                [
                                    [
                                        "EventCometGoToHorizonEventButton_renderer$normalization.graphql",
                                        "EventCometGoToHorizonEventButton.react",
                                        "PublicEventCometRSVPButtonRenderer_rsvpStyleRenderer$normalization.graphql",
                                        "PublicEventCometRSVPButtonRenderer.react",
                                        "PublicEventCometRSVPButtonGroupRenderer_rsvpStyleRenderer$normalization.graphql",
                                        "PublicEventCometRSVPButtonGroupRenderer.react",
                                        "FDSTooltipDeferredImpl.react",
                                    ],
                                    "sd",
                                ],
                            ],
                            [
                                "RequireDeferredReference",
                                "unblock",
                                [],
                                [
                                    [
                                        "EventCometGoToHorizonEventButton_renderer$normalization.graphql",
                                        "EventCometGoToHorizonEventButton.react",
                                        "PublicEventCometRSVPButtonRenderer_rsvpStyleRenderer$normalization.graphql",
                                        "PublicEventCometRSVPButtonRenderer.react",
                                        "PublicEventCometRSVPButtonGroupRenderer_rsvpStyleRenderer$normalization.graphql",
                                        "PublicEventCometRSVPButtonGroupRenderer.react",
                                        "FDSTooltipDeferredImpl.react",
                                    ],
                                    "css",
                                ],
                            ],
                            ["CometResourceScheduler", "registerHighPriHashes", None, [["W9npjVJ", "nxeN8W2", "Qs1dPyP", "Fr6AKJO", "GFAegrq", "4WPk4nL", "5lfgPIX", "YXJzSot", "UBazzGR"]]],
                        ],
                        "phd2_indexes": ":1888,1889,1553,1552,1886,1887,2395,1925,1417,2028,792,1885,2323",
                    }
                },
                {"__bbox": None},
                {"__bbox": None},
            ],
        ]
    ]
}


non_events_response: internal_bbox_content_Type = {
    "require": [
        [
            "ScheduledServerJS",
            "handle",
            None,
            [
                {
                    "__bbox": {
                        "define": [
                            ["cr:6943", ["EventListenerImplForCacheStorage"], {"__rc": ["EventListenerImplForCacheStorage", None]}, -1],
                            ["cr:3024", [], {"__rc": [None, None]}, -1],
                            ["cr:2046346", [], {"__rc": [None, None]}, -1],
                            ["cr:8906", ["goURIWWW"], {"__rc": ["goURIWWW", None]}, -1],
                            ["cr:8828", [], {"__rc": [None, None]}, -1],
                            ["cr:1094907", [], {"__rc": [None, None]}, -1],
                            ["cr:334", ["ghlTestUBTFacebook"], {"__rc": ["ghlTestUBTFacebook", None]}, -1],
                            ["cr:1543261", [], {"__rc": [None, None]}, -1],
                            ["cr:1402", ["CometNetworkStatusToast"], {"__rc": ["CometNetworkStatusToast", None]}, -1],
                            ["cr:2718", [], {"__rc": [None, None]}, -1],
                            ["cr:5090", [], {"__rc": [None, None]}, -1],
                            ["cr:9041", [], {"__rc": [None, None]}, -1],
                            ["cr:1201738", [], {"__rc": [None, None]}, -1],
                            ["cr:1332233", [], {"__rc": [None, None]}, -1],
                            ["cr:1345969", ["AccessibilityWebAssistiveTechTypedLoggerLite"], {"__rc": ["AccessibilityWebAssistiveTechTypedLoggerLite", None]}, -1],
                            ["cr:1516609", ["BDCometSignalCollectionTrigger"], {"__rc": ["BDCometSignalCollectionTrigger", None]}, -1],
                            ["cr:1634616", ["CometUserActivity"], {"__rc": ["CometUserActivity", None]}, -1],
                            ["MarauderConfig", [], {"app_version": "1.0.0.0 (1020050632)", "gk_enabled": False}, 31],
                            [
                                "CurrentEnvironment",
                                [],
                                {"facebookdotcom": True, "messengerdotcom": False, "workplacedotcom": False, "instagramdotcom": False, "workdotmetadotcom": False, "horizondotmetadotcom": False},
                                827,
                            ],
                            [
                                "RTISubscriptionManagerConfig",
                                [],
                                {"config": {}, "autobot": {}, "assimilator": {}, "unsubscribe_release": True, "bladerunner_www_sandbox": None, "is_intern": False},
                                1081,
                            ],
                            [
                                "MqttWebConfig",
                                [],
                                {
                                    "fbid": "0",
                                    "appID": 219994525426954,
                                    "endpoint": "wss://edge-chat.facebook.com/chat",
                                    "pollingEndpoint": "https://edge-chat.facebook.com/mqtt/pull",
                                    "subscribedTopics": [],
                                    "capabilities": 10,
                                    "clientCapabilities": 3,
                                    "chatVisibility": False,
                                    "hostNameOverride": "",
                                },
                                3790,
                            ],
                            [
                                "RequestStreamE2EClientSamplingConfig",
                                [],
                                {
                                    "sampleRate": 100000,
                                    "methodToSamplingMultiplier": {
                                        "RTCSessionMessage": 10000,
                                        "Presence": 0.01,
                                        "FBGQLS:VOD_TICKER_SUBSCRIBE": 0.01,
                                        "FBGQLS:STORIES_TRAY_SUBSCRIBE": 100,
                                        "Collabri": 0.1,
                                        "FBGQLS:WORK_AVAILABILITY_STATUS_FANOUT_SUBSCRIBE": 0.1,
                                        "FBGQLS:GROUP_UNSEEN_ACTIVITY_SUBSCRIBE": 0.1,
                                        "FBGQLS:GROUP_RESET_UNSEEN_ACTIVITY_SUBSCRIBE": 0.1,
                                        "FBGQLS:INTERN_CALENDAR_UPDATE_SUBSCRIBE": 0.1,
                                        "SKY:gizmo_manage": 10000,
                                        "FBGQLS:FEEDBACK_LIKE_SUBSCRIBE": 10,
                                        "FBGQLS:HUDDLE_USERS_REQUESTED_TO_SPEAK_COUNT_SUBSCRIBE": 1000,
                                    },
                                },
                                4501,
                            ],
                            ["MqttWebDeviceID", [], {"clientID": "e026d059-d343-405d-bd86-93ff37c30c25"}, 5003],
                            ["AdsManagerReadRegions", [], {"excluded_endpoints": ["/am_tabular"]}, 7950],
                            ["AsyncRequestConfig", [], {"retryOnNetworkError": "1", "useFetchStreamAjaxPipeTransport": True}, 328],
                            ["SessionNameConfig", [], {"seed": "0w2p"}, 757],
                            ["WebDevicePerfInfoData", [], {"needsFullUpdate": True, "needsPartialUpdate": False, "shouldLogResourcePerf": False}, 3977],
                            ["DGWWebConfig", [], {"appId": "2220391788200892", "appVersion": "0", "dgwVersion": "2", "endpoint": "", "fbId": "0", "authType": ""}, 5508],
                            ["DOMScannerConfig", [], {"scan_id": "", "delay": 0, "needs_scan": False}, 7201],
                            ["WebStorageMonsterLoggingURI", [], {"uri": "/ajax/webstorage/process_keys/?state=1"}, 3032],
                            ["UserTimezoneServerTimeData", [], {"timezone": None, "force_update": None, "server_time": None, "server_gmt_offset": None}, 5502],
                            [
                                "CometRouteActorToasterBlocklist",
                                [],
                                {
                                    "route_trace_policies": [
                                        "comet.jobs.composer",
                                        "comet.jobs.detailView",
                                        "comet.compat.XCometPageJobOpeningDetailViewController",
                                        "comet.offer.create",
                                        "comet.offers.offer_details",
                                        "comet.crisis.safety_check",
                                        "comet.crisis.home_page",
                                    ]
                                },
                                5542,
                            ],
                            ["cr:1088657", [], {"__rc": [None, None]}, -1],
                            ["GhlTennisKnobsConfig", [], {"ghlbox_log_validity_in_mins": 7200, "ghlbox_initialize_in_mins": 14400, "change_class_interval_in_mins": 1440}, 6687],
                            [
                                "BDSignalCollectionData",
                                [],
                                {
                                    "sc": '{"t":1659080345,"c":[[30000,838801],[30001,838801],[30002,838801],[30003,838801],[30004,838801],[30005,838801],[30006,573585],[30007,838801],[30008,838801],[30012,838801],[30013,838801],[30015,806033],[30018,806033],[30021,540823],[30022,540817],[30040,806033],[30093,806033],[30094,806033],[30095,806033],[30101,541591],[30102,541591],[30103,541591],[30104,541591],[30106,806039],[30107,806039],[38000,541427],[38001,806643]]}',
                                    "fds": 60,
                                    "fda": 60,
                                    "i": 60,
                                    "sbs": 1,
                                    "dbs": 100,
                                    "bbs": 100,
                                    "hbi": 60,
                                    "rt": 262144,
                                    "hbcbc": 2,
                                    "hbvbc": 0,
                                    "hbbi": 30,
                                    "sid": -1,
                                    "hbv": "2272154727875730566",
                                },
                                5239,
                            ],
                        ],
                        "require": [
                            ["ContextualConfig"],
                            ["BladeRunnerClient"],
                            ["CometToast.react"],
                            ["WebDevicePerfInfoLogging"],
                            ["CometPixelRatioUpdater"],
                            ["CometChromeDome"],
                            ["CometBrowserDimensionsLogger"],
                            ["FbtLogging"],
                            ["ClientConsistencyFalcoEvent"],
                            ["DGWRequestStreamClient"],
                            ["CometSuspenseFalcoEvent"],
                            ["IntlQtEventFalcoEvent"],
                            ["addCometProfileSwitchAnnotation"],
                            ["FDSAlertDialogImpl.react"],
                            ["CometGHLTestUBT"],
                            ["CometRootDeferred"],
                            ["CometFBUncaughtError.react"],
                            ["CometTopnavItemClickFalcoEvent"],
                            ["CometTopnavItemImpressionFalcoEvent"],
                            ["CometNotificationsStateChangeSubscription"],
                            ["CometToasterView_DO_NOT_USE.react"],
                            ["CometBatchNotificationsStateChangeSubscription"],
                            ["CometRelayEF"],
                            ["CometRouteActorToaster.react"],
                            ["CometOnBeforeUnloadDialog.react"],
                            ["ODS"],
                            [
                                "emptyFunction",
                                "thatReturns",
                                ["RequireDeferredReference"],
                                [
                                    [
                                        {"__dr": "ContextualConfig"},
                                        {"__dr": "BladeRunnerClient"},
                                        {"__dr": "CometToast.react"},
                                        {"__dr": "WebDevicePerfInfoLogging"},
                                        {"__dr": "CometPixelRatioUpdater"},
                                        {"__dr": "CometChromeDome"},
                                        {"__dr": "CometBrowserDimensionsLogger"},
                                        {"__dr": "FbtLogging"},
                                        {"__dr": "ClientConsistencyFalcoEvent"},
                                        {"__dr": "DGWRequestStreamClient"},
                                        {"__dr": "CometSuspenseFalcoEvent"},
                                        {"__dr": "IntlQtEventFalcoEvent"},
                                        {"__dr": "addCometProfileSwitchAnnotation"},
                                        {"__dr": "FDSAlertDialogImpl.react"},
                                        {"__dr": "CometGHLTestUBT"},
                                        {"__dr": "CometRootDeferred"},
                                        {"__dr": "CometFBUncaughtError.react"},
                                        {"__dr": "CometTopnavItemClickFalcoEvent"},
                                        {"__dr": "CometTopnavItemImpressionFalcoEvent"},
                                        {"__dr": "CometNotificationsStateChangeSubscription"},
                                        {"__dr": "CometToasterView_DO_NOT_USE.react"},
                                        {"__dr": "CometBatchNotificationsStateChangeSubscription"},
                                        {"__dr": "CometRelayEF"},
                                        {"__dr": "CometRouteActorToaster.react"},
                                        {"__dr": "CometOnBeforeUnloadDialog.react"},
                                        {"__dr": "ODS"},
                                    ]
                                ],
                            ],
                            [
                                "CometPlatformRootClient",
                                "setInitDeferredPayload",
                                [],
                                [
                                    {
                                        "sketchInfo": None,
                                        "userID": 0,
                                        "deferredCookies": {
                                            "_js_datr": {
                                                "value": "oOKsZ59RqeYhODbn4zmKOYBC",
                                                "expiration_for_js": 34560000000,
                                                "expiration_for_http": 1773943456,
                                                "path": "/",
                                                "domain": ".facebook.com",
                                                "secure": True,
                                                "http_only": True,
                                                "first_party_only": True,
                                                "add_js_prefix": True,
                                                "same_site": "None",
                                            }
                                        },
                                        "blLoggingCavalryFields": {"bl_sample_rate": 0, "hr_sample_rate": 0, "parent_lid": "7470595059743900427"},
                                    }
                                ],
                            ],
                            ["MqttLongPollingRunner"],
                            ["Chromedome"],
                            ["AcfToastImpressionFalcoEvent"],
                            ["json-bigint"],
                            ["Bootloader", "markComponentsAsImmediate", [], [["FDSProfileVideoSection.react"]]],
                            [
                                "RequireDeferredReference",
                                "unblock",
                                [],
                                [
                                    [
                                        "ContextualConfig",
                                        "BladeRunnerClient",
                                        "CometToast.react",
                                        "WebDevicePerfInfoLogging",
                                        "CometPixelRatioUpdater",
                                        "CometChromeDome",
                                        "CometBrowserDimensionsLogger",
                                        "FbtLogging",
                                        "ClientConsistencyFalcoEvent",
                                        "DGWRequestStreamClient",
                                        "CometSuspenseFalcoEvent",
                                        "IntlQtEventFalcoEvent",
                                        "addCometProfileSwitchAnnotation",
                                        "FDSAlertDialogImpl.react",
                                        "CometGHLTestUBT",
                                        "CometRootDeferred",
                                        "CometFBUncaughtError.react",
                                        "CometTopnavItemClickFalcoEvent",
                                        "CometTopnavItemImpressionFalcoEvent",
                                        "CometNotificationsStateChangeSubscription",
                                        "CometToasterView_DO_NOT_USE.react",
                                        "CometBatchNotificationsStateChangeSubscription",
                                        "CometRelayEF",
                                        "CometRouteActorToaster.react",
                                        "CometOnBeforeUnloadDialog.react",
                                        "ODS",
                                        "MqttLongPollingRunner",
                                        "Chromedome",
                                        "CometExceptionDialog.react",
                                        "AcfToastImpressionFalcoEvent",
                                        "json-bigint",
                                    ],
                                    "sd",
                                ],
                            ],
                            [
                                "RequireDeferredReference",
                                "unblock",
                                [],
                                [
                                    [
                                        "ContextualConfig",
                                        "BladeRunnerClient",
                                        "CometToast.react",
                                        "WebDevicePerfInfoLogging",
                                        "CometPixelRatioUpdater",
                                        "CometChromeDome",
                                        "CometBrowserDimensionsLogger",
                                        "FbtLogging",
                                        "ClientConsistencyFalcoEvent",
                                        "DGWRequestStreamClient",
                                        "CometSuspenseFalcoEvent",
                                        "IntlQtEventFalcoEvent",
                                        "addCometProfileSwitchAnnotation",
                                        "FDSAlertDialogImpl.react",
                                        "CometGHLTestUBT",
                                        "CometRootDeferred",
                                        "CometFBUncaughtError.react",
                                        "CometTopnavItemClickFalcoEvent",
                                        "CometTopnavItemImpressionFalcoEvent",
                                        "CometNotificationsStateChangeSubscription",
                                        "CometToasterView_DO_NOT_USE.react",
                                        "CometBatchNotificationsStateChangeSubscription",
                                        "CometRelayEF",
                                        "CometRouteActorToaster.react",
                                        "CometOnBeforeUnloadDialog.react",
                                        "ODS",
                                        "MqttLongPollingRunner",
                                        "Chromedome",
                                        "CometExceptionDialog.react",
                                        "AcfToastImpressionFalcoEvent",
                                        "json-bigint",
                                    ],
                                    "css",
                                ],
                            ],
                        ],
                    }
                },
                {"__bbox": {"require": [["qplTimingsServerJS", None, None, ["7470595059743900427", "tierThreeBeforeScheduler"]]]}},
                {"__bbox": {"require": [["qplTimingsServerJS", None, None, ["7470595059743900427", "tierThreeInsideScheduler"]]]}},
            ],
        ]
    ]
}


@pytest.mark.parametrize(
    "json_dict,expected",
    [
        (schedule_server_js_example, ['789092220770764', '2533827373664092', '783985534010634',]),
        (non_events_response, []),
    ],
)
def test_extract_events_from_json(json_dict: internal_bbox_content_Type, expected: list[str]) -> None:

    events = list(extract_prefetched_events_from_inline_json(json_dict))

    assert all([isinstance(e, Event) for e in events])

    p = list([e.id for e in events])

    assert p == expected


def test_convert_facebook_event_to_spider_event() -> None:
    facebook_events = list(extract_prefetched_events_from_inline_json(schedule_server_js_example))

    fb_event = facebook_events[0]

    pprint(fb_event)
    # make sure we're starting with the right event
    assert fb_event.id == '789092220770764'

    scraper_event = convert_facebook_event_to_spider_event(fb_event)
    assert scraper_event.summary == 'Ghost Bike Ride For Jean Louis - placeholder time'



@pytest.mark.parametrize("provided,expected", [
    ('Sat, Nov 1, 2025', datetime(2025, 11, 1, 0, 0))
])
def test_parse_day_time_sentence(provided: str, expected: datetime) -> None:
    assert parse_day_time_sentence(provided) == expected
