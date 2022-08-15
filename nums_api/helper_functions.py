from nums_api.models_helpers import Like

# function that queries db for top 10 facts

likes = (Like
            .query
            .filter(Like.user_id.in_(following_ids))
            .order_by(Message.timestamp.desc())
            .limit(100)
            .all())
