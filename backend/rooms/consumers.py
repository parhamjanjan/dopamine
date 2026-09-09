from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from .models import (
    RoomMembership,
    RoomChatMessage,
)
from .services import get_room_ranking


class StudyRoomConsumer(
    AsyncJsonWebsocketConsumer
):

    async def connect(self):

        self.room_id = (
            self.scope['url_route']['kwargs']
            ['room_id']
        )

        self.room_group_name = (
            f'study_room_{self.room_id}'
        )

        # =================================================
        # User
        # =================================================

        user = self.scope.get('user')

        if (
            not user
            or not user.is_authenticated
        ):
            await self.close(
                code=4001
            )
            return

        self.user_id = user.id
        self.username = user.username

        # =================================================
        # Ranking
        # =================================================

        self.ranking_period = 'today'

        # =================================================
        # Membership
        # =================================================

        is_member = (
            await self.check_membership(
                user.id,
                self.room_id
            )
        )

        if not is_member:

            await self.close(
                code=4003
            )
            return

        # =================================================
        # Join Channel Group
        # =================================================

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # =================================================
        # Notify Room Members
        # =================================================

        await self.channel_layer.group_send(

            self.room_group_name,

            {
                'type':
                    'room_member_joined',

                'user_id':
                    self.user_id,

                'username':
                    self.username,
            }
        )

        # =================================================
        # Initial Ranking
        # =================================================

        ranking = (
            await database_sync_to_async(
                get_room_ranking
            )(
                self.room_id,
                self.ranking_period
            )
        )

        await self.send_json({

            'type':
                'connection',

            'message':
                'با موفقیت به سالن مطالعه متصل شدید.',

            'room_id':
                self.room_id,

            'user_id':
                self.user_id,

            'username':
                self.username,

            'ranking':
                ranking,

            'period':
                self.ranking_period,
        })

    # =====================================================
    # Disconnect
    # =====================================================

    async def disconnect(
        self,
        close_code
    ):

        # -------------------------------------------------
        # Notify members that user left
        # -------------------------------------------------

        try:

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'room_member_left',

                    'user_id':
                        self.user_id,
                }
            )

        except Exception:

            pass

        # -------------------------------------------------
        # Leave group
        # -------------------------------------------------

        try:

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        except Exception:

            pass

    # =====================================================
    # Receive
    # =====================================================

    async def receive_json(
        self,
        content,
        **kwargs
    ):

        message_type = content.get(
            'type'
        )

        # =================================================
        # Ranking Ping
        # =================================================

        if message_type == 'ping':

            ranking = (
                await database_sync_to_async(
                    get_room_ranking
                )(
                    self.room_id,
                    self.ranking_period
                )
            )

            await self.send_json({

                'type':
                    'ranking_update',

                'ranking':
                    ranking,

                'period':
                    self.ranking_period,
            })

        # =================================================
        # Ranking Period
        # =================================================

        elif (
            message_type ==
            'ranking_period'
        ):

            period = content.get(
                'period',
                'today'
            )

            valid_periods = {
                'today',
                'yesterday',
                'week',
                'all',
            }

            if period not in valid_periods:
                return

            self.ranking_period = (
                period
            )

            ranking = (
                await database_sync_to_async(
                    get_room_ranking
                )(
                    self.room_id,
                    self.ranking_period
                )
            )

            await self.send_json({

                'type':
                    'ranking_update',

                'ranking':
                    ranking,

                'period':
                    self.ranking_period,
            })

        # =================================================
        # WebRTC - Camera Started
        # =================================================

        elif (
            message_type ==
            'camera_share_started'
        ):

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'camera_share_started',

                    'user_id':
                        self.user_id,

                    'username':
                        self.username,
                }
            )

        # =================================================
        # WebRTC - Camera Stopped
        # =================================================

        elif (
            message_type ==
            'camera_share_stopped'
        ):

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'camera_share_stopped',

                    'user_id':
                        self.user_id,
                }
            )

        # =================================================
        # Camera State Request
        # =================================================

        elif (
            message_type ==
            'camera_state_request'
        ):

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'camera_state_request',

                    'requester_id':
                        self.user_id,
                }
            )

        # =================================================
        # Camera State Response
        # =================================================

        elif (
            message_type ==
            'camera_state_response'
        ):

            target_user_id = content.get(
                'target_user_id'
            )

            if target_user_id is None:
                return

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'camera_state_response',

                    'user_id':
                        self.user_id,

                    'username':
                        self.username,

                    'target_user_id':
                        target_user_id,
                }
            )

        # =================================================
        # WebRTC Offer
        # =================================================

        elif (
            message_type ==
            'webrtc_offer'
        ):

            target_user_id = content.get(
                'target_user_id'
            )

            offer = content.get(
                'offer'
            )

            if (
                target_user_id is None
                or not offer
            ):
                return

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'webrtc_offer',

                    'sender_id':
                        self.user_id,

                    'sender_username':
                        self.username,

                    'target_user_id':
                        target_user_id,

                    'offer':
                        offer,
                }
            )

        # =================================================
        # WebRTC Answer
        # =================================================

        elif (
            message_type ==
            'webrtc_answer'
        ):

            target_user_id = content.get(
                'target_user_id'
            )

            answer = content.get(
                'answer'
            )

            if (
                target_user_id is None
                or not answer
            ):
                return

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'webrtc_answer',

                    'sender_id':
                        self.user_id,

                    'target_user_id':
                        target_user_id,

                    'answer':
                        answer,
                }
            )

        # =================================================
        # WebRTC ICE Candidate
        # =================================================

        elif (
            message_type ==
            'webrtc_ice_candidate'
        ):

            target_user_id = content.get(
                'target_user_id'
            )

            candidate = content.get(
                'candidate'
            )

            if (
                target_user_id is None
                or not candidate
            ):
                return

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'webrtc_ice_candidate',

                    'sender_id':
                        self.user_id,

                    'target_user_id':
                        target_user_id,

                    'candidate':
                        candidate,
                }
            )

        # =================================================
        # CHAT HISTORY
        # =================================================

        elif (
            message_type ==
            'chat_history_request'
        ):

            history = (
                await self.get_chat_history()
            )

            await self.send_json({

                'type':
                    'chat_history',

                'messages':
                    history,
            })

        # =================================================
        # CHAT MESSAGE
        # =================================================

        elif (
            message_type ==
            'chat_message'
        ):

            message = content.get(
                'message',
                ''
            )

            client_id = content.get(
                'client_id',
                ''
            )

            # -------------------------------------------------
            # Validation
            # -------------------------------------------------

            if not isinstance(
                message,
                str
            ):
                return

            message = message.strip()

            if not message:
                return

            if len(message) > 1000:
                return

            # -------------------------------------------------
            # Save
            # -------------------------------------------------

            message_data = (
                await self.create_chat_message(
                    message,
                    client_id,
                )
            )

            if not message_data:
                return

            # -------------------------------------------------
            # Broadcast to all room members
            # -------------------------------------------------

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'chat_message',

                    'message_data':
                        message_data,
                }
            )

    # =====================================================
    # Room Member Joined
    # =====================================================

    async def room_member_joined(
        self,
        event
    ):

        if (
            event['user_id']
            ==
            self.user_id
        ):
            return

        await self.send_json({

            'type':
                'room_member_joined',

            'user_id':
                event['user_id'],

            'username':
                event['username'],
        })

    # =====================================================
    # Room Member Left
    # =====================================================

    async def room_member_left(
        self,
        event
    ):

        if (
            event['user_id']
            ==
            self.user_id
        ):
            return

        await self.send_json({

            'type':
                'room_member_left',

            'user_id':
                event['user_id'],
        })

    # =====================================================
    # Camera Share Started
    # =====================================================

    async def camera_share_started(
        self,
        event
    ):

        if (
            event['user_id']
            ==
            self.user_id
        ):
            return

        await self.send_json({

            'type':
                'camera_share_started',

            'user_id':
                event['user_id'],

            'username':
                event['username'],
        })

    # =====================================================
    # Camera Share Stopped
    # =====================================================

    async def camera_share_stopped(
        self,
        event
    ):

        if (
            event['user_id']
            ==
            self.user_id
        ):
            return

        await self.send_json({

            'type':
                'camera_share_stopped',

            'user_id':
                event['user_id'],
        })

    # =====================================================
    # Camera State Request
    # =====================================================

    async def camera_state_request(
        self,
        event
    ):

        requester_id = event.get(
            'requester_id'
        )

        if requester_id == self.user_id:
            return

        await self.send_json({

            'type':
                'camera_state_request',

            'requester_id':
                requester_id,
        })

    # =====================================================
    # Camera State Response
    # =====================================================

    async def camera_state_response(
        self,
        event
    ):

        target_user_id = event.get(
            'target_user_id'
        )

        if (
            target_user_id
            !=
            self.user_id
        ):
            return

        await self.send_json({

            'type':
                'camera_state_response',

            'user_id':
                event['user_id'],

            'username':
                event['username'],
        })

    # =====================================================
    # WebRTC Offer
    # =====================================================

    async def webrtc_offer(
        self,
        event
    ):

        if (
            event['target_user_id']
            !=
            self.user_id
        ):
            return

        await self.send_json({

            'type':
                'webrtc_offer',

            'sender_id':
                event['sender_id'],

            'sender_username':
                event['sender_username'],

            'offer':
                event['offer'],
        })

    # =====================================================
    # WebRTC Answer
    # =====================================================

    async def webrtc_answer(
        self,
        event
    ):

        if (
            event['target_user_id']
            !=
            self.user_id
        ):
            return

        await self.send_json({

            'type':
                'webrtc_answer',

            'sender_id':
                event['sender_id'],

            'answer':
                event['answer'],
        })

    # =====================================================
    # WebRTC ICE Candidate
    # =====================================================

    async def webrtc_ice_candidate(
        self,
        event
    ):

        if (
            event['target_user_id']
            !=
            self.user_id
        ):
            return

        await self.send_json({

            'type':
                'webrtc_ice_candidate',

            'sender_id':
                event['sender_id'],

            'candidate':
                event['candidate'],
        })

    # =====================================================
    # Ranking Refresh
    # =====================================================

    async def ranking_refresh(
        self,
        event
    ):

        ranking = (
            await database_sync_to_async(
                get_room_ranking
            )(
                self.room_id,
                self.ranking_period
            )
        )

        await self.send_json({

            'type':
                'ranking_update',

            'ranking':
                ranking,

            'period':
                self.ranking_period,
        })

    # =====================================================
    # CHAT MESSAGE
    # =====================================================

    async def chat_message(
        self,
        event
    ):

        message_data = (
            event.get(
                'message_data'
            )
        )

        if not message_data:
            return

        await self.send_json({

            'type':
                'chat_message',

            'message_data':
                message_data,
        })

    # =====================================================
    # Chat History
    # =====================================================

    @database_sync_to_async
    def get_chat_history(
        self
    ):

        messages = list(
            RoomChatMessage.objects
            .filter(
                room_id=self.room_id
            )
            .select_related('user')
            .order_by('-created_at')[:300]
        )

        messages.reverse()

        return [

            {
                'id':
                    message.id,

                'client_id':
                    message.client_id,

                'user_id':
                    message.user_id,

                'username':
                    message.user.username,

                'message':
                    message.message,

                'created_at':
                    message.created_at.isoformat(),
            }

            for message in messages
        ]

    # =====================================================
    # Create Chat Message
    # =====================================================

    @database_sync_to_async
    def create_chat_message(
        self,
        message,
        client_id
    ):

        try:

            message_obj = (
                RoomChatMessage.objects.create(

                    room_id=self.room_id,

                    user_id=self.user_id,

                    message=message,

                    client_id=client_id or '',
                )
            )

            return {

                'id':
                    message_obj.id,

                'client_id':
                    message_obj.client_id,

                'user_id':
                    self.user_id,

                'username':
                    self.username,

                'message':
                    message_obj.message,

                'created_at':
                    message_obj.created_at.isoformat(),
            }

        except Exception as error:

            print(
                'CHAT MESSAGE SAVE ERROR:',
                error
            )

            return None

    # =====================================================
    # Membership
    # =====================================================

    @database_sync_to_async
    def check_membership(
        self,
        user_id,
        room_id
    ):

        return (
            RoomMembership.objects
            .filter(
                room_id=room_id,
                user_id=user_id,
                is_active=True,
                room__is_active=True,
            )
            .exists()
        )