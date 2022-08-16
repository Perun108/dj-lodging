class UserRepository:
    @classmethod
    def save(cls, user):
        user.save()
