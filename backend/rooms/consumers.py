from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from django.utils import timezone

from .models import (
    RoomMembership,
    RoomChatMessage,
    RoomChatMessageEditHistory,
    RoomChatReaction,
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

            reply_to_id = content.get(
                'reply_to_id'
            )

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

            if reply_to_id is not None:

                try:
                    reply_to_id = int(
                        reply_to_id
                    )
                except (
                    TypeError,
                    ValueError
                ):
                    return

            message_data = (
                await self.create_chat_message(
                    message,
                    client_id,
                    reply_to_id,
                )
            )

            if not message_data:
                return

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'chat_message',

                    'message_data':
                        message_data,
                }
            )

        # =================================================
        # EDIT MESSAGE
        # =================================================

        elif (
            message_type ==
            'chat_message_edit'
        ):

            message_id = content.get(
                'message_id'
            )

            new_message = content.get(
                'message',
                ''
            )

            try:

                message_id = int(
                    message_id
                )

            except (
                TypeError,
                ValueError
            ):

                return

            if not isinstance(
                new_message,
                str
            ):
                return

            new_message = (
                new_message.strip()
            )

            if not new_message:
                return

            if len(new_message) > 1000:
                return

            message_data = (
                await self.edit_chat_message(
                    message_id,
                    new_message,
                )
            )

            if not message_data:
                return

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'chat_message_edited',

                    'message_data':
                        message_data,
                }
            )

        # =================================================
        # DELETE MESSAGE
        # =================================================

        elif (
            message_type ==
            'chat_message_delete'
        ):

            message_id = content.get(
                'message_id'
            )

            try:

                message_id = int(
                    message_id
                )

            except (
                TypeError,
                ValueError
            ):

                return

            message_data = (
                await self.delete_chat_message(
                    message_id
                )
            )

            if not message_data:
                return

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'chat_message_deleted',

                    'message_data':
                        message_data,
                }
            )

        # =================================================
        # REPLY
        # =================================================
        #
        # Reply itself is stored when chat_message is sent.
        # This block is intentionally not needed.
        #
        # =================================================

        # =================================================
        # REACTION
        # =================================================

        elif (
            message_type ==
            'chat_message_reaction'
        ):

            message_id = content.get(
                'message_id'
            )

            reaction = content.get(
                'reaction'
            )

            try:

                message_id = int(
                    message_id
                )

            except (
                TypeError,
                ValueError
            ):

                return

            valid_reactions = {
                'cry',
                'laugh',
                'heart',
                'like',
                'dislike',
            }

            if reaction not in valid_reactions:
                return

            reaction_data = (
                await self.set_chat_reaction(
                    message_id,
                    reaction,
                )
            )

            if not reaction_data:
                return

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'chat_message_reaction_updated',

                    'reaction_data':
                        reaction_data,
                }
            )

        # =================================================
        # REMOVE REACTION
        # =================================================

        elif (
            message_type ==
            'chat_message_reaction_remove'
        ):

            message_id = content.get(
                'message_id'
            )

            try:

                message_id = int(
                    message_id
                )

            except (
                TypeError,
                ValueError
            ):

                return

            reaction_data = (
                await self.remove_chat_reaction(
                    message_id
                )
            )

            if not reaction_data:
                return

            await self.channel_layer.group_send(

                self.room_group_name,

                {
                    'type':
                        'chat_message_reaction_removed',

                    'reaction_data':
                        reaction_data,
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
    # CHAT MESSAGE EDITED
    # =====================================================

    async def chat_message_edited(
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
                'chat_message_edited',

            'message_data':
                message_data,
        })

    # =====================================================
    # CHAT MESSAGE DELETED
    # =====================================================

    async def chat_message_deleted(
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
                'chat_message_deleted',

            'message_data':
                message_data,
        })

    # =====================================================
    # CHAT REACTION UPDATED
    # =====================================================

    async def chat_message_reaction_updated(
        self,
        event
    ):

        reaction_data = (
            event.get(
                'reaction_data'
            )
        )

        if not reaction_data:
            return

        await self.send_json({

            'type':
                'chat_message_reaction_updated',

            'reaction_data':
                reaction_data,
        })

    # =====================================================
    # CHAT REACTION REMOVED
    # =====================================================

    async def chat_message_reaction_removed(
        self,
        event
    ):

        reaction_data = (
            event.get(
                'reaction_data'
            )
        )

        if not reaction_data:
            return

        await self.send_json({

            'type':
                'chat_message_reaction_removed',

            'reaction_data':
                reaction_data,
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
            .select_related(
                'user',
                'reply_to',
                'reply_to__user',
                'deleted_by',
            )
            .prefetch_related(
                'reactions',
                'reactions__user',
            )
            .order_by('-created_at')[:300]
        )

        messages.reverse()

        return [
            self.serialize_message(
                message
            )
            for message in messages
        ]

    # =====================================================
    # Create Chat Message
    # =====================================================

    @database_sync_to_async
    def create_chat_message(
        self,
        message,
        client_id,
        reply_to_id=None,
    ):

        try:

            reply_to = None

            if reply_to_id is not None:

                reply_to = (
                    RoomChatMessage.objects
                    .filter(
                        id=reply_to_id,
                        room_id=self.room_id,
                    )
                    .first()
                )

                if not reply_to:
                    return None

            message_obj = (
                RoomChatMessage.objects.create(

                    room_id=self.room_id,

                    user_id=self.user_id,

                    message=message,

                    client_id=client_id or '',

                    reply_to=reply_to,
                )
            )

            return self.serialize_message(
                message_obj
            )

        except Exception as error:

            print(
                'CHAT MESSAGE SAVE ERROR:',
                error
            )

            return None

    # =====================================================
    # Edit Chat Message
    # =====================================================

    @database_sync_to_async
    def edit_chat_message(
        self,
        message_id,
        new_message,
    ):

        try:

            message_obj = (
                RoomChatMessage.objects
                .select_related(
                    'user',
                    'reply_to',
                    'reply_to__user',
                    'deleted_by',
                )
                .prefetch_related(
                    'reactions',
                    'reactions__user',
                )
                .filter(
                    id=message_id,
                    room_id=self.room_id,
                )
                .first()
            )

            if not message_obj:
                return None

            # فقط صاحب پیام
            if message_obj.user_id != self.user_id:
                return None

            # پیام حذف‌شده قابل ویرایش نیست
            if message_obj.is_deleted:
                return None

            # اگر متن واقعاً تغییر نکرده
            if message_obj.message == new_message:
                return None

            # ذخیره نسخه قبلی
            RoomChatMessageEditHistory.objects.create(

                message=message_obj,

                old_message=message_obj.message,

                edited_by_id=self.user_id,
            )

            message_obj.message = new_message
            message_obj.edited_at = timezone.now()

            message_obj.save(
                update_fields=[
                    'message',
                    'edited_at',
                ]
            )

            return self.serialize_message(
                message_obj
            )

        except Exception as error:

            print(
                'CHAT MESSAGE EDIT ERROR:',
                error
            )

            return None

    # =====================================================
    # Delete Chat Message
    # =====================================================

    @database_sync_to_async
    def delete_chat_message(
        self,
        message_id
    ):

        try:

            message_obj = (
                RoomChatMessage.objects
                .select_related(
                    'user',
                    'reply_to',
                    'reply_to__user',
                    'deleted_by',
                )
                .prefetch_related(
                    'reactions',
                    'reactions__user',
                )
                .filter(
                    id=message_id,
                    room_id=self.room_id,
                )
                .first()
            )

            if not message_obj:
                return None

            # فقط صاحب پیام
            if message_obj.user_id != self.user_id:
                return None

            # قبلاً حذف شده
            if message_obj.is_deleted:
                return None

            message_obj.is_deleted = True
            message_obj.deleted_at = timezone.now()
            message_obj.deleted_by_id = self.user_id

            message_obj.save(
                update_fields=[
                    'is_deleted',
                    'deleted_at',
                    'deleted_by',
                ]
            )

            return self.serialize_message(
                message_obj
            )

        except Exception as error:

            print(
                'CHAT MESSAGE DELETE ERROR:',
                error
            )

            return None

    # =====================================================
    # Set Reaction
    # =====================================================

    @database_sync_to_async
    def set_chat_reaction(
        self,
        message_id,
        reaction,
    ):

        try:

            message_obj = (
                RoomChatMessage.objects
                .filter(
                    id=message_id,
                    room_id=self.room_id,
                )
                .first()
            )

            if not message_obj:
                return None

            if message_obj.is_deleted:
                return None

            reaction_obj = (
                RoomChatReaction.objects
                .filter(
                    message_id=message_id,
                    user_id=self.user_id,
                )
                .first()
            )

            if reaction_obj:

                reaction_obj.reaction = reaction

                reaction_obj.save(
                    update_fields=[
                        'reaction'
                    ]
                )

            else:

                reaction_obj = (
                    RoomChatReaction.objects.create(

                        message=message_obj,

                        user_id=self.user_id,

                        reaction=reaction,
                    )
                )

            return self.serialize_reaction(
                reaction_obj
            )

        except Exception as error:

            print(
                'CHAT REACTION ERROR:',
                error
            )

            return None

    # =====================================================
    # Remove Reaction
    # =====================================================

    @database_sync_to_async
    def remove_chat_reaction(
        self,
        message_id
    ):

        try:

            reaction_obj = (
                RoomChatReaction.objects
                .select_related(
                    'user',
                    'message',
                )
                .filter(
                    message_id=message_id,
                    user_id=self.user_id,
                )
                .first()
            )

            if not reaction_obj:
                return None

            data = self.serialize_reaction(
                reaction_obj
            )

            reaction_obj.delete()

            return data

        except Exception as error:

            print(
                'CHAT REACTION REMOVE ERROR:',
                error
            )

            return None

    # =====================================================
    # Serialize Message
    # =====================================================

    def serialize_message(
        self,
        message
    ):

        reactions = []

        try:

            for reaction in (
                message.reactions.all()
            ):

                reactions.append({

                    'id':
                        reaction.id,

                    'user_id':
                        reaction.user_id,

                    'username':
                        reaction.user.username,

                    'reaction':
                        reaction.reaction,

                    'created_at':
                        reaction.created_at.isoformat(),
                })

        except Exception:

            reactions = []

        reply_data = None

        if message.reply_to:

            reply_data = {

                'id':
                    message.reply_to.id,

                'user_id':
                    message.reply_to.user_id,

                'username':
                    message.reply_to.user.username,

                'message':
                    message.reply_to.message,

                'is_deleted':
                    message.reply_to.is_deleted,
            }

        return {

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

            'edited_at':
                (
                    message.edited_at.isoformat()
                    if message.edited_at
                    else None
                ),

            'is_deleted':
                message.is_deleted,

            'deleted_at':
                (
                    message.deleted_at.isoformat()
                    if message.deleted_at
                    else None
                ),

            'deleted_by_id':
                message.deleted_by_id,

            'reply_to':
                reply_data,

            'reactions':
                reactions,
        }

    # =====================================================
    # Serialize Reaction
    # =====================================================

    def serialize_reaction(
        self,
        reaction
    ):

        return {

            'id':
                reaction.id,

            'message_id':
                reaction.message_id,

            'user_id':
                reaction.user_id,

            'username':
                reaction.user.username,

            'reaction':
                reaction.reaction,

            'created_at':
                reaction.created_at.isoformat(),
        }

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