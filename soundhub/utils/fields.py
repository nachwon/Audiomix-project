import re

from rest_framework import serializers


class BypassEmptyStringField(serializers.ImageField):
    def to_internal_value(self, data):
        if data == '':
            return data
        return super().to_internal_value(data)


class ProfileImageField(BypassEmptyStringField):
    def to_representation(self, value):
        if not value:
            return None
        p = re.compile(r'(user_\d+/profile_img/)')
        path = p.match(value.name).group(1)

        data = {
            "profile_img_200": f"{path}profile_img_200.png",
            "profile_img_400": f"{path}profile_img_400.png",
        }
        return data


class LikedPostsField(serializers.RelatedField):
    def to_representation(self, value):
        post_list = value.all()
        data_list = list()
        for post in post_list:
            if post.author.profile_img.name == "":
                profile_img = None
            else:
                profile_img = post.author.profile_img.name
            data = {
                "id": post.pk,
                "author": {
                    "id": post.author.id,
                    "nickname": post.author.nickname,
                    "profile_img": profile_img,
                },
                "title": post.title,
                "genre": post.genre,
                "instrument": post.instrument,
                "num_liked": post.num_liked,
                "num_comments": post.num_comments,
                "created_date": post.created_date,
            }
            data_list.append(data)
        return data_list


class PostSetField(serializers.RelatedField):
    def to_representation(self, value):
        post_list = value.all()
        data_list = list()
        for post in post_list:
            data = {
                "id": post.pk,
                "title": post.title,
                "genre": post.genre,
                "instrument": post.instrument,
                "num_liked": post.num_liked,
                "num_comments": post.num_comments,
                "created_date": post.created_date,
            }
            data_list.append(data)
        return data_list


class AuthorField(serializers.RelatedField):
    def to_representation(self, value):
        if value.profile_img.name == "":
            profile_img = None
        else:
            profile_img = value.profile_img.name
        data = {
            "id": value.id,
            "nickname": value.nickname,
            "profile_img": profile_img
        }

        return data
