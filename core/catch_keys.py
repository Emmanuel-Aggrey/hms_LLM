class CACHE_KEY:
    @staticmethod
    def get_token_key(user_id: str):
        return f"token_id_{user_id}"
