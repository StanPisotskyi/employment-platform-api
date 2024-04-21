from django.db import models
from api_auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class SkillManager(models.Manager):
    def create(self, title):
        if title is None:
            raise TypeError('Skill must have a title.')

        try:
            existed_skill = Skill.objects.get(title=title)
        except ObjectDoesNotExist:
            existed_skill = None

        if isinstance(existed_skill, Skill):
            raise TypeError('Skill already exists.')

        skill = Skill(title=title)

        skill.save()

        return skill


class UserSkillManager(models.Manager):
    pass


class SkillEvaluationManager(models.Manager):
    pass


class Skill(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, db_index=True, unique=True)

    REQUIRED_FIELDS = ['title']

    objects = SkillManager()

    def __str__(self):
        return self.title


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='skill_user_set')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=False, related_name='skill_skill_set')

    REQUIRED_FIELDS = ['user', 'skill']

    objects = UserSkillManager()

    class Meta:
        unique_together = (('user', 'skill'),)

    def __str__(self):
        return self.skill.title


class SkillEvaluation(models.Model):
    link = models.ForeignKey(UserSkill, on_delete=models.CASCADE, null=False, related_name='evaluation_link_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='evaluation_user_set')

    REQUIRED_FIELDS = ['link', 'user']

    objects = SkillEvaluationManager()

    class Meta:
        unique_together = (('link', 'user'),)

    def __str__(self):
        return self.link.skill.title
